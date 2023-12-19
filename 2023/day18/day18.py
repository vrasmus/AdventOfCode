with open("input.txt", "r") as f:
    lines = [l.strip().split() for l in f.readlines()]
    plan = [(l[0], int(l[1]), l[2][1:-1]) for l in lines]

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
directions = {"U": UP, "D": DOWN, "R": RIGHT, "L": LEFT}

def part1():
    def in_grid(x,y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])
    
    origin_shift = 400
    grid = [["."] * 2*origin_shift for _ in range(2*origin_shift)]
    pos = (0 + origin_shift, 0 + origin_shift)
    grid[pos[0]][pos[1]] = "#"
    
    for d, l, c in plan:
        dx, dy = directions[d]
        for steps in range(l):
            x, y = pos
            pos = (x + dx, y + dy)
            grid[x][y] = "#"
    
    
    
    
    queue = [(0,0)]
    while queue:
        x, y = queue.pop()
        if grid[x][y] != ".":
            continue
        grid[x][y] = "o"
        for dx, dy in directions.values():
            if in_grid(x+dx, y+dy):
                queue.append((x+dx, y+dy))
            
    
    result = 0
    for row in grid:
        for char in row:
            if char in "#.":
                result += 1
    return result

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
