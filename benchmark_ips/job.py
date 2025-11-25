"""Job class for managing benchmarks."""

import sys
import json
import os
import platform
from .job_entry import JobEntry
from .report import Report
from . import timing
from .stats import SD


# Microseconds per 100 milliseconds
MICROSECONDS_PER_100MS = 100_000
# Microseconds per second
MICROSECONDS_PER_SECOND = timing.MICROSECONDS_PER_SECOND
# The percentage of the expected runtime to allow before reporting a weird runtime
MAX_TIME_SKEW = 0.05
# Keep iterations below this to avoid overflow
MAX_ITERATIONS = 1 << 30


class StreamReport:
    """Stream report for outputting benchmark progress."""

    def __init__(self, job, stream=None):
        """
        Initialize StreamReport.

        Args:
            job: Parent Job instance
            stream: Output stream (default: sys.stdout)
        """
        self.last_item = None
        self.out = stream or sys.stdout
        self.job = job

    def start_warming(self):
        """Print warming up header."""
        self.out.write(f"Python {platform.python_version()} on {platform.system()}\n")
        self.out.write("Warming up --------------------------------------\n")

    def start_running(self):
        """Print calculating header."""
        self.out.write("Calculating -------------------------------------\n")

    def warming(self, label, warmup):
        """
        Print warming label.

        Args:
            label: Benchmark label
            warmup: Warmup time
        """
        self.out.write(str(label).rjust(self.job.max_width))

    def running(self, label, time):
        """
        Print running label.

        Args:
            label: Benchmark label
            time: Benchmark time
        """
        self.warming(label, time)

    def warmup_stats(self, warmup_time_us, timing_val):
        """
        Print warmup statistics.

        Args:
            warmup_time_us: Warmup time in microseconds
            timing_val: Timing value
        """
        from .helpers import scale
        format_type = self.job.format_type

        if format_type == 'human':
            self.out.write(f"{scale(timing_val)} i/100ms\n")
        else:
            self.out.write(f"{timing_val:10d} i/100ms\n")

    def add_report(self, item, caller=None):
        """
        Add report item.

        Args:
            item: Report entry
            caller: Caller information
        """
        self.out.write(f" {item.body(self.job.format_type, self.job.max_width)}\n")
        self.last_item = item

    def footer(self):
        """Print footer."""
        if self.last_item:
            footer_text = self.last_item.stats.footer()
            if footer_text:
                self.out.write(footer_text.rjust(40) + "\n")


class MultiReport:
    """Multi-report handler that can output to multiple streams."""

    def __init__(self, *reporters):
        """
        Initialize MultiReport.

        Args:
            reporters: List of reporter instances
        """
        self.reporters = list(reporters)

    def __lshift__(self, reporter):
        """
        Add a reporter.

        Args:
            reporter: Reporter to add
        """
        self.reporters.append(reporter)

    def quiet(self):
        """Check if all reporters are quiet."""
        return all(not isinstance(r, StreamReport) for r in self.reporters)

    def make_quiet(self):
        """Remove all StreamReport instances."""
        self.reporters = [r for r in self.reporters if not isinstance(r, StreamReport)]

    def __getattr__(self, name):
        """Delegate method calls to all reporters."""
        def method(*args, **kwargs):
            for reporter in self.reporters:
                if hasattr(reporter, name):
                    getattr(reporter, name)(*args, **kwargs)
        return method


