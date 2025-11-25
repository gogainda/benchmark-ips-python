# Examples

This directory contains various examples demonstrating benchmark-ips usage.

## Quick Start Examples

### `simple.py`
Basic benchmark comparing different operations (addition, string operations, etc.)
```bash
python3 examples/simple.py
```

### `quick.py`
Quick comparison API using `ips_quick()` for rapid benchmarking
```bash
python3 examples/quick.py
```

### `context_manager.py`
Context manager style benchmarking
```bash
python3 examples/context_manager.py
```

## Comprehensive Examples

### `demo.py`
Interactive 7-part demonstration covering:
- Basic benchmarking
- String operations
- List comprehensions
- Quick comparison API
- Manual iteration control
- Quiet mode & programmatic access
- Baseline comparison

```bash
python3 examples/demo.py
```

### `fast_vs_slow.py`
Comprehensive performance comparison showing dramatic differences:
- String building (join vs concatenation)
- List vs set membership (1190x faster!)
- Sorting algorithms
- Built-in vs manual implementations

```bash
python3 examples/fast_vs_slow.py
```

### `slow_vs_fast_demo.py`
Detailed slow vs fast code demonstrations with explanations

```bash
python3 examples/slow_vs_fast_demo.py
```

## Python Idioms Benchmark

### `python_idioms_benchmark.py` ⭐
Comprehensive benchmark comparing Python idioms (inspired by fast-ruby benchmarks):

- **Exception Handling**: hasattr vs try/except
- **Iteration**: List comprehension vs map vs for loop
- **List Operations**: List vs set membership (1190x difference!)
- **Dict Operations**: Direct access vs get(), dict literal vs dict()
- **String Operations**: Concatenation methods, string building, case comparison
- **Function Calls**: Direct call vs unpacking, attribute access
- **Sorting**: sorted()[:1] vs min(), reverse sorting methods
- **Filtering**: filter() vs list comprehension

```bash
python3 examples/python_idioms_benchmark.py
```

**Key findings:**
- Set membership is 1190x faster than list membership for large collections
- List comprehensions are ~3x faster than map() for simple operations
- `''.join()` is 7.4x faster than loop with `+=` for string building
- `random.choice()` is 563x faster than `shuffle().copy()[0]`
- Generator expressions are 3.45x faster than filter() for first-match
- Direct attribute access and getattr() have similar performance
- `dict | dict` (Python 3.9+) is fastest for dict merging

## Starter Template

### `my_first_benchmark.py`
Simple template to get started with your own benchmarks
```bash
python3 examples/my_first_benchmark.py
```

## Running from Examples Directory

All examples include path handling and can be run directly from the examples/ directory:

```bash
cd examples
python3 simple.py
python3 python_idioms_benchmark.py
./fast_vs_slow.py  # All .py files are executable
```

## Tips

- Use `warmup=1, time=2` for quick testing
- Use `warmup=2, time=5` (default) for accurate results
- Add `quiet=True` to suppress output and access results programmatically
- Use `x.enable_compare()` to see relative performance differences
