with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]


def parse(lines):
    elves = set()
    for i, line in enumerate(lines):
        for j, pos in enumerate(line):
            if pos == "#":
                elves.add((i,j))
    return elves


def translate(direction):
    match direction:
        case "N":
            return -1, 0
        case "S":
            return 1, 0
        case "E":
            return 0, 1
        case "W":
            return 0, -1


def adjacent(pos, direction):
    match direction:
        case "N":
            steps = [(-1,-1),(-1, 0),(-1,1)]
        case "S":
            steps = [(1,-1),(1, 0),(1,1)]
        case "E":
            steps = [(-1,1),(0, 1),(1,1)]
        case "W":
            steps = [(-1,-1),(0,-1),(1,-1)]

    x, y = pos
    for dx, dy in steps:
        yield x+dx, y+dy


def elf_propose(elves, elf, order):
    x, y = elf
    has_neighbors = False
    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]:
        if (x+dx,y+dy) in elves:
            has_neighbors = True
            break

    if has_neighbors:
        for direction in order:
            valid_move = True
            for pos in adjacent(elf, direction):
                if pos in elves:
                    valid_move = False
            if valid_move:
                dx, dy = translate(direction)
                return x+dx, y+dy
    return elf


def propose(elves, order):
    proposals = {}
    for elf in elves:
        proposal = elf_propose(elves, elf, order)
        if proposal not in proposals:
            proposals[proposal] = []
        proposals[proposal].append(elf)
    return proposals


def move(proposals):
    moved = set()
    for p, elves in proposals.items():
        if len(elves) == 1:
            moved.add(p)
        else:
            for elf in elves:
                moved.add(elf)
    return moved


def step(elves, order):
    proposals = propose(elves, order)
    return move(proposals)


def simulate(elves):
    order = ["N", "S", "W", "E"]
    r = 0
    while True:
        if r == 10:  
            print("Part 1:", empty_ground(elves))
        new_elves = step(elves, order)
        r += 1

        if len(elves) == len(elves.intersection(new_elves)):
            print("Part 2:", r)
            return 

        order = order[1:] + order[:1]
        elves = new_elves
        #draw(elves)


def bounds(elves):
    x_max = float("-inf")
    x_min = float("inf")
    y_max = float("-inf")
    y_min = float("inf")
    for x, y in elves:
        x_max = max(x_max, x)
        x_min = min(x_min, x)
        y_max = max(y_max, y)
        y_min = min(y_min, y)
    return x_min, x_max, y_min, y_max


def draw(elves):
    x_min, x_max, y_min, y_max = bounds(elves)
    grid = [["."]*(y_max-y_min+1) for _ in range(x_max-x_min+1)]
   
    for x, y in elves:
        grid[x-x_min][y-y_min] = "#"

    for line in grid:
        print("".join(line))
    print("")


def empty_ground(elves):
    x_min, x_max, y_min, y_max = bounds(elves)
    return (x_max-x_min + 1) * (y_max-y_min + 1) - len(elves)


if __name__ == "__main__":    
    elves = parse(lines)
    simulate(elves)
