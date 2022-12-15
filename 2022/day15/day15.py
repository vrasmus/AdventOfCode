with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]


def to_coord(s):
    x, y = s.split(", ")
    return int(x[2:]),int(y[2:])


def parse(line):
    line = line.split(": ")
    line[0] = line[0].removeprefix("Sensor at").strip()
    line[1] = line[1].removeprefix("closest beacon is at").strip()
    return to_coord(line[0]), to_coord(line[1])


def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def coverage(cave, y, llim=float("-inf"), rlim=float("inf")):
    # Find intervals covered by the sensor
    intervals = []
    for sensor, beacon in cave.items():
        d_beacon = dist(sensor, beacon)
        sx, sy = sensor
        min_d = dist(sensor, (sx, y))
    
        remains = d_beacon - min_d
        if remains <= 0:
            continue
        intervals.append((sx-remains, sx+remains))
    intervals.sort()

    # Remove overlaps in the intervals
    truncated = []
    prevl, prevr = llim, llim
    for left, right in intervals:
        if right > rlim:
            right = rlim
        if left > rlim:
            left = rlim
        if right <= prevr:
            continue
        if left <= prevr:
            left = prevr
        prevl, prevr = left, right
        truncated.append([left, right])
    
    # Merge the intervals
    merged = [truncated[0]]
    for left, right in truncated[1:]:
        if left == merged[-1][1]:
            merged[-1][1] = right
        else:
            merged.append([left,right])

    return merged


def total_coverage(intervals):
    return sum([i[1]-i[0] for i in intervals])


def tuning_frequency(beacon):
    bx, by = beacon
    return bx*4000000 + by


def discover_beacon(cave, limit=4000000):
    # brute-force search for a y where the covered interval [0:4000000] is split by a single point
    for y in range(0, limit+1):
        if y % 100000 == 0:
            print(y)

        intervals = coverage(cave, y, llim=0, rlim=limit)
        if len(intervals) != 1:
            break
    
    assert intervals[0][1] + 2 == intervals[1][0]
    x = intervals[0][1] + 1
    return x, y


if __name__ == "__main__":
    cave = {}
    for line in lines:
        sensor, beacon = parse(line)
        cave[sensor] = beacon
    
    print("Part1:", total_coverage(coverage(cave, y=2000000)))
    print("Part2:", tuning_frequency(discover_beacon(cave)))
