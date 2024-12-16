with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

WEST, EAST, NORTH, SOUTH = (0, -1), (0, 1), (-1, 0), (1, 0)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST] # Clockwise


start_dir = 1 # Index of east
start = None
goal = None
for i, row in enumerate(grid):
    for j, tile in enumerate(row):
        match tile:
            case "S":
                start = (i,j)
            case "E":
                goal = (i,j)


def move(pos, d):
    x, y = pos
    dx, dy = DIRECTIONS[d]
    return x+dx, y+dy


import heapq

def optimal_paths(start, goal):
    q = [(0, start, start_dir, [])]
    visited = {}

    best = 1e99
    optimal_tiles = set()
    while q:
        cost, at, d, path = heapq.heappop(q)
        path.append(at)
        if at == goal and cost <= best:
            optimal_tiles.update(path)
            best = cost
    
        if grid[at[0]][at[1]] == "#":
            # Hit wall, impossible.
            continue
        
        if cost > visited.get((at, d), 1e99):
            continue # Already done.
        visited[(at, d)] = cost
    
        x, y  = at
        # Move forward
        heapq.heappush(q,(cost + 1, move(at, d), d, path.copy()))
        # Turn clockwise
        dc = (d + 1) % len(DIRECTIONS)
        heapq.heappush(q, (cost + 1001, move(at, dc), dc, path.copy()))
        # Turn counter-clockwise
        dcc = (d - 1) % len(DIRECTIONS)
        heapq.heappush(q, (cost + 1001, move(at, dcc), dcc, path.copy()))

    return best, len(optimal_tiles)

optimal_cost, optimal_path_tiles = optimal_paths(start, goal)
print("Part 1:", optimal_cost)
print("Part 2:", optimal_path_tiles)
