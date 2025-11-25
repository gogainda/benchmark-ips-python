# benchmark-ips Quick Reference Cheatsheet

## Installation & Import
```python
# Add to path or install
export PYTHONPATH=/path/to/benchmark-ips:$PYTHONPATH

# Import
import benchmark_ips as bm
```

## Three Ways to Use

### 1️⃣ Context Manager (Recommended)
```python
with bm.benchmark(warmup=2, time=5) as x:
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)
    x.enable_compare()
```

### 2️⃣ Function Style
```python
def my_bench(x):
    x.report("test", lambda: 1 + 2)
    x.enable_compare()

bm.ips(my_bench, warmup=2, time=5)
```

### 3️⃣ Quick Compare
```python
bm.ips_quick('upper', 'lower', on="hello", warmup=1, time=2)
```

## Configuration

```python
# Method 1: Keyword args
x.config(warmup=2, time=5, quiet=False)

# Method 2: Dict
x.config({'warmup': 2, 'time': 5})

# Method 3: Direct
x.warmup = 2
x.time = 5
```

| Option | Default | Description |
|--------|---------|-------------|
| warmup | 2 | Warmup seconds |
| time | 5 | Benchmark seconds |
| iterations | 1 | Number of runs |
| quiet | False | Suppress output |
| stats | 'sd' | Stats model |
| confidence | 95 | Confidence % |

## Reporting

### Automatic Loop
```python
x.report("label", lambda: your_code())
```

### Manual Loop (lower overhead)
```python
def manual(times):
    for _ in range(times):
        your_code()

x.report("label", manual)
```

## Comparison

```python
# Fastest first (default)
x.enable_compare()

# First as baseline
x.enable_compare(order='baseline')
```

## Output Control

```python
# Quiet mode
x.set_quiet(True)

# JSON to file
x.enable_json('results.json')

# JSON to stdout
import sys
x.enable_json(sys.stdout)
```

## Access Results

```python
report = bm.ips(bench_func)

# Access entries
for entry in report.entries:
    print(entry.label)              # "test"
    print(entry.ips)                # 1234567.8
    print(entry.iterations)         # 123456
    print(entry.error_percentage)   # 5.2
    print(entry.seconds)            # 0.123

# Get JSON data
data = report.data  # List of dicts
```

## Common Patterns

### Before/After
```python
with bm.benchmark() as x:
    x.report("before", old_func)
    x.report("after", new_func)
    x.enable_compare(order='baseline')
```

### Multiple Implementations
```python
with bm.benchmark() as x:
    x.report("approach1", func1)
    x.report("approach2", func2)
    x.report("approach3", func3)
    x.enable_compare()
```

### Quick Method Compare
```python
obj = "hello"
bm.ips_quick('upper', 'lower', 'title', on=obj)
```

### Silent with Results
```python
def bench(x):
    x.config(quiet=True, warmup=1, time=1)
    x.report("test", lambda: func())

report = bm.ips(bench)
print(f"Result: {report.entries[0].ips:.0f} i/s")
```

## Tips

✅ **DO:**
- Use longer times for fast operations
- Setup data outside the benchmark
- Use manual loops for micro-benchmarks
- Compare similar operations

❌ **DON'T:**
- Mix fast and slow operations
- Include setup in benchmark
- Use too short warmup times
- Compare apples to oranges

## Example Output

```
Python 3.12.9 on Linux
Warming up --------------------------------------
            test1     1.423M i/100ms
            test2     1.485M i/100ms
Calculating -------------------------------------
            test1     14.459M (± 7.1%) i/s   (69.16 ns/i)
            test2     15.111M (± 4.6%) i/s   (66.18 ns/i)

Comparison:
test2: 15111110.5 i/s
test1: 14459979.2 i/s - 1.04x slower
```

## Need More Help?

- 📖 Full guide: `USAGE_GUIDE.md`
- 🧪 Examples: `examples/` directory
- 🎯 Demo: `python demo.py`
- ✅ Tests: `pytest tests/`