class Job:
    """Benchmark job manager."""

    def __init__(self, opts=None):
        """
        Initialize the Job.

        Args:
            opts: Optional configuration dictionary
        """
        opts = opts or {}

        self.list = []
        self.run_single = False
        self.json_path = False
        self.compare = False
        self.compare_order = 'fastest'
        self.held_path = None
        self.held_results = None
        self.max_width = 20  # automatically computed as entries are added

        self.timing_data = {}  # default to 1 in case warmup isn't run
        self.full_report = Report()

        # Default warmup and calculation time in seconds
        self.warmup = 2
        self.time = 5
        self.iterations = 1

        # Default statistical model
        self.stats_type = 'sd'
        self.confidence = 95

        # Format type
        self.format_type = 'human'

        self._out = MultiReport(StreamReport(self))

    def config(self, opts=None, **kwargs):
        """
        Configure job options.

        Args:
            opts: Configuration dictionary (optional)
            **kwargs: Configuration as keyword arguments
        """
        # Merge opts dict and kwargs
        if opts is None:
            opts = kwargs
        else:
            opts = {**opts, **kwargs}

        if 'warmup' in opts:
            self.warmup = opts['warmup']
        if 'time' in opts:
            self.time = opts['time']
        if 'iterations' in opts:
            self.iterations = opts['iterations']
        if 'stats' in opts:
            self.stats_type = opts['stats']
        if 'confidence' in opts:
            self.confidence = opts['confidence']
        if 'quiet' in opts:
            self.set_quiet(opts['quiet'])
        if 'suite' in opts:
            self.set_suite(opts['suite'])

    @property
    def quiet(self):
        """Check if output is quiet."""
        return self._out.quiet()

    def set_quiet(self, val):
        """
        Set quiet mode.

        Args:
            val: True to enable quiet mode
        """
        if val:
            self._out.make_quiet()
        else:
            if self._out.quiet():
                self._out << StreamReport(self)

    def set_suite(self, suite):
        """
        Set custom suite.

        Args:
            suite: Custom suite instance
        """
        self._out << suite

    @property
    def suite(self):
        """Get suite."""
        return self._out

    def is_compare(self):
        """
        Check if comparison is enabled.

        Returns:
            bool: True if comparison is enabled
        """
        return self.compare

    def enable_compare(self, order='fastest'):
        """
        Enable comparison.

        Args:
            order: Comparison order
        """
        self.compare = True
        self.compare_order = order

    def is_hold(self):
        """
        Check if results are held.

        Returns:
            bool: True if holding results
        """
        return self.held_path is not None

    def hold(self, held_path):
        """
        Hold results after each iteration.

        Args:
            held_path: File path to store results
        """
        self.held_path = held_path
        self.run_single = True

    def save(self, held_path):
        """
        Save interim results.

        Args:
            held_path: File path to store results
        """
        self.held_path = held_path
        self.run_single = False

    def is_run_single(self):
        """
        Check if running single items.

        Returns:
            bool: True if running single items
        """
        return self.run_single

    def is_json(self):
        """
        Check if JSON output is enabled.

        Returns:
            bool: True if JSON output is enabled
        """
        return bool(self.json_path)

    def enable_json(self, path="data.json"):
        """
        Enable JSON output.

        Args:
            path: Path for JSON output
        """
        self.json_path = path

    def item(self, label="", action=None):
        """
        Register a benchmark item.

        Args:
            label: Label of benchmarked code
            action: Code to be benchmarked (callable or string)

        Returns:
            Job: Self for chaining

        Raises:
            ValueError: If action is not provided
        """
        if action is None:
            raise ValueError("no action provided")

        label_str = str(label)
        if len(label_str) > self.max_width:
            self.max_width = len(label_str)

        self.list.append(JobEntry(label, action))
        return self

    def report(self, label="", action=None):
        """
        Alias for item().

        Args:
            label: Label of benchmarked code
            action: Code to be benchmarked

        Returns:
            Job: Self for chaining
        """
        return self.item(label, action)

    def cycles_per_100ms(self, time_msec, iters):
        """
        Calculate cycles needed to run for approx 100ms.

        Args:
            time_msec: Each iteration's time in microseconds
            iters: Iterations

        Returns:
            int: Cycles per 100ms
        """
        cycles = int((MICROSECONDS_PER_100MS / time_msec) * iters)
        return max(cycles, 1)

    def time_us(self, before, after):
        """
        Calculate time difference in microseconds.

        Args:
            before: Before time
            after: After time

        Returns:
            float: Time difference
        """
        return timing.time_us(before, after)

    def iterations_per_sec(self, cycles, time_us):
        """
        Calculate iterations per second.

        Args:
            cycles: Number of cycles
            time_us: Time in microseconds

        Returns:
            float: Iterations per second
        """
        return MICROSECONDS_PER_SECOND * (cycles / time_us)

    def load_held_results(self):
        """Load held results from file."""
        if not self.held_path or not os.path.exists(self.held_path) or os.path.getsize(self.held_path) == 0:
            return

        with open(self.held_path, 'r') as f:
            data = json.load(f)

        self.held_results = {}
        for result in data:
            self.held_results[result['item']] = result
            stats = self.create_stats(result['samples'])
            self.create_report(
                result['item'],
                result['measured_us'],
                result['iter'],
                stats,
                result['cycles']
            )

    def save_held_results(self):
        """Save held results to file."""
        if not self.held_path:
            return

        data = [
            {
                'item': e.label,
                'measured_us': e.microseconds,
                'iter': e.iterations,
                'samples': e.samples,
                'cycles': e.measurement_cycle
            }
            for e in self.full_report.entries
        ]

        with open(self.held_path, 'w') as f:
            json.dump(data, f)
            f.write("\n")

    def all_results_have_been_run(self):
        """
        Check if all results have been run.

        Returns:
            bool: True if all results are complete
        """
        return len(self.full_report.entries) == len(self.list)

    def clear_held_results(self):
        """Clear held results file."""
        if os.path.exists(self.held_path):
            os.remove(self.held_path)

    def run(self):
        """Run the benchmark."""
        if self.warmup and self.warmup != 0:
            self._out.start_warming()
            for _ in range(self.iterations):
                self.run_warmup()

        self._out.start_running()

        for n in range(self.iterations):
            self.run_benchmark()

        self._out.footer()

    def run_warmup(self):
        """Run warmup phase."""
        for item in self.list:
            if self.run_single and self.held_results and item.label in self.held_results:
                continue

            self._out.warming(item.label, self.warmup)

            timing.clean_env()

            # Run for up to half of the configured warmup time
            before = timing.now()
            target = timing.add_second(before, self.warmup / 2.0)

            cycles = 1
            while True:
                t0 = timing.now()
                item.call_times(cycles)
                t1 = timing.now()
                warmup_iter = cycles
                warmup_time_us = timing.time_us(t0, t1)

                if cycles >= MAX_ITERATIONS:
                    break
                cycles *= 2

                if timing.now() + warmup_time_us * 2 >= target:
                    break

            per_100ms = self.cycles_per_100ms(warmup_time_us, warmup_iter)
            cycles = min(per_100ms, MAX_ITERATIONS)
            self.timing_data[item] = cycles

            # Run for the remaining warmup time
            target = timing.add_second(before, self.warmup)
            while timing.now() + MICROSECONDS_PER_100MS < target:
                item.call_times(cycles)

            self._out.warmup_stats(warmup_time_us, self.timing_data[item])

            if self.run_single:
                break

    def run_benchmark(self):
        """Run benchmark calculation phase."""
        for item in self.list:
            if self.run_single and self.held_results and item.label in self.held_results:
                continue

            self._out.running(item.label, self.time)

            timing.clean_env()

            iter_count = 0
            measurements_us = []

            # Get cycles from warmup, default to 1
            cycles = self.timing_data.get(item, 1)

            target = timing.add_second(timing.now(), self.time)

            while True:
                before = timing.now()
                item.call_times(cycles)
                after = timing.now()

                iter_us = timing.time_us(before, after)
                if iter_us <= 0.0:
                    continue

                iter_count += cycles
                measurements_us.append(iter_us)

                if timing.now() >= target:
                    break

            final_time = before
            measured_us = sum(measurements_us)

            samples = [
                self.iterations_per_sec(cycles, time_us)
                for time_us in measurements_us
            ]

            stats = self.create_stats(samples)
            rep = self.create_report(item.label, measured_us, iter_count, stats, cycles)

            if abs(final_time - target) >= (self.time * MAX_TIME_SKEW):
                rep.show_total_time()

            self._out.add_report(rep, None)

            if self.run_single:
                break

    def create_stats(self, samples):
        """
        Create statistics object from samples.

        Args:
            samples: List of sample values

        Returns:
            Stats object
        """
        if self.stats_type == 'sd':
            return SD(samples)
        else:
            raise ValueError(f"unknown stats {self.stats_type}")

    def run_comparison(self):
        """Run comparison of entries."""
        if self.compare:
            self.full_report.run_comparison(self.compare_order)

    def generate_json(self):
        """Generate JSON output."""
        if self.is_json():
            self.full_report.generate_json(self.json_path)

    def create_report(self, label, measured_us, iter_count, stats, cycles):
        """
        Create report by adding entry to full_report.

        Args:
            label: Report item label
            measured_us: Measured time in microseconds
            iter_count: Number of iterations
            stats: Statistics object
            cycles: Number of cycles

        Returns:
            ReportEntry: Entry with data
        """
        return self.full_report.add_entry(label, measured_us, iter_count, stats, cycles)
