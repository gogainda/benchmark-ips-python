#!/usr/bin/env python3
"""
Interactive Demo of benchmark-ips

Run this to see how the library works!
"""

import sys
from pathlib import Path
# Add parent directory to path so examples can be run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

import benchmark_ips as bm
import time


def demo_basic():
    """Demo 1: Basic benchmarking"""
    print("=" * 60)
    print("DEMO 1: Basic Benchmarking")
    print("=" * 60)
    print("\nComparing basic arithmetic operations:\n")

    with bm.benchmark(warmup=1, time=2) as x:
        x.report("addition", lambda: 1 + 2)
        x.report("multiplication", lambda: 2 * 3)
        x.report("division", lambda: 10 / 2)
        x.report("power", lambda: 2 ** 3)
        x.enable_compare()


def demo_strings():
    """Demo 2: String operations"""
    print("\n" + "=" * 60)
    print("DEMO 2: String Operations")
    print("=" * 60)
    print("\nComparing different string concatenation methods:\n")

    text = "hello"

    with bm.benchmark(warmup=1, time=2) as x:
        x.report("+ operator", lambda: text + " world")
        x.report("f-string", lambda: f"{text} world")
        x.report("format()", lambda: "{} world".format(text))
        x.report("% operator", lambda: "%s world" % text)
        x.enable_compare()


def demo_lists():
    """Demo 3: List comprehensions"""
    print("\n" + "=" * 60)
    print("DEMO 3: List Comprehensions vs Map")
    print("=" * 60)
    print("\nComparing ways to double numbers in a list:\n")

    numbers = list(range(100))

    with bm.benchmark(warmup=1, time=2) as x:
        x.report("list comp", lambda: [n * 2 for n in numbers])
        x.report("map", lambda: list(map(lambda n: n * 2, numbers)))
        x.report("for loop", lambda: [x * 2 for x in numbers])
        x.enable_compare()


def demo_quick():
    """Demo 4: Quick comparison"""
    print("\n" + "=" * 60)
    print("DEMO 4: Quick Comparison API")
    print("=" * 60)
    print("\nQuick comparison of string methods:\n")

    bm.ips_quick('upper', 'lower', 'title',
                 on="hello world",
                 warmup=1, time=2)


def demo_manual():
    """Demo 5: Manual iteration control"""
    print("\n" + "=" * 60)
    print("DEMO 5: Manual Iteration Control")
    print("=" * 60)
    print("\nFor very fast operations, manual control reduces overhead:\n")

    with bm.benchmark(warmup=1, time=2) as x:
        # Automatic - library handles loop
        x.report("automatic", lambda: 1 + 2)

        # Manual - you handle loop (lower overhead)
        def manual(times):
            i = 0
            while i < times:
                1 + 2
                i += 1

        x.report("manual loop", manual)
        x.enable_compare()


def demo_quiet():
    """Demo 6: Quiet mode with programmatic access"""
    print("\n" + "=" * 60)
    print("DEMO 6: Quiet Mode & Programmatic Access")
    print("=" * 60)
    print("\nRunning benchmark in quiet mode...\n")

    def bench(x):
        x.config(warmup=1, time=1, quiet=True)
        x.report("operation1", lambda: sum(range(100)))
        x.report("operation2", lambda: [i for i in range(100)])

    report = bm.ips(bench)

    # Access results programmatically
    print("Results accessed programmatically:")
    for entry in report.entries:
        print(f"  {entry.label:15s}: {entry.ips:15,.0f} i/s")
        print(f"  {'':15s}  {entry.iterations:15,} iterations")
        print(f"  {'':15s}  ±{entry.error_percentage:13.1f}% error")
        print()


def demo_baseline():
    """Demo 7: Baseline comparison"""
    print("=" * 60)
    print("DEMO 7: Baseline Comparison")
    print("=" * 60)
    print("\nCompare optimizations against a baseline:\n")

    data = list(range(100))

    with bm.benchmark(warmup=1, time=2) as x:
        # First one is baseline
        x.report("baseline", lambda: sum(data))
        x.report("optimized v1", lambda: sum(data))
        x.report("optimized v2", lambda: sum(data))
        x.enable_compare(order='baseline')


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "benchmark-ips Python Demo" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    demos = [
        demo_basic,
        demo_strings,
        demo_lists,
        demo_quick,
        demo_manual,
        demo_quiet,
        demo_baseline,
    ]

    for i, demo_func in enumerate(demos, 1):
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\nError in demo {i}: {e}")
            continue

        # Pause between demos
        if i < len(demos):
            print("\n" + "-" * 60)
            input("Press Enter for next demo (or Ctrl+C to exit)...")

    print("\n" + "=" * 60)
    print("🎉 Demo complete!")
    print("=" * 60)
    print("\nTry it yourself:")
    print("  1. Check out examples/simple.py")
    print("  2. Read USAGE_GUIDE.md for more details")
    print("  3. Write your own benchmarks!")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled.")
