with open("input.txt", "r") as f:
    content = f.readlines()

grid = []
for line in content:
    grid.append(list(map(int,line.strip())))

def isLow(i, j):
    if i > 0 and grid[i][j] >= grid[i-1][j]:
        return False
    if i < len(grid) - 1 and grid[i][j] >= grid[i+1][j]:
        return False
    if j > 0 and grid[i][j] >= grid[i][j-1]:
        return False
    if j < len(grid[i]) - 1 and grid[i][j] >= grid[i][j+1]:
        return False
    return True

def gridVal(i,j):
    if i < 0 or i >= len(grid):
        return -2
    if j < 0 or j >= len(grid[i]):
        return -2
    if grid[i][j] == 9:
        return -2
    if (i,j) in used:
        return -2
    return grid[i][j]

def basinSize(i,j):
    used.add((i,j))
    size = 1
    if grid[i][j] < gridVal(i-1,j):
        size += basinSize(i-1, j)
    if grid[i][j] < gridVal(i+1,j):
        size += basinSize(i+1, j)
    if grid[i][j] < gridVal(i,j-1):
        size += basinSize(i, j-1)
    if grid[i][j] < gridVal(i,j+1):
        size += basinSize(i, j+1)
    return size

lows = []
riskSum = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if isLow(i,j):
            riskSum += 1 + grid[i][j]
            lows.append((i,j))
print(riskSum)

used = set()
basins = []
for i, j in lows:
    res = basinSize(i,j)
    basins.append(res)
basins.sort()
print(basins[-1]*basins[-2]*basins[-3])
