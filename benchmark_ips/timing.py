"""Timing utilities for benchmarking."""

import gc
import time
import statistics


MICROSECONDS_PER_SECOND = 1_000_000


def mean(samples):
    """
    Calculate (arithmetic) mean of given samples.

    Args:
        samples: List of samples to calculate mean

    Returns:
        float: Mean of given samples
    """
    return statistics.mean(samples)


def variance(samples, m=None):
    """
    Calculate variance of given samples.

    Args:
        samples: List of samples
        m: Optional mean (Expected value)

    Returns:
        float: Variance of given samples
    """
    if m is None:
        m = mean(samples)

    total = sum((i - m) ** 2 for i in samples)
    return total / len(samples)


def stddev(samples, m=None):
    """
    Calculate standard deviation of given samples.

    Args:
        samples: List of samples to calculate standard deviation
        m: Optional mean (Expected value)

    Returns:
        float: Standard deviation of given samples
    """
    return variance(samples, m) ** 0.5


def clean_env():
    """Recycle used objects by running Garbage Collector."""
    gc.collect()


def now():
    """
    Get current time in microseconds using monotonic clock.

    Returns:
        float: Current time in microseconds
    """
    return time.perf_counter() * MICROSECONDS_PER_SECOND


def add_second(t, s):
    """
    Add seconds to time representation.

    Args:
        t: Time in microseconds
        s: Seconds to add

    Returns:
        float: New time in microseconds
    """
    return t + (s * MICROSECONDS_PER_SECOND)


def time_us(before, after):
    """
    Return the number of microseconds between the 2 moments.

    Args:
        before: Earlier time in microseconds
        after: Later time in microseconds

    Returns:
        float: Time difference in microseconds
    """
    return after - before
