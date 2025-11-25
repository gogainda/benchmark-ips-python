"""Report module for benchmark results."""

import json
import sys
from . import compare as compare_module


class ReportEntry:
    """Represents benchmarking code data for Report."""

    def __init__(self, label, us, iters, stats, cycles):
        """
        Initialize Report Entry.

        Args:
            label: Label of entry
            us: Measured time in microseconds
            iters: Number of iterations
            stats: Statistics object
            cycles: Number of cycles
        """
        self.label = label
        self.microseconds = us
        self.iterations = iters
        self.stats = stats
        self.measurement_cycle = cycles
        self._show_total_time = False

    @property
    def ips(self):
        """
        LEGACY: Iterations per second.

        Returns:
            float: Number of iterations per second
        """
        return self.stats.central_tendency

    @property
    def ips_sd(self):
        """
        LEGACY: Standard deviation of iteration per second.

        Returns:
            float: Standard deviation of iteration per second
        """
        return self.stats.error

    @property
    def samples(self):
        """
        Get samples from stats.

        Returns:
            list: Sample values
        """
        return self.stats.samples

    def show_total_time(self):
        """Control if the total time the job took is reported."""
        self._show_total_time = True

    @property
    def seconds(self):
        """
        Return entry's microseconds in seconds.

        Returns:
            float: Time in seconds
        """
        return self.microseconds / 1_000_000.0

    @property
    def runtime(self):
        """Alias for seconds."""
        return self.seconds

    @property
    def error_percentage(self):
        """
        Return entry's standard deviation of iteration per second in percentage.

        Returns:
            float: Error percentage
        """
        return self.stats.error_percentage()

    def body(self, format_type='human', max_width=20):
        """
        Return Entry body text with left padding.

        Args:
            format_type: Format type ('human' or 'raw')
            max_width: Maximum width for label

        Returns:
            str: Formatted body text
        """
        from .helpers import scale, humanize_duration

        per_iter = (" (%s/i)" % humanize_duration(1_000_000_000 / self.stats.central_tendency)).rjust(15)

        if format_type == 'human':
            left = ("%s (±%4.1f%%) i/s" % (scale(self.stats.central_tendency), self.stats.error_percentage())).ljust(20)
            iters = scale(self.iterations)

            if self._show_total_time:
                return left + per_iter + (" - %s in %10.6fs" % (iters, self.runtime))
            else:
                return left + per_iter + (" - %s" % iters)
        else:
            left = ("%10.1f (±%.1f%%) i/s" % (self.stats.central_tendency, self.stats.error_percentage())).ljust(20)

            if self._show_total_time:
                return left + per_iter + (" - %10d in %10.6fs" % (self.iterations, self.runtime))
            else:
                return left + per_iter + (" - %10d" % self.iterations)

    def header(self, max_width=20):
        """
        Return header with padding.

        Args:
            max_width: Maximum width for label

        Returns:
            str: Right justified header
        """
        return str(self.label).rjust(max_width)

    def __str__(self):
        """
        Return string representation of Entry object.

        Returns:
            str: Header and body
        """
        return f"{self.header()} {self.body()}"

    def display(self):
        """Print entry to current standard output."""
        sys.stdout.write(str(self) + "\n")


class Report:
    """Report contains benchmarking entries."""

    def __init__(self):
        """Initialize the Report."""
        self.entries = []
        self._data = None

    def add_entry(self, label, microseconds, iters, stats, measurement_cycle):
        """
        Add entry to report.

        Args:
            label: Entry label
            microseconds: Measured time in microseconds
            iters: Number of iterations
            stats: Statistical results
            measurement_cycle: Number of cycles

        Returns:
            ReportEntry: Last added entry
        """
        entry = ReportEntry(label, microseconds, iters, stats, measurement_cycle)
        # Remove any existing entry with the same label
        self.entries = [e for e in self.entries if e.label != label]
        self.entries.append(entry)
        return entry

    @property
    def data(self):
        """
        Entries data in array for generate json.

        Returns:
            list: Array of dictionaries with entry data
        """
        if self._data is None:
            self._data = [
                {
                    'name': entry.label,
                    'central_tendency': entry.stats.central_tendency,
                    'ips': entry.stats.central_tendency,  # for backwards compatibility
                    'error': entry.stats.error,
                    'stddev': entry.stats.error,  # for backwards compatibility
                    'microseconds': entry.microseconds,
                    'iterations': entry.iterations,
                    'cycles': entry.measurement_cycle,
                }
                for entry in self.entries
            ]
        return self._data

    def run_comparison(self, order='fastest'):
        """
        Run comparison of entries.

        Args:
            order: Comparison order
        """
        compare_module.compare(*self.entries, order=order)

    def generate_json(self, path):
        """
        Generate json from Report data to given path.

        Args:
            path: Path to generate json or file-like object (e.g., sys.stdout)
        """
        data = self.data

        if hasattr(path, 'write'):  # File-like object (e.g., STDOUT)
            path.write(json.dumps(data, indent=2))
        else:
            with open(path, 'w') as f:
                f.write(json.dumps(data, indent=2))
