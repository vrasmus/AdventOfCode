import concurrent.futures

with open("input.txt", "r") as f:
    groupings = f.read().split("\n\n")

    seeds = list(map(int, groupings[0].split()[1:]))
    mappings = []
    for m in groupings[1:]:
        m = m.strip().split("\n")[1:]
        m = [list(map(int,m_.split())) for m_ in m]
        mappings.append(m)


def map_to_closest(seed, mappings):
    current = seed
    for mapping in mappings:
        for dest, src, extent in mapping:
            if src <= current < src + extent:
                change = current - src
                current = dest + change 
                break
    return current


def part1():
    closest = 1e999
    for seed in seeds:
        closest = min(closest, map_to_closest(seed, mappings))
    return closest


"""
Brute-forcing isn't really possible for my input (at least with naive Python).
So, find something "close enough" and brute-force from there.
"""
def part2():
    closest = 1e999

    seedStarts = seeds[::2]
    seedRanges = seeds[1::2]
    for seedStart, seedRange in zip(seedStarts, seedRanges):
        for seed in range(seedStart, seedStart+seedRange, 10000):
            loc = map_to_closest(seed, mappings)
            if loc < closest:
                closest = loc
                somewhatCloseSeed = seed

    for seed in range(somewhatCloseSeed - 10000, somewhatCloseSeed + 10000):
        loc = map_to_closest(seed, mappings)
        if loc < closest:
            closest = loc
    return closest


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


