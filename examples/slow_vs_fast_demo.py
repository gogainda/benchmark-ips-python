#!/usr/bin/env python3
"""
Demonstration: Obviously SLOW vs FAST code

This shows dramatic performance differences to demonstrate benchmark-ips!
"""

import sys
from pathlib import Path
# Add parent directory to path so examples can be run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

import benchmark_ips as bm


def demo_1_string_building():
    """Demo 1: String concatenation - SLOW vs FAST"""
    print("=" * 70)
    print("DEMO 1: String Building - SLOW vs FAST")
    print("=" * 70)
    print("\nBuilding a string with 1000 parts:\n")

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Concatenating strings in a loop (creates new string each time!)
        def slow_concat():
            result = ""
            for i in range(1000):
                result = result + str(i)  # Creates new string every iteration!
            return result

        # FAST: Using join (efficient)
        def fast_join():
            return "".join(str(i) for i in range(1000))

        x.report("❌ SLOW (concatenation)", slow_concat)
        x.report("✅ FAST (join)", fast_join)
        x.enable_compare()


def demo_2_list_operations():
    """Demo 2: List operations - SLOW vs FAST"""
    print("\n" + "=" * 70)
    print("DEMO 2: Finding Items in Collections - SLOW vs FAST")
    print("=" * 70)
    print("\nChecking if item exists in 10,000 items:\n")

    # Setup data
    items = list(range(10000))
    items_set = set(range(10000))
    target = 9999  # Last item (worst case)

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Linear search in list
        def slow_list_search():
            return target in items

        # FAST: Hash lookup in set
        def fast_set_lookup():
            return target in items_set

        x.report("❌ SLOW (list search)", slow_list_search)
        x.report("✅ FAST (set lookup)", fast_set_lookup)
        x.enable_compare()


def demo_3_loops():
    """Demo 3: Loop operations - SLOW vs FAST"""
    print("\n" + "=" * 70)
    print("DEMO 3: Sum Numbers - SLOW vs FAST")
    print("=" * 70)
    print("\nSumming 10,000 numbers:\n")

    numbers = list(range(10000))

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Manual loop with append
        def slow_manual_sum():
            total = 0
            for i in range(len(numbers)):
                total += numbers[i]  # Index lookup every time!
            return total

        # FAST: Built-in sum
        def fast_builtin():
            return sum(numbers)

        x.report("❌ SLOW (manual loop)", slow_manual_sum)
        x.report("✅ FAST (built-in sum)", fast_builtin)
        x.enable_compare()


def demo_4_dictionary_access():
    """Demo 4: Dictionary operations - SLOW vs FAST"""
    print("\n" + "=" * 70)
    print("DEMO 4: Counting Items - SLOW vs FAST")
    print("=" * 70)
    print("\nCounting occurrences of items:\n")

    items = ['a', 'b', 'c', 'a', 'b', 'a'] * 1000

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Using list.count() for each unique item
        def slow_count():
            result = {}
            for item in set(items):
                result[item] = items.count(item)  # Scans entire list each time!
            return result

        # FAST: Using dict to count in one pass
        def fast_count():
            result = {}
            for item in items:
                result[item] = result.get(item, 0) + 1
            return result

        # FASTER: Using Counter
        from collections import Counter
        def fastest_counter():
            return Counter(items)

        x.report("❌ SLOW (list.count)", slow_count)
        x.report("✅ FAST (dict)", fast_count)
        x.report("🚀 FASTEST (Counter)", fastest_counter)
        x.enable_compare()


