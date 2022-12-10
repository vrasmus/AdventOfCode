with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")

MOVE_MAP = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def parse_move(line):
    s = line.split(" ")
    return int(s[1]), MOVE_MAP[s[0]]


def move_knot(target, knot):
    hx, hy = target
    tx, ty = knot
    
    moved_x, moved_y = False, False
    if tx <= hx - 2:
        tx += 1
        moved_x = True
    if tx >= hx + 2:
        tx -= 1
        moved_x = True
    if ty <= hy - 2:
        ty += 1
        moved_y = True
    if ty >= hy + 2:
        ty -= 1
        moved_y = True
    
    if moved_x and not moved_y:
        if ty <= hy-1:
            ty += 1
        if ty >= hy+1:
            ty -= 1
    if moved_y and not moved_x:
        if tx <= hx-1:
            tx += 1
        if tx >= hx+1:
            tx -= 1

    return tx, ty 


def simulate(num_knots):
    moves = [parse_move(m) for m in lines]
    knots = [(0,0)]*(num_knots+1)
    visited = set()
    visited.add((0,0))
    for steps, (dx, dy) in moves:
        for _ in range(steps):
            x, y = knots[0]
            knots[0] = (x+dx, y+dy)
            for i in range(1, len(knots)):
                knots[i] = move_knot(knots[i-1], knots[i])
            visited.add(knots[-1])
    return len(visited)


if __name__ == "__main__":
    print("Part 1:", simulate(1))
    print("Part 2:", simulate(9))
