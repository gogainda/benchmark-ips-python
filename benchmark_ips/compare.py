"""Functionality for performing comparison between reports."""

import sys


def compare(*entries, order='fastest'):
    """
    Compare between reports, prints out facts of each report:
    runtime, comparative speed difference.

    Args:
        entries: Report entries to compare
        order: Comparison order - 'fastest' or 'baseline'
    """
    if len(entries) < 2:
        return

    entries = list(entries)
    max_width = max(len(str(e.label)) for e in entries)

    if order == 'baseline':
        baseline = entries.pop(0)
        sorted_entries = sorted(entries, key=lambda e: e.stats.central_tendency, reverse=True)
    elif order == 'fastest':
        sorted_entries = sorted(entries, key=lambda e: e.stats.central_tendency, reverse=True)
        baseline = sorted_entries.pop(0)
    else:
        raise ValueError(f"Unknown order: {order}")

    sys.stdout.write("\nComparison:\n")

    sys.stdout.write(f"{str(baseline.label).rjust(max_width)}: {baseline.stats.central_tendency:10.1f} i/s\n")

    for report in sorted_entries:
        name = str(report.label)

        sys.stdout.write(f"{name.rjust(max_width)}: {report.stats.central_tendency:10.1f} i/s - ")

        if report.stats.overlaps(baseline.stats):
            sys.stdout.write("same-ish: difference falls within error")
        elif report.stats.central_tendency > baseline.stats.central_tendency:
            speedup, error = report.stats.speedup(baseline.stats)
            sys.stdout.write(f"{speedup:.2f}x ")
            if error is not None:
                sys.stdout.write(f" (± {error:.2f})")
            sys.stdout.write(" faster")
        else:
            slowdown, error = report.stats.slowdown(baseline.stats)
            sys.stdout.write(f"{slowdown:.2f}x ")
            if error is not None:
                sys.stdout.write(f" (± {error:.2f})")
            sys.stdout.write(" slower")

        sys.stdout.write("\n")

    footer = baseline.stats.footer()
    if footer:
        sys.stdout.write(footer.rjust(40) + "\n")

    sys.stdout.write("\n")
