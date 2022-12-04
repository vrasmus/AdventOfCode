def parse_range(r):
    return tuple(map(int, r.split("-")))


def parse_line(l):
    r1, r2 = l.strip().split(",")
    return parse_range(r1), parse_range(r2)


def total_overlap(r1, r2):
    r1min, r1max = r1
    r2min, r2max = r2
    if r2min <= r1min and r1max <= r2max:
        return True
    if r1min <= r2min and r2max <= r1max:
        return True
    return False


def any_overlap(r1, r2):
    r1min, r1max = r1
    r2min, r2max = r2
    if r2min <= r1min <= r2max:
        return True
    if r1min <= r2min <= r1max:
        return True
    return False


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        pairs = [parse_line(l) for l in f.readlines()]

    totalPart1 = 0
    totalPart2 = 0
    for pair in pairs:
        if total_overlap(*pair):
            totalPart1 += 1
        if any_overlap(*pair):
            totalPart2 += 1

    print("Part 1:", totalPart1)
    print("Part 2:", totalPart2)
