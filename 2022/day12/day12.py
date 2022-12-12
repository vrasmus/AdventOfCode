from collections import deque

with open("input.txt", "r") as f:
    rows = f.read().strip().split("\n")
    grid = [list(r) for r in rows]


def find_start(grid):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == "S":
                return i, j


def add_neighbors(grid, queue, i, j, steps):
    curr = ord(grid[i][j])
    
    for di, dj in [(0,1),(1,0),(0,-1),(-1,0)]:
        ni, nj = i+di, j+dj
        if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
            continue

        neighbor = ord(grid[ni][nj])
        if ord("a") <= neighbor <= curr + 1 or (grid[i][j] == "z" and grid[ni][nj] == "E"):
            queue.append(((ni,nj), steps+1))


def find_shortest_path(grid, i, j):
    # Solve using BFS
    visited = {}
    queue = deque()
    queue.append(((i,j), 0))
    while queue:
        (i,j), steps = queue.popleft()
        if (i,j) in visited:
            continue

        visited[(i,j)] = steps
        if grid[i][j] == "E":
            return steps
        
        add_neighbors(grid, queue, i, j, steps)
    return float("inf") # No path...


def find_global_best(grid):
    dist = float("inf")
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "a":
                dist = min(dist, find_shortest_path(grid, i, j))
    return dist


if __name__ == "__main__":
    i,j = find_start(grid)
    grid[i][j] = "a"
    print("Part 1:", find_shortest_path(grid, i,j))
    print("Part 2:", find_global_best(grid))