def demo_5_nested_loops():
    """Demo 5: Nested loops - SLOW vs FAST"""
    print("\n" + "=" * 70)
    print("DEMO 5: Finding Common Elements - SLOW vs FAST")
    print("=" * 70)
    print("\nFinding common elements between two lists:\n")

    list1 = list(range(500))
    list2 = list(range(250, 750))

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Nested loops O(n²)
        def slow_nested():
            result = []
            for item1 in list1:
                for item2 in list2:
                    if item1 == item2:
                        result.append(item1)
                        break
            return result

        # FAST: Set intersection O(n)
        def fast_set():
            return list(set(list1) & set(list2))

        x.report("❌ SLOW (nested loops)", slow_nested)
        x.report("✅ FAST (set intersection)", fast_set)
        x.enable_compare()


def demo_6_string_formatting():
    """Demo 6: String formatting - SLOW vs FAST"""
    print("\n" + "=" * 70)
    print("DEMO 6: Creating Formatted Strings - SLOW vs FAST")
    print("=" * 70)
    print("\nCreating 1000 formatted strings:\n")

    with bm.benchmark(warmup=1, time=2) as x:
        # SLOW: Multiple concatenations
        def slow_concat():
            results = []
            for i in range(1000):
                results.append("Item " + str(i) + " value: " + str(i * 2))
            return results

        # MEDIUM: format()
        def medium_format():
            results = []
            for i in range(1000):
                results.append("Item {} value: {}".format(i, i * 2))
            return results

        # FAST: f-strings
        def fast_fstring():
            results = []
            for i in range(1000):
                results.append(f"Item {i} value: {i * 2}")
            return results

        x.report("❌ SLOW (concatenation)", slow_concat)
        x.report("⚡ MEDIUM (format)", medium_format)
        x.report("✅ FAST (f-string)", fast_fstring)
        x.enable_compare()


def demo_7_extreme_difference():
    """Demo 7: Extreme difference - VERY SLOW vs VERY FAST"""
    print("\n" + "=" * 70)
    print("DEMO 7: EXTREME DIFFERENCE - Bubble Sort vs Built-in Sort")
    print("=" * 70)
    print("\nSorting 500 numbers:\n")

    data = list(range(500, 0, -1))  # Reversed list (worst case)

    with bm.benchmark(warmup=0.5, time=1) as x:
        # VERY SLOW: Bubble sort O(n²)
        def very_slow_bubble():
            arr = data[:]
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr

        # VERY FAST: Built-in sort O(n log n)
        def very_fast_builtin():
            return sorted(data)

        x.report("🐌 VERY SLOW (bubble sort)", very_slow_bubble)
        x.report("🚀 VERY FAST (built-in sort)", very_fast_builtin)
        x.enable_compare()


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SLOW vs FAST Code Comparison" + " " * 25 + "║")
    print("║" + " " * 18 + "benchmark-ips Demo" + " " * 32 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    print("This demo shows OBVIOUS performance differences!")
    print("Watch how benchmark-ips measures and compares them.\n")

    demos = [
        demo_1_string_building,
        demo_2_list_operations,
        demo_3_loops,
        demo_4_dictionary_access,
        demo_5_nested_loops,
        demo_6_string_formatting,
        demo_7_extreme_difference,
    ]

    for i, demo_func in enumerate(demos, 1):
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error in demo {i}: {e}")
            import traceback
            traceback.print_exc()
            continue

        # Pause between demos
        if i < len(demos):
            print("\n" + "-" * 70)
            try:
                input("Press Enter for next demo (Ctrl+C to exit)...")
            except KeyboardInterrupt:
                print("\n\nDemo stopped.")
                break

    print("\n" + "=" * 70)
    print("🎓 KEY TAKEAWAYS:")
    print("=" * 70)
    print("1. String concatenation in loops is SLOW - use join()")
    print("2. 'in list' is SLOW - use 'in set' for lookups")
    print("3. Built-in functions (sum, sorted) are FAST")
    print("4. Nested loops are SLOW - use sets/dicts when possible")
    print("5. f-strings are FAST - prefer them over concatenation")
    print("6. Algorithm choice matters! O(n²) vs O(n log n) is huge!")
    print("=" * 70)
    print("\n✨ benchmark-ips helps you make informed optimization decisions!\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled.")
