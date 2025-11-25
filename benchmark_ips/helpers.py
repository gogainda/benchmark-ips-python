"""Helper functions for formatting output."""

import math


SUFFIXES = ['', 'k', 'M', 'B', 'T', 'Q']


def scale(value):
    """
    Scale a value and add appropriate suffix.

    Args:
        value: Value to scale

    Returns:
        str: Scaled value with suffix
    """
    if value == 0:
        return "%10.3f" % 0

    scale_factor = int(math.log10(value) / 3)
    if scale_factor < 0 or scale_factor >= len(SUFFIXES):
        scale_factor = 0

    suffix = SUFFIXES[scale_factor]
    scaled_value = value / (1000 ** scale_factor)

    return "%10.3f%s" % (scaled_value, suffix)


def humanize_duration(duration_ns):
    """
    Convert duration in nanoseconds to human-readable format.

    Args:
        duration_ns: Duration in nanoseconds

    Returns:
        str: Humanized duration string
    """
    if duration_ns < 1000:
        return "%.2f ns" % duration_ns
    elif duration_ns < 1_000_000:
        return "%.2f μs" % (duration_ns / 1000)
    elif duration_ns < 1_000_000_000:
        return "%.2f ms" % (duration_ns / 1_000_000)
    else:
        return "%.2f s" % (duration_ns / 1_000_000_000)
