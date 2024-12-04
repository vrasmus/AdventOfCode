with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

TARGET = "XMAS"
DIRECTIONS = [(0,1), (1,0), (0,-1), (-1,0), (1,-1), (1,1), (-1,1), (-1,-1)]


def dfs(row, col, idx, direction):
    if idx == 4:
        return True
    if not (0 <= row < len(grid)):
        return False
    if not (0 <= col < len(grid[row])):
        return False

    if grid[row][col] != TARGET[idx]:
        return False

    drow, dcol = direction
    return dfs(row + drow, col + dcol, idx+1, direction)


def valid_x_mas(row, col):
    if not (1 <= row < len(grid)-1):
        return False
    if not (1 <= col < len(grid[row])-1):
        return False

    if not grid[row][col] == "A":
        return False
    
    if not grid[row+1][col+1]+grid[row-1][col-1] in ["MS", "SM"]:
        return False
    
    if not grid[row-1][col+1]+grid[row+1][col-1] in ["MS", "SM"]:
        return False

    return True

res1 = 0
res2 = 0
for i, row in enumerate(grid):
    for j in range(len(row)):
        for d in DIRECTIONS:
            if dfs(i, j, 0, d):
                res1 += 1
        if valid_x_mas(i, j):
            res2 += 1

print("Part 1:", res1)
print("Part 2:", res2)
