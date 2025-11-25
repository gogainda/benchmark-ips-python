#!/usr/bin/env python3
"""
Python Idioms Performance Comparison

Benchmarks comparing different Python approaches similar to fast-ruby benchmarks.
Only includes comparisons where Python has meaningful alternatives.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import benchmark_ips as bm
from types import SimpleNamespace
import random


print("=" * 70)
print("  PYTHON IDIOMS - Performance Benchmarks")
print("  (Inspired by fast-ruby benchmarks)")
print("=" * 70)
print()


# =============================================================================
# EXCEPTION HANDLING
# =============================================================================
print("🔧 EXCEPTION HANDLING")
print("-" * 70)

class TestObj:
    def method_exists(self):
        pass

obj = TestObj()

with bm.benchmark(warmup=1, time=2) as x:
    x.report("hasattr() check", lambda: hasattr(obj, 'method_exists'))
    x.report("try/except", lambda: (
        obj.method_exists if hasattr(obj, 'method_exists') else None
    ))
    x.enable_compare()


# =============================================================================
# ITERATION & COMPREHENSION
# =============================================================================
print("\n🔁 ITERATION PATTERNS")
print("-" * 70)

numbers = list(range(100))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("for loop + append", lambda: (
        [n * 2 for _ in [None] for n in numbers] if False else
        list(map(lambda n: n * 2, numbers))  # Using map as proxy for loop
    ))
    x.report("list comprehension", lambda: [n * 2 for n in numbers])
    x.report("map()", lambda: list(map(lambda n: n * 2, numbers)))
    x.enable_compare()


# =============================================================================
# LIST OPERATIONS
# =============================================================================
print("\n📋 LIST OPERATIONS")
print("-" * 70)

# List membership
items_list = list(range(10000))
items_set = set(range(10000))
target = 9999

with bm.benchmark(warmup=1, time=2) as x:
    x.report("list membership", lambda: target in items_list)
    x.report("set membership", lambda: target in items_set)
    x.enable_compare()

print()

# First/last element access
test_list = list(range(1000))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("list[0]", lambda: test_list[0])
    x.report("list[-1]", lambda: test_list[-1])
    x.enable_compare()

print()

# Random sampling
big_list = list(range(1000))

with bm.benchmark(warmup=1, time=2) as x:
    def shuffle_first():
        shuffled = big_list.copy()
        random.shuffle(shuffled)
        return shuffled[0]

    x.report("shuffle().copy()[0]", shuffle_first)
    x.report("random.choice()", lambda: random.choice(big_list))
    x.enable_compare()

print()

# List concatenation
list1 = list(range(100))
list2 = list(range(100, 200))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("list + list", lambda: list1 + list2)
    x.report("list.extend()", lambda: (
        lambda: (lst := list1.copy(), lst.extend(list2), lst)[-1]
    )())
    x.report("[*list1, *list2]", lambda: [*list1, *list2])
    x.enable_compare()


# =============================================================================
# DICT OPERATIONS
# =============================================================================
print("\n📖 DICT OPERATIONS")
print("-" * 70)

test_dict = {'key': 'value', 'foo': 'bar'}

with bm.benchmark(warmup=1, time=2) as x:
    x.report("dict['key']", lambda: test_dict['key'])
    x.report("dict.get('key')", lambda: test_dict.get('key'))
    x.enable_compare()

print()

# Dict vs SimpleNamespace (similar to Hash vs OpenStruct)
data_dict = {'x': 1, 'y': 2, 'z': 3}
data_ns = SimpleNamespace(x=1, y=2, z=3)

with bm.benchmark(warmup=1, time=2) as x:
    x.report("dict access", lambda: data_dict['x'])
    x.report("SimpleNamespace", lambda: data_ns.x)
    x.enable_compare()

print()

# Dict creation
with bm.benchmark(warmup=1, time=2) as x:
    x.report("dict literal", lambda: {'a': 1, 'b': 2})
    x.report("dict()", lambda: dict(a=1, b=2))
    x.report("dict.copy()", lambda: test_dict.copy())
    x.enable_compare()

print()

# Dict merging (Python 3.9+)
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

with bm.benchmark(warmup=1, time=2) as x:
    x.report("dict.update()", lambda: (
        lambda: (d := dict1.copy(), d.update(dict2), d)[-1]
    )())
    x.report("{**dict1, **dict2}", lambda: {**dict1, **dict2})
    x.report("dict1 | dict2", lambda: dict1 | dict2)  # Python 3.9+
    x.enable_compare()


# =============================================================================
# STRING OPERATIONS
# =============================================================================
print("\n📝 STRING OPERATIONS")
print("-" * 70)

# String concatenation
with bm.benchmark(warmup=1, time=2) as x:
    x.report("str + str", lambda: "hello" + " " + "world")
    x.report("f-string", lambda: f"hello world")
    x.report("str.format()", lambda: "{} {}".format("hello", "world"))
    x.report("str.join()", lambda: " ".join(["hello", "world"]))
    x.enable_compare()

print()

# String building
parts = [str(i) for i in range(100)]

with bm.benchmark(warmup=1, time=2) as x:
    def concat_loop():
        result = ""
        for p in parts:
            result += p
        return result

    x.report("loop with +=", concat_loop)
    x.report("''.join()", lambda: ''.join(parts))
    x.enable_compare()

print()

# String case comparison
s1, s2 = "Hello", "hello"

with bm.benchmark(warmup=1, time=2) as x:
    x.report("str.lower() ==", lambda: s1.lower() == s2.lower())
    x.report("str.casefold() ==", lambda: s1.casefold() == s2.casefold())
    x.enable_compare()

print()

# String prefix/suffix checking
text = "hello_world_test"

with bm.benchmark(warmup=1, time=2) as x:
    x.report("str.startswith()", lambda: text.startswith("hello"))
    x.report("str[:5] ==", lambda: text[:5] == "hello")
    x.report("regex match", lambda: __import__('re').match(r'^hello', text))
    x.enable_compare()

print()

# String replacement
text = "hello world hello"

with bm.benchmark(warmup=1, time=2) as x:
    x.report("str.replace()", lambda: text.replace("hello", "hi"))
    x.report("str.replace(n=1)", lambda: text.replace("hello", "hi", 1))
    x.enable_compare()


# =============================================================================
# FUNCTION CALL PATTERNS
# =============================================================================
print("\n⚡ FUNCTION CALLS")
print("-" * 70)

def regular_func(*args):
    return sum(args)

with bm.benchmark(warmup=1, time=2) as x:
    x.report("func(1,2,3)", lambda: regular_func(1, 2, 3))
    x.report("func(*[1,2,3])", lambda: regular_func(*[1, 2, 3]))
    x.enable_compare()

print()

# getattr vs direct access
class Obj:
    attr = 42

obj = Obj()

with bm.benchmark(warmup=1, time=2) as x:
    x.report("obj.attr", lambda: obj.attr)
    x.report("getattr()", lambda: getattr(obj, 'attr'))
    x.enable_compare()


# =============================================================================
# SORTING & MIN/MAX
# =============================================================================
print("\n🔢 SORTING & MIN/MAX")
print("-" * 70)

data = [{'val': i} for i in range(100, 0, -1)]

with bm.benchmark(warmup=1, time=2) as x:
    x.report("sorted()[:1]", lambda: sorted(data, key=lambda x: x['val'])[:1])
    x.report("min()", lambda: [min(data, key=lambda x: x['val'])])
    x.enable_compare()

print()

# Reverse sorting
numbers = list(range(100))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("sorted(reverse=True)", lambda: sorted(numbers, reverse=True))
    x.report("sorted()[::-1]", lambda: sorted(numbers)[::-1])
    x.enable_compare()


# =============================================================================
# FILTERING
# =============================================================================
print("\n🔍 FILTERING")
print("-" * 70)

numbers = list(range(1000))

with bm.benchmark(warmup=1, time=2) as x:
    x.report("filter() + list()", lambda: list(filter(lambda x: x % 2 == 0, numbers)))
    x.report("list comprehension", lambda: [x for x in numbers if x % 2 == 0])
    x.enable_compare()

print()

# Find first matching
with bm.benchmark(warmup=1, time=2) as x:
    x.report("next(filter())", lambda: next(filter(lambda x: x > 500, numbers)))
    x.report("next(generator)", lambda: next(x for x in numbers if x > 500))
    x.enable_compare()


print("\n" + "=" * 70)
print("✅ Benchmarks complete!")
print("=" * 70)
