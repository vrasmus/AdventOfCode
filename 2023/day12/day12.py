with open("input.txt", "r") as f:
    lines = [l.strip().split() for l in f.readlines()]
    rows = [list(l[0]) for l in lines]
    configs = [list(map(int, l[1].split(","))) for l in lines]


# For part 2 we cannot reasonably finish. We solve the same 
# subproblem many times though, so just cache all subproblems.
cache = {}
def arrangements_with_cache(row, config): 
    key = (tuple(row), tuple(config))
    if key not in cache:
        cache[key] = arrangements(row, config)
    return cache[key]


def arrangements(row, config):
    if len(row) == 0:
        return 1 if len(config) == 0 else 0

    result = 0
    if row[0] in ".?":
        # We can consider this field a "."
        result += arrangements_with_cache(row[1:], config)

    # Otherwise we have to consider the field as a "#"
    if len(config) == 0:
        return result

    group_size = config[0]
    if len(row) < group_size: 
        return result
    for i in range(group_size):
        if row[i] not in "?#":
            return result

    if len(row) > group_size and row[group_size] == "#":
        return result

    # We can make a # group here.
    result += arrangements_with_cache(row[group_size+1:], config[1:])
    return result


def part1():
    result = 0
    for row, config in zip(rows, configs):
        result += arrangements_with_cache(row, config)
    return result


def part2():
    result = 0
    for row, config in zip(rows, configs):
        super_row = []
        for _ in range(5):
            for r in row:
                super_row.append(r)
            super_row.append("?")
        super_row = super_row[:-1]

        super_config = [c for _ in range(5) for c in config]
        result += arrangements_with_cache(super_row, super_config)
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
