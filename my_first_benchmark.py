#!/usr/bin/env python3
"""Your first benchmark - try running this!"""

import benchmark_ips as bm

# Example 1: Compare string operations
print("Example 1: String Operations")
print("-" * 50)

with bm.benchmark(warmup=1, time=2) as x:
    x.report("concatenation", lambda: "hello" + " " + "world")
    x.report("f-string", lambda: f"hello world")
    x.report("format", lambda: "{} {}".format("hello", "world"))
    x.enable_compare()

print("\n")

# Example 2: Compare list operations
print("Example 2: List Operations")
print("-" * 50)

numbers = list(range(100))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("list comp", lambda: [n * 2 for n in numbers])
    x.report("map", lambda: list(map(lambda n: n * 2, numbers)))
    x.enable_compare()

print("\n✅ Try modifying this file to benchmark your own code!")
