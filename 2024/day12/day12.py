with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]



RIGHT, DOWN, UP, LEFT = (0,1), (1,0), (-1,0), (0,-1)
DIRECTIONS = [RIGHT, DOWN, UP, LEFT]


def in_grid(x,y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])


def is_corner(x, y, d1, d2):
    dx1, dy1 = d1
    dx2, dy2 = d2
    x1, y1 = x + dx1, y + dy1
    x2, y2 = x + dx2, y + dy2
    xdiag, ydiag = x + dx1 + dx2, y + dy1 + dy2

    ok1 = (not in_grid(x1, y1)) or grid[x][y] != grid[x1][y1]
    ok2 = (not in_grid(x2, y2)) or grid[x][y] != grid[x2][y2]
    outside_corner = ok1 and ok2
    inside_corner = in_grid(xdiag,ydiag) and grid[x][y] == grid[x1][y1] == grid[x2][y2] and grid[x][y] != grid[xdiag][ydiag]
    return outside_corner or inside_corner

# Number of sides is equal to number of corners (which is easier to check locally).
def check_corners(x, y):
    corners = 0
    for d1, d2 in [(UP,LEFT),(UP,RIGHT),(DOWN,LEFT),(DOWN,RIGHT)]:
        if is_corner(x, y, d1, d2):
            corners += 1
    return corners


area = {}
perimeter = {}
corners = {}
visited = set()
def dfs(x, y, regionID):
    if not in_grid(x,y):
        return

    if (x,y) in visited:
        return

    region = grid[x][y]
    visited.add((x,y))
    
    key = (region, regionID)
    area[key] = area.get(key,0) + 1
    corners[key] = corners.get(key, 0) + check_corners(x,y)
    for dx, dy in DIRECTIONS:
        xn, yn = x + dx, y + dy
        if not in_grid(xn, yn):
            perimeter[key] = perimeter.get(key, 0) + 1
            continue

        if grid[xn][yn] != region:
            perimeter[key] = perimeter.get(key, 0) + 1
        else:
            dfs(xn,yn, regionID)


for x, row in enumerate(grid):
    for y in range(len(row)):
        dfs(x,y, x*len(row)+y)


result1 = 0
result2 = 0
for key in area.keys():
    result1 += area[key] * perimeter[key]
    result2 += area[key] * corners[key]
print("Part 1:", result1)
print("Part 2:", result2)

