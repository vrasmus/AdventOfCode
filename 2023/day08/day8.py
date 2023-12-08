with open("input.txt", "r") as f:
    content = f.read()
    parts = content.split("\n\n")
    directions = parts[0]
    unparsed_maps = [p.split(" = ") for p in parts[1].strip().split("\n")]
    maps = {}
    for m in unparsed_maps:
        maps[m[0]] = tuple(m[1][1:-1].split(", "))


def part1():
    steps = 0
    at = "AAA"
    while at != "ZZZ":
        d = directions[steps % len(directions)]
        didx = 0 if d == "L" else 1
        at = maps[at][didx]
        steps += 1
    return steps


def part2_brute_force():
    at = []
    for loc in maps.keys():
        if loc[-1] == "A":
            at.append(loc)

    steps = 0
    while not all([loc[-1] == "Z" for loc in at]):
        d = directions[steps % len(directions)]
        didx = 0 if d == "L" else 1

        new_at = []
        for loc in at:
            new_at.append(maps[loc][didx])
        at = new_at
        steps += 1
    return steps


def steps_to_z_end(start):
    steps = 0
    at = start
    while at[-1] != "Z":
        d = directions[steps % len(directions)]
        didx = 0 if d == "L" else 1
        at = maps[at][didx]
        steps += 1
    return steps


def part2():
    cycle_lengths = []
    for loc in maps.keys():
        if loc[-1] == "A":
            cycle_lengths.append(steps_to_z_end(loc))

    import math
    return math.lcm(*cycle_lengths)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
