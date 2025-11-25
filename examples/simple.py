"""Simple benchmark example."""

import sys
from pathlib import Path
# Add parent directory to path so examples can be run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

import benchmark_ips as bm


def simple_benchmark(x):
    """Simple benchmark comparing different operations."""
    # Configure the number of seconds used during
    # the warmup phase (default 2) and calculation phase (default 5)
    x.config(warmup=2, time=5)

    # Typical mode, runs the block as many times as it can
    x.report("addition", lambda: 1 + 2)

    # To reduce overhead, the number of iterations is passed in
    def addition_with_times(times):
        i = 0
        while i < times:
            i += 1
            1 + 2

    x.report("addition2", addition_with_times)

    # String operations
    x.report("string concat", lambda: "hello" + "world")
    x.report("string format", lambda: f"{'hello'}{'world'}")

    # Really long labels should be formatted correctly
    x.report("addition-test-long-label", lambda: 1 + 2)

    # Compare the iterations per second of the various reports!
    x.enable_compare()


if __name__ == '__main__':
    bm.ips(simple_benchmark)
