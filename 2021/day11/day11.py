with open("input.txt", "r") as f:
    content = [l.strip() for l in f.readlines()]
grid = [list(map(int, g)) for g in map(list, content)]

def inc(row,col):
    if row < 0 or row >= len(grid):
        return
    if col < 0 or col >= len(grid[row]):
        return
    grid[row][col] += 1  

def flash(row,col):
    if grid[row][col] <= 9:
        return False

    grid[row][col] = -9999
    for r in [row-1, row, row+1]:
        for c in [col-1, col, col+1]:
            inc(r, c)
    return True

def incrementAll():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] += 1

def flashAll():
    count = 0
    flashed = -1
    while flashed != 0:
        flashed = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if flash(i,j):
                    flashed += 1
        count += flashed
    return count

def cleanAll():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = max(grid[i][j], 0)

def step():
    incrementAll()
    count = flashAll()
    cleanAll()
    return count

res = 0
for s in range(1,1000):
    this = step()
    res += this
    if s == 100:
        print("part 1:", res)
    if this == 100: # all flashes
        print("part 2:", s)
        break
