# Complete Usage Guide: benchmark-ips (Python)

## Installation

```bash
# From the project directory
pip install -e .

# Or just add to PYTHONPATH
export PYTHONPATH=/path/to/benchmark-ips:$PYTHONPATH
```

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Configuration Options](#configuration-options)
3. [Advanced Features](#advanced-features)
4. [Real-World Examples](#real-world-examples)
5. [Best Practices](#best-practices)

---

## Basic Usage

### Method 1: Function-Based API

```python
import benchmark_ips as bm

def my_benchmark(x):
    # Add benchmarks
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)

    # Enable comparison
    x.enable_compare()

# Run it
report = bm.ips(my_benchmark)
```

### Method 2: Context Manager (Recommended)

```python
import benchmark_ips as bm

with bm.benchmark(warmup=2, time=5) as x:
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)
    x.enable_compare()
```

### Method 3: Quick Comparison

```python
import benchmark_ips as bm

# Compare methods on an object
bm.ips_quick('upper', 'lower', 'title',
             on="hello world",
             warmup=1, time=2)
```

---

## Configuration Options

### Setting Configuration

You can configure benchmarks in three ways:

#### 1. Via config() method with keyword arguments
```python
def bench(x):
    x.config(warmup=2, time=5, quiet=False)
    x.report("test", lambda: 1 + 2)

bm.ips(bench)
```

#### 2. Via config() method with dict
```python
def bench(x):
    x.config({'warmup': 2, 'time': 5, 'quiet': False})
    x.report("test", lambda: 1 + 2)

bm.ips(bench)
```

#### 3. Via direct attributes
```python
def bench(x):
    x.warmup = 2
    x.time = 5
    x.report("test", lambda: 1 + 2)

bm.ips(bench)
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `warmup` | int/float | 2 | Warmup time in seconds |
| `time` | int/float | 5 | Calculation time in seconds |
| `iterations` | int | 1 | Number of warmup/calculation iterations |
| `quiet` | bool | False | Suppress output |
| `stats` | str | 'sd' | Statistical model ('sd' for standard deviation) |
| `confidence` | int | 95 | Confidence level for statistics |

### Examples

```python
# Quick benchmark (1 second total)
with bm.benchmark(warmup=0.5, time=0.5) as x:
    x.report("fast", lambda: sum(range(100)))

# Thorough benchmark (20 seconds total)
with bm.benchmark(warmup=5, time=15) as x:
    x.report("thorough", lambda: sum(range(1000)))

# Silent benchmark (no output)
def bench(x):
    x.config(warmup=1, time=1, quiet=True)
    x.report("silent", lambda: 1 + 2)

report = bm.ips(bench)
print(f"Result: {report.entries[0].ips:.0f} i/s")
```

---

## Advanced Features

### 1. Manual Iteration Control

For very fast operations, you can manually handle iterations to reduce overhead:

```python
def bench(x):
    # Automatic loop (library handles iterations)
    x.report("auto", lambda: 1 + 2)

    # Manual loop (you handle iterations)
    def manual(times):
        i = 0
        while i < times:
            1 + 2  # Your code here
            i += 1

    x.report("manual", manual)
    x.enable_compare()

bm.ips(bench, warmup=1, time=2)
```

### 2. Comparison Modes

#### Fastest First (Default)
```python
def bench(x):
    x.report("slow", lambda: sum(range(1000)))
    x.report("fast", lambda: sum(range(100)))
    x.enable_compare()  # Fastest will be baseline

bm.ips(bench, warmup=1, time=2)
```

#### Baseline Comparison
```python
def bench(x):
    x.report("baseline", lambda: sum(range(100)))
    x.report("optimized", lambda: sum(range(100)))
    x.enable_compare(order='baseline')  # First one is baseline

bm.ips(bench, warmup=1, time=2)
```

### 3. JSON Output

#### To File
```python
def bench(x):
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)
    x.enable_json('results.json')

bm.ips(bench, warmup=1, time=1)
```

#### To STDOUT
```python
import sys

def bench(x):
    x.report("test", lambda: 1 + 2)
    x.set_quiet(True)  # Don't print normal output
    x.enable_json(sys.stdout)

bm.ips(bench, warmup=1, time=1)
```

### 4. Hold Results (Multi-Run Benchmarks)

For comparing different implementations across multiple Python invocations:

```python
# First run - benchmarks item 1
def bench(x):
    x.hold('results.json')
    x.report("implementation_v1", lambda: old_code())
    x.report("implementation_v2", lambda: new_code())

bm.ips(bench, warmup=2, time=5)
# Output: "Pausing here -- run Python again to measure the next benchmark..."

# Second run - benchmarks item 2 and shows comparison
# (Run the same script again)
```

---

## Real-World Examples

### Example 1: String Manipulation

```python
import benchmark_ips as bm

text = "hello world " * 100

with bm.benchmark(warmup=2, time=3) as x:
    # Different string concatenation methods
    x.report("+ operator", lambda: text + "!")
    x.report("format()", lambda: "{}!".format(text))
    x.report("f-string", lambda: f"{text}!")
    x.report("join", lambda: "".join([text, "!"]))
    x.enable_compare()
```

### Example 2: List Operations

```python
import benchmark_ips as bm

data = list(range(1000))

with bm.benchmark(warmup=2, time=3) as x:
    # Different ways to double values
    x.report("list comp", lambda: [i * 2 for i in data])
    x.report("map", lambda: list(map(lambda i: i * 2, data)))
    x.report("for loop", lambda: [x * 2 for x in data])
    x.enable_compare()
```

### Example 3: Dictionary Lookups

```python
import benchmark_ips as bm

# Create test data
small_dict = {str(i): i for i in range(10)}
large_dict = {str(i): i for i in range(10000)}

with bm.benchmark(warmup=1, time=2) as x:
    x.report("small dict lookup", lambda: small_dict.get("5"))
    x.report("large dict lookup", lambda: large_dict.get("5000"))
    x.report("small dict in", lambda: "5" in small_dict)
    x.report("large dict in", lambda: "5000" in large_dict)
    x.enable_compare()
```

### Example 4: JSON Serialization

```python
import benchmark_ips as bm
import json

data = {
    'name': 'Test',
    'values': list(range(100)),
    'nested': {'a': 1, 'b': 2}
}

with bm.benchmark(warmup=2, time=3) as x:
    x.report("json.dumps", lambda: json.dumps(data))
    x.report("json.dumps compact",
             lambda: json.dumps(data, separators=(',', ':')))
    x.enable_compare()
```

### Example 5: File Operations

```python
import benchmark_ips as bm
import tempfile
import os

# Create test file
test_file = tempfile.mktemp()
with open(test_file, 'w') as f:
    f.write("test data\n" * 1000)

try:
    with bm.benchmark(warmup=1, time=2) as x:
        x.report("read all",
                 lambda: open(test_file).read())
        x.report("read lines",
                 lambda: open(test_file).readlines())
        x.report("with open",
                 lambda: [line for line in open(test_file)])
        x.enable_compare()
finally:
    os.remove(test_file)
```

### Example 6: Algorithm Comparison

```python
import benchmark_ips as bm

def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

data = list(range(50, 0, -1))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("bubble_sort", lambda: bubble_sort(data))
    x.report("quick_sort", lambda: quick_sort(data))
    x.report("built-in sorted", lambda: sorted(data))
    x.enable_compare()
```

---

## Best Practices

### 1. Choose Appropriate Timing

```python
# Fast operations (< 1ms): Use longer times
with bm.benchmark(warmup=3, time=10) as x:
    x.report("very fast", lambda: 1 + 2)

# Slow operations (> 100ms): Use shorter times
with bm.benchmark(warmup=0.5, time=2) as x:
    x.report("slow", lambda: time.sleep(0.1))
```

### 2. Avoid Setup in Benchmark

❌ **Bad:** Setup inside benchmark
```python
x.report("bad", lambda: sorted(list(range(1000, 0, -1))))
```

✅ **Good:** Setup outside
```python
data = list(range(1000, 0, -1))
x.report("good", lambda: sorted(data))
```

### 3. Use Manual Loops for Micro-Benchmarks

For operations faster than 1 microsecond:

```python
def bench(x):
    # Manual iteration reduces overhead
    def manual(times):
        i = 0
        while i < times:
            1 + 2  # Micro-operation
            i += 1

    x.report("micro", manual)

bm.ips(bench, warmup=2, time=5)
```

### 4. Warm Up Your Code

```python
# Good practice: explicit warmup
data = expensive_setup()

with bm.benchmark(warmup=3, time=5) as x:
    x.report("after warmup", lambda: process(data))
```

### 5. Multiple Runs for Consistency

```python
with bm.benchmark(warmup=2, time=5, iterations=3) as x:
    x.report("test", lambda: my_function())
    # Will run: 3x warmup + 3x calculation
```

### 6. Compare Similar Operations

✅ **Good:** Fair comparison
```python
with bm.benchmark() as x:
    x.report("dict.get", lambda: d.get('key'))
    x.report("dict[]", lambda: d['key'])
    x.enable_compare()
```

❌ **Bad:** Unfair comparison
```python
with bm.benchmark() as x:
    x.report("simple", lambda: 1 + 2)
    x.report("complex", lambda: time.sleep(1))
    x.enable_compare()  # Not comparable!
```

---

## Common Patterns

### Pattern 1: Before/After Optimization

```python
def old_implementation():
    return sum([i**2 for i in range(1000)])

def new_implementation():
    return sum(i**2 for i in range(1000))

with bm.benchmark(warmup=2, time=5) as x:
    x.report("old (list comp)", old_implementation)
    x.report("new (generator)", new_implementation)
    x.enable_compare(order='baseline')
```

### Pattern 2: Parameter Sweep

```python
def benchmark_sizes():
    sizes = [10, 100, 1000, 10000]

    for size in sizes:
        data = list(range(size))

        with bm.benchmark(warmup=1, time=2) as x:
            x.report(f"size_{size}", lambda: sorted(data))

        print()  # Separate runs
```

### Pattern 3: Conditional Benchmarking

```python
import sys

def bench(x):
    x.report("test", lambda: my_function())

    # Only compare if requested
    if '--compare' in sys.argv:
        x.enable_compare()

    # Only output JSON if requested
    if '--json' in sys.argv:
        x.enable_json('output.json')

bm.ips(bench, warmup=1, time=2)
```

---

## Troubleshooting

### Issue: Benchmark too fast, results vary wildly

**Solution:** Increase warmup and time
```python
with bm.benchmark(warmup=5, time=15) as x:
    x.report("fast op", lambda: 1 + 2)
```

### Issue: Benchmark too slow

**Solution:** Reduce time
```python
with bm.benchmark(warmup=0.5, time=1) as x:
    x.report("slow op", lambda: time.sleep(0.1))
```

### Issue: Need programmatic access to results

**Solution:** Use the returned report
```python
def bench(x):
    x.config(quiet=True)
    x.report("test", lambda: 1 + 2)

report = bm.ips(bench, warmup=1, time=1)

for entry in report.entries:
    print(f"{entry.label}: {entry.ips:.0f} i/s")
    print(f"  Iterations: {entry.iterations}")
    print(f"  Error: ±{entry.error_percentage:.1f}%")
```

### Issue: Want to save results for later analysis

**Solution:** Use JSON output
```python
def bench(x):
    x.report("test1", lambda: func1())
    x.report("test2", lambda: func2())
    x.enable_json('results.json')

bm.ips(bench)

# Later, analyze results
import json
with open('results.json') as f:
    data = json.load(f)
    for entry in data:
        print(f"{entry['name']}: {entry['ips']:.0f} i/s")
```

---

## Quick Reference

### Import
```python
import benchmark_ips as bm
```

### Basic Benchmark
```python
with bm.benchmark() as x:
    x.report("test", lambda: 1 + 2)
```

### Configure
```python
x.config(warmup=2, time=5, quiet=False)
x.warmup = 2  # Alternative
```

### Report
```python
x.report("label", lambda: code())
x.report("manual", lambda times: [code() for _ in range(times)])
```

### Compare
```python
x.enable_compare()  # Fastest first
x.enable_compare(order='baseline')  # First as baseline
```

### Output
```python
x.set_quiet(True)  # Suppress console
x.enable_json('file.json')  # JSON to file
x.enable_json(sys.stdout)  # JSON to stdout
```

### Results
```python
report = bm.ips(bench)
report.entries[0].label        # "test"
report.entries[0].ips          # 1234567.8
report.entries[0].iterations   # 123456
report.entries[0].error_percentage  # 5.2
report.data                    # List of dicts for JSON
```

---

## Summary

**Basic Usage:**
```python
import benchmark_ips as bm

with bm.benchmark(warmup=2, time=5) as x:
    x.report("my code", lambda: my_function())
    x.enable_compare()
```

**That's it!** The library handles:
- ✅ Adaptive warmup
- ✅ Automatic cycle counting
- ✅ Statistical analysis
- ✅ Formatted output
- ✅ Comparison with error margins

For more examples, check the `examples/` directory!
