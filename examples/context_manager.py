"""Example using context manager style."""

import benchmark_ips as bm


if __name__ == '__main__':
    print("Using context manager style:\n")

    with bm.benchmark(warmup=1, time=2) as x:
        x.report("list comprehension", lambda: [i * 2 for i in range(100)])
        x.report("map function", lambda: list(map(lambda i: i * 2, range(100))))
        x.report("for loop", lambda: [x * 2 for x in range(100)])
        x.enable_compare()
