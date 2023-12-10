with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]
rows, cols = len(grid), len(grid[0])


def find_start(grid): 
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == "S":
                return i, j


def valid_moves(x,y): 
    potentials = potential_moves(x,y)
    moves = []
    if (0,1) in potentials:
        if is_in_grid(x, y+1) and grid[x][y+1] in ["-", "7", "J"]:
            moves.append((x,y+1))
    if (0,-1) in potentials:
        if is_in_grid(x, y-1) and grid[x][y-1] in ["-", "L", "F"]:
            moves.append((x,y-1))
    if (1,0) in potentials:
        if is_in_grid(x+1, y) and grid[x+1][y] in ["|", "L", "J"]:
            moves.append((x+1,y))
    if (-1,0) in potentials:
        if is_in_grid(x-1, y) and grid[x-1][y] in ["|", "7", "F"]:
            moves.append((x-1,y))
    return moves


def potential_moves(x, y):
    this = grid[x][y]
    if this == "-":
        return [(0, -1), (0, 1)]
    if this == "|":
        return [(-1, 0), (1, 0)]
    if this == "L":
        return [(-1, 0), (0, 1)]
    if this == "J":
        return [(-1, 0), (0, -1)]
    if this == "F":
        return [(1, 0), (0, 1)]
    if this == "7":
        return [(1, 0), (0, -1)]
    if this == "S":
        return [(0,1), (1,0), (-1,0), (0,-1)]


def is_in_grid(x,y): 
    return 0 <= x < rows and 0 <= y < cols


if __name__ == "__main__":
    start = find_start(grid)

    visited = {}
    queue = [(start, 0, [])]

    while queue:
        (x, y), steps, history = queue[0]
        queue = queue[1:]

        if (x,y) in visited: 
            continue
        visited[(x, y)] = True

        history = history.copy()
        history.append((x,y))

        moves = valid_moves(x,y)
        for move in moves:
            queue.append((move, steps+1, history))

    print(f"Part 1: {len(history) - 1}")
