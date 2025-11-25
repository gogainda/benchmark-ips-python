#!/usr/bin/env python3
"""
Simple FAST vs SLOW comparison - All demos in one run!
"""

import benchmark_ips as bm
from collections import Counter


print("=" * 70)
print("  FAST vs SLOW CODE - Performance Comparison")
print("=" * 70)
print()


# Demo 1: String building
print("1️⃣  STRING BUILDING (1000 parts)")
print("-" * 70)

with bm.benchmark(warmup=1, time=2) as x:
    def slow():
        result = ""
        for i in range(1000):
            result = result + str(i)
        return result

    def fast():
        return "".join(str(i) for i in range(1000))

    x.report("❌ SLOW (concat)", slow)
    x.report("✅ FAST (join)", fast)
    x.enable_compare()


# Demo 2: List membership
print("\n2️⃣  MEMBERSHIP TEST (10,000 items)")
print("-" * 70)

items_list = list(range(10000))
items_set = set(range(10000))
target = 9999

with bm.benchmark(warmup=1, time=2) as x:
    x.report("❌ SLOW (list)", lambda: target in items_list)
    x.report("✅ FAST (set)", lambda: target in items_set)
    x.enable_compare()


# Demo 3: Summing
print("\n3️⃣  SUM NUMBERS (10,000 numbers)")
print("-" * 70)

numbers = list(range(10000))

with bm.benchmark(warmup=1, time=2) as x:
    def slow():
        total = 0
        for i in range(len(numbers)):
            total += numbers[i]
        return total

    x.report("❌ SLOW (manual)", slow)
    x.report("✅ FAST (built-in)", lambda: sum(numbers))
    x.enable_compare()


# Demo 4: Counting items
print("\n4️⃣  COUNT ITEMS (6,000 items)")
print("-" * 70)

items = ['a', 'b', 'c', 'a', 'b', 'a'] * 1000

with bm.benchmark(warmup=1, time=2) as x:
    def slow():
        result = {}
        for item in set(items):
            result[item] = items.count(item)
        return result

    def fast():
        result = {}
        for item in items:
            result[item] = result.get(item, 0) + 1
        return result

    x.report("❌ SLOW (list.count)", slow)
    x.report("✅ FAST (dict)", fast)
    x.report("🚀 FASTEST (Counter)", lambda: Counter(items))
    x.enable_compare()


# Demo 5: Common elements
print("\n5️⃣  FIND COMMON ELEMENTS (500 & 500 items)")
print("-" * 70)

list1 = list(range(500))
list2 = list(range(250, 750))

with bm.benchmark(warmup=1, time=2) as x:
    def slow():
        result = []
        for item1 in list1:
            for item2 in list2:
                if item1 == item2:
                    result.append(item1)
                    break
        return result

    x.report("❌ SLOW (nested loops)", slow)
    x.report("✅ FAST (set &)", lambda: list(set(list1) & set(list2)))
    x.enable_compare()


# Demo 6: String formatting
print("\n6️⃣  FORMAT STRINGS (1,000 strings)")
print("-" * 70)

with bm.benchmark(warmup=1, time=2) as x:
    def slow():
        return ["Item " + str(i) + " val: " + str(i*2) for i in range(1000)]

    def fast():
        return [f"Item {i} val: {i*2}" for i in range(1000)]

    x.report("❌ SLOW (concat)", slow)
    x.report("✅ FAST (f-string)", fast)
    x.enable_compare()


# Demo 7: EXTREME difference - Sorting
print("\n7️⃣  SORTING (500 numbers) - EXTREME DIFFERENCE!")
print("-" * 70)

data = list(range(500, 0, -1))

with bm.benchmark(warmup=0.5, time=1) as x:
    def bubble_sort():
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    x.report("🐌 SLOW (bubble sort)", bubble_sort)
    x.report("🚀 FAST (built-in)", lambda: sorted(data))
    x.enable_compare()


# Summary
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print("""
KEY LESSONS:
  1. String concat in loops → Use join()             (~1.2x faster)
  2. 'in list' lookups → Use 'in set'                (~1000x faster!)
  3. Manual sum → Use built-in sum()                 (~2x faster)
  4. list.count() in loop → Use dict or Counter      (~10-100x faster)
  5. Nested loops → Use set operations               (~100-500x faster)
  6. String concat → Use f-strings                   (~1.3x faster)
  7. Bubble sort → Use built-in sorted()             (~1000x+ faster!)

💡 TIP: Always measure! benchmark-ips shows you the REAL difference.
""")
print("=" * 70)
