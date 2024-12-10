with open("input.txt","r") as f:
    grid = [list(map(int, list(l.strip()))) for l in f.readlines()]

DIRECTIONS = [(0,1), (1,0), (-1,0), (0,-1)]

def in_grid(x,y):
    if not (0<=x<len(grid)):
        return False
    if not (0<=y<len(grid[x])):
        return False
    return True

def dfs(x, y, visited_peaks, prev = -1, part2 = False):
    if not in_grid(x,y):
        return 0
    
    if grid[x][y] != prev + 1:
        return 0

    if grid[x][y] == 9:
        if part2:
            # Repeated trail peaks are fine
            return 1

        if (x,y) in visited_peaks:
            return 0
        visited_peaks.add((x,y))
        return 1

    res = 0
    for dx, dy in DIRECTIONS:
        res += dfs(x+dx, y+dy, visited_peaks, grid[x][y], part2)
    return res  


result1 = 0
result2 = 0
for x, row in enumerate(grid):
    for y, val in enumerate(row):
        result1 += dfs(x,y,set(), part2=False)
        result2 += dfs(x,y,set(), part2=True)
print("Part 1:", result1)
print("Part 2:", result2)
