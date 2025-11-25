"""Quick benchmark example using ips_quick."""

import benchmark_ips as bm


if __name__ == '__main__':
    # Compare string methods
    print("Comparing string methods:")
    bm.ips_quick('upper', 'lower', on="Hello World!", warmup=1, time=2)

    print("\n" + "="*50 + "\n")

    # Compare list operations
    print("Comparing list methods:")
    my_list = [1, 2, 3, 4, 5]
    bm.ips_quick('copy', 'reverse', on=my_list, warmup=1, time=2)
