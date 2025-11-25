# Translation Notes: Ruby benchmark-ips to Python

## Overview

This document describes the translation of the Ruby `benchmark-ips` gem to Python.

## Project Structure

```
benchmark_ips/
├── __init__.py           # Main module with ips() and ips_quick() functions
├── timing.py             # Timing utilities and statistics
├── compare.py            # Comparison functionality
├── helpers.py            # Helper functions for formatting
├── job.py                # Job class for managing benchmarks
├── job_entry.py          # Entry class for individual benchmark items
├── report.py             # Report and ReportEntry classes
└── stats/
    ├── __init__.py
    ├── stats_metric.py   # Base stats interface
    └── sd.py             # Standard deviation implementation

tests/
└── test_benchmark_ips.py # Comprehensive test suite

examples/
├── simple.py             # Basic usage example
├── quick.py              # ips_quick() example
└── context_manager.py    # Context manager usage
```

## Key Translation Decisions

### 1. Blocks vs Lambdas
**Ruby:** Uses blocks with `do...end` or `{...}`
```ruby
x.report("test") { 1 + 2 }
```

**Python:** Uses lambda functions or regular functions
```python
x.report("test", lambda: 1 + 2)
```

### 2. Method Names
**Ruby:** Uses `!` suffix for methods with side effects
```ruby
x.compare!
x.hold!('results.json')
```

**Python:** Uses descriptive names without special characters
```python
x.enable_compare()
x.hold('results.json')
```

### 3. Configuration
**Ruby:** Supports both hash and method syntax
```ruby
x.config(time: 5, warmup: 2)
x.time = 5
```

**Python:** Supports both dict and keyword arguments
```python
x.config(time=5, warmup=2)
x.config({'time': 5, 'warmup': 2})
x.time = 5
```

### 4. Context Manager (Python Addition)
Python version adds context manager support for more Pythonic usage:
```python
with benchmark(warmup=1, time=2) as x:
    x.report("test", lambda: 1 + 2)
    x.enable_compare()
```

### 5. Timing Implementation
**Ruby:** Uses `Process.clock_gettime` with `CLOCK_MONOTONIC`
**Python:** Uses `time.perf_counter()` which provides similar monotonic timing

### 6. Statistics
Currently implements:
- **SD (Standard Deviation)**: Fully implemented
- **Bootstrap**: Placeholder (would require kalibera package equivalent)

## API Compatibility

### Main Functions

| Ruby | Python | Notes |
|------|--------|-------|
| `Benchmark.ips` | `benchmark_ips.ips()` | Identical API |
| `Benchmark.ips_quick` | `benchmark_ips.ips_quick()` | Identical API |
| `x.report(label, &block)` | `x.report(label, callable)` | Uses callable instead of block |
| `x.config(opts)` | `x.config(opts)` or `x.config(**kwargs)` | Enhanced with kwargs |
| `x.compare!` | `x.enable_compare()` | Renamed for Python conventions |
| `x.hold!(path)` | `x.hold(path)` | Renamed |
| `x.save!(path)` | `x.save(path)` | Renamed |
| `x.json!(path)` | `x.enable_json(path)` | Renamed |

### Configuration Options

All configuration options are preserved:
- `warmup`: Warmup time in seconds (default: 2)
- `time`: Calculation time in seconds (default: 5)
- `iterations`: Number of iterations (default: 1)
- `stats`: Statistical model (default: 'sd')
- `confidence`: Confidence level (default: 95)
- `quiet`: Suppress output (default: False)

## Testing

All tests from the original Ruby test suite have been translated to pytest:
- 18 test cases covering all major functionality
- All tests passing
- Uses pytest fixtures for output capture

Run tests with:
```bash
pytest tests/
```

## Examples

### Basic Usage
```python
import benchmark_ips as bm

def my_benchmark(x):
    x.config(warmup=2, time=5)
    x.report("addition", lambda: 1 + 2)
    x.report("multiplication", lambda: 2 * 3)
    x.enable_compare()

bm.ips(my_benchmark)
```

### Quick Comparison
```python
import benchmark_ips as bm

bm.ips_quick('upper', 'lower', on="hello", warmup=1, time=2)
```

### Context Manager
```python
import benchmark_ips as bm

with bm.benchmark(warmup=1, time=2) as x:
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)
    x.enable_compare()
```

## Differences from Ruby Version

1. **No string evaluation by default**: For security, string code evaluation is supported but not recommended
2. **Context managers**: Python-specific feature for cleaner resource management
3. **Type hints**: Could be added in future for better IDE support
4. **No GC.disable**: Python's GC API is different; uses `gc.collect()` instead
5. **Bootstrap stats**: Not yet implemented (would need Python equivalent of kalibera gem)

## Dependencies

**Runtime:** None (pure Python)
**Development:**
- pytest >= 7.0.0
- pytest-cov >= 3.0.0

## Installation

```bash
pip install benchmark-ips
```

Or for development:
```bash
git clone <repo>
cd benchmark-ips
pip install -e .
pip install -r requirements-dev.txt
```

## Python Version Support

- Python 3.7+
- Tested on Python 3.12

## Performance Characteristics

The Python port maintains the same algorithmic approach as the Ruby version:
1. Adaptive warmup to determine optimal cycle count
2. Multiple sampling runs during calculation phase
3. Statistical analysis with standard deviation
4. Comparison with error margins

Expected overhead is minimal and comparable to the Ruby version.

## Future Enhancements

Potential improvements:
1. Bootstrap confidence intervals (requires additional library)
2. Type hints throughout codebase
3. Async/await support for async code benchmarking
4. Additional output formats (CSV, HTML)
5. Integration with profiling tools
6. Multi-process benchmarking support

## License

MIT License (same as original Ruby version)

## Credits

- Original Ruby implementation: Evan Phoenix and contributors
- Python port: Translated using Claude AI (2025)
