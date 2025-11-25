"""Tests for benchmark-ips functionality."""

import pytest
import sys
import io
import json
import tempfile
import os
import time
import benchmark_ips as bm
from benchmark_ips.helpers import humanize_duration, scale


class TestBenchmarkIPS:
    """Test suite for benchmark-ips."""

    def test_kwargs(self, capsys):
        """Test benchmark with keyword arguments."""
        def bench(x):
            x.report("sleep 0.25", lambda: time.sleep(0.25))

        bm.ips(bench, time=0.001, warmup=0.001, quiet=False)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_warmup0(self, capsys):
        """Test benchmark with zero warmup."""
        def bench(x):
            x.report("sleep 0.25", lambda: time.sleep(0.25))

        bm.ips(bench, time=1, warmup=0, quiet=False)

        captured = capsys.readouterr()
        assert "Warming up" not in captured.out
        assert len(captured.err) == 0

    def test_output(self, capsys):
        """Test that output is generated."""
        def bench(x):
            x.warmup = 0
            x.time = 0.1
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench, time=1)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_quiet(self, capsys):
        """Test quiet mode."""
        def bench(x):
            x.config({'warmup': 0.001, 'time': 0.001})
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench, quiet=True)
        captured = capsys.readouterr()
        assert len(captured.out) == 0

        def bench2(x):
            x.config({'warmup': 0.001, 'time': 0.001, 'quiet': True})
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench2)
        captured = capsys.readouterr()
        assert len(captured.out) == 0

        def bench3(x):
            x.config({'warmup': 0.001, 'time': 0.001})
            x.set_quiet(True)
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench3)
        captured = capsys.readouterr()
        assert len(captured.out) == 0

    def test_quiet_option_override(self, capsys):
        """Test quiet option override."""
        def bench(x):
            x.config({'warmup': 0.001, 'time': 0.001})
            x.set_quiet(False)
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench, quiet=True)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

        def bench2(x):
            x.config({'quiet': False, 'warmup': 0.001, 'time': 0.001})
            x.report("operation", lambda: 100 * 100)

        bm.ips(bench2, quiet=True)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_ips(self):
        """Test basic IPS functionality."""
        def bench(x):
            x.config({'time': 1, 'warmup': 1})
            x.report("sleep 0.25", lambda: time.sleep(0.25))
            x.report("sleep 0.05", lambda: time.sleep(0.05))
            x.enable_compare()

        report = bm.ips(bench)

        rep1 = report.entries[0]
        rep2 = report.entries[1]

        assert rep1.label == "sleep 0.25"
        assert rep1.iterations == 4
        assert abs(rep1.ips - 4.0) < 0.2

        assert rep2.label == "sleep 0.05"
        assert abs(rep2.iterations - 20.0) < 1.0
        assert abs(rep2.ips - 20.0) < 2.0

    def test_ips_alternate_config(self):
        """Test alternate configuration method."""
        def bench(x):
            x.time = 1
            x.warmup = 1
            x.report("sleep 0.25", lambda: time.sleep(0.25))

        report = bm.ips(bench)
        rep = report.entries[0]

        assert rep.label == "sleep 0.25"
        assert rep.iterations == 4
        assert abs(rep.ips - 4.0) < 0.4

    def test_ips_defaults(self):
        """Test default configuration."""
        def bench(x):
            x.report("sleep 0.25", lambda: time.sleep(0.25))

        report = bm.ips(bench)
        rep = report.entries[0]

        assert rep.label == "sleep 0.25"
        assert rep.iterations == 4 * 5  # 4 per second * 5 seconds
        assert abs(rep.ips - 4.0) < 0.2

    def test_ips_report_using_symbol(self):
        """Test reporting with different label types."""
        def bench(x):
            x.warmup = 0
            x.time = 0.1
            x.report("sleep_a_quarter_second", lambda: 1 + 1)

        report = bm.ips(bench)
        rep = report.entries[0]

        assert rep.label == "sleep_a_quarter_second"

    def test_ips_default_data(self):
        """Test default data structure."""
        def bench(x):
            x.config({'warmup': 0.001, 'time': 0.001})
            x.report("sleep 0.25", lambda: time.sleep(0.25))

        report = bm.ips(bench)
        all_data = report.data

        assert all_data
        assert all_data[0]['name'] == "sleep 0.25"
        assert 'ips' in all_data[0]
        assert 'stddev' in all_data[0]

    def test_ips_empty(self):
        """Test empty benchmark."""
        def bench(x):
            x.config({'warmup': 0.001, 'time': 0.001})

        report = bm.ips(bench)
        all_data = report.data

        assert all_data is not None
        assert all_data == []

    def test_json_output(self):
        """Test JSON output to file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as json_file:
            json_path = json_file.name

        try:
            def bench(x):
                x.config({'warmup': 0.001, 'time': 0.001})
                x.report("sleep 0.25", lambda: time.sleep(0.25))
                x.enable_json(json_path)

            bm.ips(bench)

            with open(json_path, 'r') as f:
                json_data = f.read()

            assert json_data

            data = json.loads(json_data)
            assert data
            assert len(data) == 1
            assert data[0]['name'] == "sleep 0.25"
            assert 'ips' in data[0]
            assert 'stddev' in data[0]
        finally:
            if os.path.exists(json_path):
                os.remove(json_path)

    def test_json_output_to_stdout(self):
        """Test JSON output to stdout."""
        output_capture = io.StringIO()

        def bench(x):
            x.config({'warmup': 0.001, 'time': 0.001})
            x.report("sleep 0.25", lambda: time.sleep(0.25))
            x.set_quiet(True)
            x.enable_json(output_capture)

        bm.ips(bench)

        json_str = output_capture.getvalue()
        assert len(json_str) > 0

        data = json.loads(json_str)
        assert data
        assert len(data) == 1
        assert data[0]['name'] == "sleep 0.25"
        assert 'ips' in data[0]
        assert 'stddev' in data[0]

    def test_hold(self):
        """Test hold functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as temp_file:
            temp_file_name = temp_file.name

        try:
            def bench(x):
                x.report("operation", lambda: 100 * 100)
                x.report("operation2", lambda: 100 * 100)
                x.hold(temp_file_name)

            bm.ips(bench, time=0.001, warmup=0.001)

            assert os.path.exists(temp_file_name)
        finally:
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)

    def test_small_warmup_and_time(self):
        """Test with very small warmup and time values."""
        def bench1(x):
            x.config({'warmup': 0.0000000001, 'time': 0.001})
            x.report("addition", lambda: 1 + 2)

        report = bm.ips(bench1)
        assert report.entries[0].iterations >= 1

        def bench2(x):
            x.config({'warmup': 0, 'time': 0.0000000001})
            x.report("addition", lambda: 1 + 2)

        report = bm.ips(bench2)
        assert report.entries[0].iterations == 1

        def bench3(x):
            x.config({'warmup': 0.001, 'time': 0.0000000001})
            x.report("addition", lambda: 1 + 2)

        report = bm.ips(bench3)
        assert report.entries[0].iterations >= 1

        def bench4(x):
            x.config({'warmup': 0.0000000001, 'time': 0.0000000001})
            x.report("addition", lambda: 1 + 2)

        report = bm.ips(bench4)
        assert report.entries[0].iterations >= 1

        def bench5(x):
            x.config({'warmup': 0, 'time': 0})
            x.report("addition", lambda: 1 + 2)

        report = bm.ips(bench5)
        assert report.entries[0].iterations == 1

    def test_humanize_duration(self):
        """Test humanize_duration function."""
        assert humanize_duration(0.000000001) == "0.00 ns"
        assert humanize_duration(123.456789) == "123.46 ns"
        assert humanize_duration(12345.67890123) == "12.35 μs"
        assert humanize_duration(123456789.0123456789) == "123.46 ms"
        assert humanize_duration(123456789012.3456789012) == "123.46 s"

    def test_scale(self):
        """Test scale function."""
        result = scale(1000)
        assert 'k' in result or '1' in result

        result = scale(1000000)
        assert 'M' in result or '1' in result

    def test_quick(self, capsys):
        """Test ips_quick function."""
        bm.ips_quick('upper', 'lower', on="Hello World!", warmup=0.001, time=0.001)
        captured = capsys.readouterr()
        assert len(captured.out) > 0
