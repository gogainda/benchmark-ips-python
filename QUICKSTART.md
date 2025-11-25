# 🚀 Quick Start Guide

Get started with benchmark-ips in 60 seconds!

## Step 1: Import

```python
import benchmark_ips as bm
```

## Step 2: Write Your First Benchmark

```python
# The simplest way - context manager
with bm.benchmark() as x:
    x.report("addition", lambda: 1 + 2)
    x.report("multiplication", lambda: 2 * 3)
    x.enable_compare()
```

## Step 3: Run It!

```bash
PYTHONPATH=. python your_script.py
```

## Output

```
Python 3.12.9 on Linux
Warming up --------------------------------------
            addition     1.423M i/100ms
      multiplication     1.485M i/100ms
Calculating -------------------------------------
            addition     14.459M (± 7.1%) i/s
      multiplication     15.111M (± 4.6%) i/s

Comparison:
      multiplication: 15111110.5 i/s
            addition: 14459979.2 i/s - 1.04x slower
```

## Complete Example

```python
import benchmark_ips as bm

# Prepare your data
data = list(range(1000))

# Benchmark different approaches
with bm.benchmark(warmup=2, time=5) as x:
    x.report("sum", lambda: sum(data))
    x.report("loop", lambda: sum([x for x in data]))
    x.enable_compare()
```

## Try the Interactive Demo

```bash
PYTHONPATH=. python demo.py
```

## Next Steps

- 📖 Read `USAGE_GUIDE.md` for detailed examples
- 🎯 Check `CHEATSHEET.md` for quick reference
- 🧪 Explore `examples/` directory
- ✅ Run `pytest tests/` to see tests

---

**That's it! You're ready to benchmark!** 🎉
