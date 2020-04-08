import sys
import math
import bisect
from pathlib import Path


def percentile(n, percent):
    k = (len(n) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return n[int(k)]
    d0 = n[int(f)] * (c - k)
    d1 = n[int(c)] * (k - f)
    return d0 + d1


if __name__ == '__main__':
    numbers_file = Path(sys.argv[1])

    with numbers_file.open() as stream:
        data = tuple(int(line) for line in stream)

    data = sorted(data)

    average = sum(data) / len(data)
    percentile_90 = percentile(data, 0.90)

    start = bisect.bisect_left(data, average)
    stop = bisect.bisect_left(data, percentile_90) - 1

    if stop < start:
        start, stop = stop, start

    items = (data[i] for i in range(start, stop + 1))
    print(sum(items))
