with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")
    grid = [[int(x) for x in list(line)] for line in lines]
    

def valid(grid, i, j):
    n, m = len(grid), len(grid[0])
    return 0 <= i < n and 0 <= j < m


def search(grid, i, j, curr_max, direction, visible):
    if not valid(grid, i, j):
        return

    if grid[i][j] > curr_max:
        visible.add((i,j))

    dr, dc = direction
    search(grid, i+dr, j+dc, max(curr_max, grid[i][j]), direction, visible)


def viewing_distance(grid, i, j, direction):
    dr, dc = direction   
    x, y = i + dr, j + dc
    steps = 0
    while valid(grid, x, y) and grid[x][y] < grid[i][j]:
        x += dr
        y += dc
        steps += 1
    return steps + 1 if valid(grid, x, y) else steps


def scenic_score(grid, i, j):
    d1 = viewing_distance(grid, i, j, (0, 1))
    d2 = viewing_distance(grid, i, j, (1, 0))
    d3 = viewing_distance(grid, i, j, (0, -1))
    d4 = viewing_distance(grid, i, j, (-1, 0))
    return d1 * d2 * d3 * d4


if __name__ == "__main__":
    n, m = len(grid), len(grid[0])
    visible = set()
    for i in range(n):
        search(grid, i, 0, -1, (0, 1), visible)
        search(grid, i, n-1, -1, (0, -1), visible)
    for j in range(m):
        search(grid, 0, j, -1, (1, 0), visible)
        search(grid, m-1, j, -1, ( -1, 0), visible)
    print("Part 1:", len(visible))
    
    best = 0
    for i in range(n):
        for j in range(m):
            score = scenic_score(grid, i, j)
            best = max(best, score)
    print("Part 2:", best)
