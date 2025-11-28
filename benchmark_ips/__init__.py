"""
benchmark-ips: Iterations per second benchmarking for Python.

A Python port of the Ruby benchmark-ips library.
"""

import sys
import os
from .job import Job
from .report import Report
from . import compare as compare_module


__version__ = "2.14.1"
__codename__ = "Akagi"


# Global options
_options = {'format': 'human'}


def get_options():
    """
    Get benchmark options.

    Returns:
        dict: Options dictionary
    """
    return _options


def ips(*args, **kwargs):
    """
    Measure code in block, each code's benchmarked result will display in
    iteration per second with standard deviation in given time.

    Args:
        time: Specify how long should benchmark your code in seconds
        warmup: Specify how long should Warmup time run in seconds
        quiet: Suppress output
        **kwargs: Additional options

    Returns:
        Report: Benchmark report

    Example:
        >>> import benchmark_ips as bm
        >>> def my_benchmark(x):
        ...     x.config(time=5, warmup=2)
        ...     x.report("addition", lambda: 1 + 2)
        ...     x.compare()
        >>> report = bm.ips(my_benchmark)
    """
    # Handle both positional and keyword arguments
    if args and callable(args[0]):
        # First argument is the block function
        block = args[0]
        args = args[1:]
    elif 'block' in kwargs:
        block = kwargs.pop('block')
    else:
        block = None

    # Parse remaining arguments
    if args and isinstance(args[0], dict):
        time = args[0].get('time')
        warmup = args[0].get('warmup')
        quiet = args[0].get('quiet')
    else:
        time = kwargs.get('time')
        warmup = kwargs.get('warmup')
        quiet = kwargs.get('quiet')

        if len(args) >= 1 and not isinstance(args[0], dict):
            time = args[0]
        if len(args) >= 2:
            warmup = args[1]
        if len(args) >= 3:
            quiet = args[2]

    # Store original stdout sync state (not applicable in Python, but keep for API compatibility)
    job = Job()

    job_opts = {}
    if time is not None:
        job_opts['time'] = time
    if warmup is not None:
        job_opts['warmup'] = warmup
    if quiet is not None:
        job_opts['quiet'] = quiet

    job.config(job_opts)

    # If block is provided, call it with the job
    if block:
        block(job)

    # Otherwise, return job for use with context manager
    else:
        return job

    job.load_held_results()
    job.run()

    if job.is_run_single() and job.all_results_have_been_run():
        job.clear_held_results()
    else:
        job.save_held_results()
        if job.is_run_single():
            print('\nPausing here -- run Python again to measure the next benchmark...')

    job.run_comparison()
    job.generate_json()

    report = job.full_report

    # Handle SHARE environment variable
    if os.environ.get('SHARE') or os.environ.get('SHARE_URL'):
        try:
            from .share import Share
            share = Share(report, job)
            share.share()
        except ImportError:
            print("Warning: Share functionality not implemented")

    return report


def ips_quick(*methods, on=None, **opts):
    """
    Quickly compare multiple methods on the same object.

    Args:
        *methods: Method names to compare
        on: Object on which to call the methods
        **opts: Additional options for customizing the benchmark

    Returns:
        Report: Benchmark report

    Example:
        >>> import benchmark_ips as bm
        >>> bm.ips_quick('upper', 'lower', on="hello", warmup=1, time=1)
    """
    def benchmark_block(x):
        x.enable_compare()

        for name in methods:
            if on is not None:
                # Call method on the object
                method = getattr(on, name)
                x.report(name, lambda times: [method() for _ in range(times)])
            else:
                # Assume it's a function in the caller's scope
                # This is tricky in Python, so we'll use eval
                import inspect
                frame = inspect.currentframe().f_back.f_back
                func = frame.f_locals.get(name) or frame.f_globals.get(name)
                if func:
                    x.report(name, lambda times, f=func: [f() for _ in range(times)])

    return ips(benchmark_block, **opts)


def compare(*entries, order='fastest'):
    """
    Compare benchmark entries.

    Args:
        *entries: Report entries to compare
        order: Comparison order

    Example:
        >>> import benchmark_ips as bm
        >>> # entries from a report
        >>> bm.compare(*report.entries)
    """
    return compare_module.compare(*entries, order=order)


class BenchmarkContext:
    """Context manager for benchmark-ips."""

    def __init__(self, job):
        """
        Initialize context.

        Args:
            job: Job instance
        """
        self.job = job

    def __enter__(self):
        """Enter context."""
        return self.job

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and run benchmark."""
        if exc_type is None:
            self.job.load_held_results()
            self.job.run()

            if self.job.is_run_single() and self.job.all_results_have_been_run():
                self.job.clear_held_results()
            else:
                self.job.save_held_results()
                if self.job.is_run_single():
                    print('\nPausing here -- run Python again to measure the next benchmark...')

            self.job.run_comparison()
            self.job.generate_json()
        return False


def benchmark(**opts):
    """
    Create a benchmark context manager.

    Args:
        **opts: Benchmark options

    Returns:
        BenchmarkContext: Context manager

    Example:
        >>> import benchmark_ips as bm
        >>> with bm.benchmark(time=1, warmup=1) as x:
        ...     x.report("test", lambda: 1 + 2)
        ...     x.enable_compare()
    """
    job = Job()
    job.config(opts)
    return BenchmarkContext(job)


__all__ = [
    'ips',
    'ips_quick',
    'compare',
    'benchmark',
    'get_options',
    '__version__',
    '__codename__',
]
