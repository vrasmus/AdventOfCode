with open("input.txt", "r") as f:
    content = f.read()


def parse_map(map_input):
    lines = map_input.split("\n")
    longest_line = max(map(len,lines))
    grid = []
    for l in lines:
        grid.append(list(l))
        while len(grid[-1]) < longest_line:
            grid[-1].append(" ")
    return grid


def parse_directions(directions):
    import re
    
    steps = list(map(int, re.findall('\d+', directions)))
    turns = re.findall('[RL]', directions)
    
    directions = []
    for step, turn in zip(steps, turns):
        directions.append(step)
        directions.append(turn)
    return directions


def find_start(grid):
    i = 0
    while grid[0][i] != ".":
        i += 1
    return (0, i), (0, 1)


def next_pos(grid, pos, orientation):
    x, y = pos
    dx, dy = orientation
    
    x_new = (x+dx) % len(grid)
    y_new = (y+dy) % len(grid[x_new])
    
    # Wrap around the map...
    while grid[x_new][y_new] == " ":
        x_new = (x_new + dx) % len(grid)
        y_new = (y_new + dy) % len(grid[x_new])
    
    if grid[x_new][y_new] == "#":
        # Step blocked by wall
        return x, y

    return x_new, y_new


def move(grid, pos, orientation, steps):
    while steps > 0:
        pos = next_pos(grid, pos, orientation)
        steps -= 1
    return pos


def turn_right(orientation):
    match orientation: 
        case (0, 1):
            return (1, 0)
        case (1, 0):
            return (0, -1)
        case (0, -1):
            return (-1, 0)
        case (-1, 0):
            return (0, 1)


def turn_left(orientation):
    match orientation: 
        case (0, 1):
            return (-1, 0)
        case (-1, 0):
            return (0, -1)
        case (0, -1):
            return (1, 0)
        case (1, 0):
            return (0, 1)


def turn(orientation, direction):
    match direction:
        case "R":
            return turn_right(orientation)
        case "L":
            return turn_left(orientation)


def do(grid, pos, orientation, direction):
    if direction in ["L", "R"]:
        orientation = turn(orientation, direction)
    else:
        pos = move(grid, pos, orientation, direction)
    return pos, orientation


def password(pos, orientation):
    x, y = pos
    
    match orientation:
        case (0,1):
            facing = 0
        case (1,0):
            facing = 1
        case (0,-1):
            facing = 2
        case (-1, 0):
            facing = 3
    
    return (x+1) * 1000 + (y+1) * 4 + facing

if __name__ == "__main__":
    map_input, directions_input = content.split("\n\n")
    grid = parse_map(map_input)
    directions = parse_directions(directions_input)

    pos, dd = find_start(grid)
    for direction in directions:
        pos, dd = do(grid, pos, dd, direction)
    print("Part 1:", password(pos, dd))
