with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

def parse(line):
    line = line.split(" -> ")
    line = [tuple(map(int, l.split(","))) for l in line]
    return line


def draw_single(start, end, cave):
    sx, sy = start
    ex, ey = end

    if sx == ex:
        # Horizontal line
        if sy > ey:
            sy, ey = ey, sy
        for y in range(sy, ey+1):
            cave[(sx, y)] = "#"

    if sy == ey:
        # Vertical line
        if sx > ex:
            sx, ex = ex, sx
        for x in range(sx, ex+1):
            cave[(x, sy)] = "#"


def draw(line, cave):
    start = line[0]
    for end in line[1:]:
        draw_single(start, end, cave)
        start = end


def drop_sand(cave, step_limit=1000):
    x, y = 500, 0
    
    while step_limit:
        if (x, y+1) not in cave:
            y += 1
        elif (x-1, y+1) not in cave:
            y += 1   
            x -= 1
        elif (x+1, y+1) not in cave:
            y += 1
            x += 1
        else:
            cave[(x,y)] = "o"
            break
        step_limit -= 1

    return step_limit > 0 # Non-zero if not done


def find_floor(cave):
    lowest = 0
    for x, y in cave.keys():
        lowest = max(lowest, y)
    return lowest + 2


def drop_sand_with_floor(cave, floor):
    x, y = 500, 0
    if (x, y) in cave:
        return False
    
    while True:
        if y+1 == floor:
            cave[(x,y)] = "o"
            return True
        elif (x, y+1) not in cave:
            y += 1
        elif (x-1, y+1) not in cave:
            y += 1   
            x -= 1
        elif (x+1, y+1) not in cave:
            y += 1
            x += 1
        else:
            cave[(x,y)] = "o"
            return True


def part1(lines):
    cave = {}
    for l in lines:
        draw(l, cave)
    
    filled_before = len(cave)
    while drop_sand(cave):
        pass
    filled_after = len(cave)
    return filled_after - filled_before


def part2(lines):
    cave = {}
    for l in lines:
        draw(l, cave)
    
    floor = find_floor(cave)
    filled_before = len(cave)
    while drop_sand_with_floor(cave, floor):
        pass
    filled_after = len(cave)
    return filled_after - filled_before


if __name__ == "__main__":
    lines = [parse(l) for l in lines]
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))
    
