with open("input.txt", "r") as f:
    content = [l.strip().split(",") for l in f.readlines()]
    locs = [tuple(map(int, l)) for l in content]

GRID_X = GRID_Y = 71
STEPS_PART_1 = 1024

DIRECTIONS = [(0,1), (1,0), (-1,0),(0,-1)]

def in_grid(x, y):
    return 0 <= x < GRID_X and 0 <= y < GRID_Y


def simulate(steps):
    grid = {}
    for step in range(steps): 
        # Simulate first kilobyte falling
        x, y = locs[step]
        grid[(x,y)] = "#"
    return grid


def minimum_steps(grid):
    visited = set()
    queue = [(0,0,0)]
    while queue:
        x, y, steps = queue[0]
        queue = queue[1:]
        if not in_grid(x, y):
            continue
        if grid.get((x,y)) == "#":
            continue
        if (x, y) in visited:
            continue
        visited.add((x,y))
        if (x, y) == (GRID_X - 1, GRID_Y - 1):
            return steps 
        
        for dx,dy in DIRECTIONS:
            queue.append((x+dx,y+dy,steps+1))

    return None
    

def best_path_at_time(t):
    grid = simulate(t)
    return minimum_steps(grid)


def part2():
    for t in range(STEPS_PART_1, len(locs)):
        steps = best_path_at_time(t)
        if not steps:
            break
    return locs[t-1]


print("Part 1:", best_path_at_time(STEPS_PART_1))
print("Part 2:", part2())
