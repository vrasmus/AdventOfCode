with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

antennas = {}
for i, row in enumerate(grid):
    for j, space in enumerate(row):
        if space != ".":
            locs = antennas.get(space, set())
            locs.add((i,j))
            antennas[space] = locs


ROWS, COLS = len(grid), len(grid[0])


def in_grid(x, y):
    if not (0 <= x < ROWS):
        return False
    if not (0 <= y < COLS):
        return False
    return True


def find_antinodes(part2=False):
    antinodes = set()
    for antenna, locs in antennas.items():
        locs = list(locs)
        for i in range(len(locs)):
            for j in range(len(locs)):
                if i == j:
                    continue
                (x1, y1), (x2,y2) = locs[i], locs[j]
                dx, dy = x1 - x2, y1 - y2
                step = 0 if part2 else 1
                xa, ya = x1 + step*dx, y1 + step*dy
                while in_grid(xa, ya) and (step == 1 or part2):
                    antinodes.add((xa,ya))
                    step += 1
                    xa, ya = x1 + step*dx, y1 + step*dy
    return antinodes


print("Part 1:", len(find_antinodes(part2=False)))
print("Part 2:", len(find_antinodes(part2=True)))
    
