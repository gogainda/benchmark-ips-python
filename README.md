# benchmark-ips

**Iterations per second benchmarking for Python**

[![Tests](https://img.shields.io/badge/tests-18%20passing-brightgreen)](#testing)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE_PYTHON)

A Python port of the Ruby [benchmark-ips](https://github.com/evanphx/benchmark-ips) gem by Evan Phoenix.

**Python Port:** Igor Goncharov <igor@igorstechnoclub.com>

## Description

An iterations per second enhancement for benchmarking. For short snippets of code, ips automatically figures out how many times to run the code to get interesting data. No more guessing at random iteration counts!

## Installation

```bash
pip install benchmark-ips
```

Or for development:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

## Synopsis

```python
import benchmark_ips as bm

def my_benchmark(x):
    # Configure the number of seconds used during
    # the warmup phase (default 2) and calculation phase (default 5)
    x.config(warmup=2, time=5)

    # Typical mode, runs the block as many times as it can
    x.report("addition", lambda: 1 + 2)

    # To reduce overhead, the number of iterations is passed in
    # and the block must run the code the specific number of times.
    # Used for when the workload is very small and any overhead
    # introduces significant errors.
    def addition2(times):
        i = 0
        while i < times:
            i += 1
            1 + 2

    x.report("addition2", addition2)

    # Really long labels should be formatted correctly
    x.report("addition-test-long-label", lambda: 1 + 2)

    # Compare the iterations per second of the various reports!
    x.enable_compare()

bm.ips(my_benchmark)
```

This will generate the following report:

```
Python 3.11.0 on Linux
Warming up --------------------------------------
            addition      3.572M i/100ms
           addition2      3.672M i/100ms
addition-test-long-label
                          3.511M i/100ms
Calculating -------------------------------------
            addition     36.209M (± 2.8%) i/s   (27.62 ns/i) -    182.253M
           addition2     36.552M (± 7.8%) i/s   (27.36 ns/i) -    183.541M
addition-test-long-label
                         36.164M (± 5.8%) i/s   (27.65 ns/i) -    181.312M

Comparison:
           addition2: 36558904.5 i/s
addition-test-long-label: 36135428.8 i/s - same-ish: difference falls within error
            addition: 34666931.3 i/s - same-ish: difference falls within error
```

### Using Context Manager

You can also use a context manager style:

```python
import benchmark_ips as bm

with bm.benchmark(warmup=2, time=5) as x:
    x.report("addition", lambda: 1 + 2)
    x.report("multiplication", lambda: 2 * 3)
    x.enable_compare()
```

### Quick Comparison

Use `ips_quick` to save a few lines of code:

```python
import benchmark_ips as bm

# Runs a suite comparing "hello".upper() and "hello".lower()
bm.ips_quick('upper', 'lower', on="hello", warmup=1, time=2)
```

This adds a very small amount of overhead, which may be significant if you're microbenchmarking things that can do over 1 million iterations per second. In that case, you're better off using the full format.

## Features

### Configuration Options

- `warmup`: Warmup time in seconds (default: 2)
- `time`: Calculation time in seconds (default: 5)
- `iterations`: Number of warmup and calculation iterations (default: 1)
- `stats`: Statistical model to use (default: 'sd' for standard deviation)
- `confidence`: Confidence level for statistics (default: 95)
- `quiet`: Suppress output (default: False)

### Hold and Save Results

Hold results between multiple invocations of Python:

```python
def my_benchmark(x):
    x.hold('results.json')
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)

bm.ips(my_benchmark, time=1, warmup=1)
```

This will run only one benchmark each time you run the command, storing results in the specified file. The file is deleted when all results have been gathered and the report is shown.

### JSON Output

Generate output in JSON format:

```python
def my_benchmark(x):
    x.report("some report", lambda: 1 + 2)
    x.enable_json('results.json')

bm.ips(my_benchmark)
```

Or to stdout:

```python
import sys

def my_benchmark(x):
    x.report("some report", lambda: 1 + 2)
    x.set_quiet(True)
    x.enable_json(sys.stdout)

bm.ips(my_benchmark)
```

### Comparison Modes

Compare results with different ordering:

```python
def my_benchmark(x):
    x.report("test1", lambda: 1 + 2)
    x.report("test2", lambda: 2 * 3)
    x.enable_compare(order='baseline')  # or 'fastest' (default)

bm.ips(my_benchmark)
```

## Running Tests

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=benchmark_ips tests/
```

## Differences from Ruby Version

This Python port maintains API compatibility with the Ruby version where possible, with these differences:

1. **Lambda functions** instead of blocks: Python uses `lambda` or regular functions instead of Ruby blocks
2. **Context managers**: Python version adds support for `with` statement
3. **Method names**: Some Ruby methods use underscores (e.g., `enable_compare` instead of `compare!`)
4. **No string evaluation by default**: For security, string code evaluation is supported but not recommended

## Requirements

- Python 3.7 or higher
- No external dependencies for basic functionality

## License

MIT License

This Python port maintains the same MIT License as the original Ruby implementation to ensure maximum compatibility and freedom of use.

- **Original Ruby version:** Copyright (c) 2015 Evan Phoenix
- **Python port:** Copyright (c) 2025 Python Port Contributors

See `LICENSE_PYTHON` for full license text.

## Credits and Attribution

This is a **Python port** of the excellent [benchmark-ips Ruby gem](https://github.com/evanphx/benchmark-ips) created by **Evan Phoenix**.

### Original Work
- **Author:** Evan Phoenix
- **Project:** benchmark-ips (Ruby gem)
- **Repository:** https://github.com/evanphx/benchmark-ips
- **License:** MIT License

### Python Port
- **Translation:** November 2025
- **Approach:** Faithful port maintaining API compatibility
- **License:** MIT License (same as original)

**Thank you to Evan Phoenix and all Ruby benchmark-ips contributors for creating such a valuable tool!**

For detailed credits, see `CREDITS.md`.

## Contributing

This is a port of the Ruby gem. For issues specific to the Python version, please report them in the issue tracker. For general feature requests or improvements, consider contributing to the original Ruby version.
