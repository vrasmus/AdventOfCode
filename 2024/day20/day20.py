import sys
sys.setrecursionlimit(10000)

with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]

def in_grid(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])

def on_path(x,y):
    return in_grid(x,y) and grid[x][y] != "#"

cache = {}
def distance_to_goal(x, y, prev = None):
    if (x,y) in cache:
        return cache[(x,y)]

    if grid[x][y] == "E":
        return 0

    for dx, dy in DIRECTIONS:
        candidate = (x+dx, y+dy)
        if on_path(*candidate) and prev != candidate:
            dist = distance_to_goal(x+dx, y+dy, (x,y)) + 1
            cache[(x,y)] = dist
            return cache[(x,y)]


def paths_saving_enough(x,y, max_skip = 2):
    result = 0
    org_dist = distance_to_goal(x,y)
    for dx in range(-max_skip, max_skip+1):
        for dy in range(-max_skip, max_skip+1):
            dist = abs(dx) + abs(dy)
            if dist > max_skip:
                continue
            if on_path(x+dx, y+dy):
                new_dist = distance_to_goal(x+dx,y+dy)
                if new_dist - org_dist - dist >= 100:
                    result += 1
    return result

for i, row in enumerate(grid):
    for j, field in enumerate(row):
        if field == "S":
            start = (i,j)
        if field == "E":
            end = (i,j)

# First populate cache of distances everywhere on path.
distance_to_goal(*start)

result1 = 0
result2 = 0
for i, row in enumerate(grid):
    for j, field in enumerate(row):
        if field != "#":
            result1 += paths_saving_enough(i,j, max_skip = 2)
            result2 += paths_saving_enough(i,j, max_skip = 20)

print("Part 1:", result1)
print("Part 2:", result2)
