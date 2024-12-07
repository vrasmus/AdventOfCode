with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

DIRECTIONS = [(-1,0), (0,1), (1,0), (0,-1)]

def in_grid(i,j):
    if not 0<=i<len(grid):
        return False
    if not 0<=j<len(grid[i]):
        return False
    return True


def parse():
    obstructions = set()
    for i, row in enumerate(grid):
        for j, field in enumerate(row):
            if field == "^":
                start = (i,j)
            if field == "#":
                obstructions.add((i,j))
    return start, obstructions


# brute force, guess that if we don't exit after cycle_min steps to be stuck forever.
def patrol(start, obstructions, part1 = False, cycle_min = 10000):
    visited = set()
    curr = start
    direction = 0
    step = 0
    while in_grid(*curr):
        step += 1
        visited.add(curr)
        dx, dy = DIRECTIONS[direction]
        x, y = curr
        nxt = x+dx, y+dy
        if nxt in obstructions:
            direction = (direction + 1)%4
        else:
            curr = nxt

        if cycle_min < step:
            return True # cycle
    
    if part1:
        print("Part 1:", len(visited))
    return False # No cycle


def search_cycles(start, obstructions):
    cycles = 0
    for i in range(len(grid)):
        print(f"{i/len(grid)*100}%")
        for j in range(len(grid[i])):
            if (i,j) in obstructions or (i,j) == start:
                continue
            obstructions.add((i,j))
            if patrol(start, obstructions):
                cycles += 1
            obstructions.remove((i,j))
    print("Part 2:", cycles)


start, obstructions = parse()
patrol(start, obstructions, True)
search_cycles(start, obstructions)
