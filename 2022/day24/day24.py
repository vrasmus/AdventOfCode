from collections import deque

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]


def blizzard_to_direction(blizzard):
    match blizzard:
        case ">":
            return (0, 1)
        case "<":
            return (0, -1)
        case "^":
            return (-1, 0)
        case "v":
            return (1, 0)


def step_blizzards(basin, wall_right, wall_bottom):
    new = {}
    for (x,y), directions in basin.items():
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if nx == wall_bottom:
                nx = 1
            if nx == 0:
                nx = wall_bottom - 1
            if ny == wall_right:
                ny = 1
            if ny == 0:
                ny = wall_right - 1
            if (nx, ny) not in new:
                new[(nx,ny)] = []
            new[(nx, ny)].append((dx,dy))
    return new


def options(pos, basin, wall_right, wall_bottom):
    x, y = pos
    goal = (wall_bottom, wall_right-1)
    for dx, dy in [(1,0), (0,1), (-1,0), (0,-1), (0,0)]:
        nx, ny = x+dx, y+dy
        if (nx,ny) == goal or (nx,ny) == (0, 1):
            yield nx, ny
        if 0 < nx < wall_bottom and 0 < ny < wall_right and (nx, ny) not in basin:
            yield nx, ny


def traverse(start, goal, steps, wall_right, wall_botton, blizzards):
    seen = set()
    
    queue = deque([(steps, start)])
    while queue:
        steps, pos = queue.popleft()
        if (steps, pos) in seen:
            continue
        seen.add((steps, pos))
    
        if steps == len(blizzards):
            tmp = step_blizzards(blizzards[-1], wall_right, wall_bottom)
            blizzards.append(tmp)
        basin = blizzards[steps]
        
        if pos == goal:
            return steps - 1
        
        for npos in options(pos, basin, wall_right, wall_bottom):
            queue.append((steps+1, npos))
        

if __name__ == "__main__":
    wall_right, wall_bottom = len(lines[0])-1, len(lines)-1 
    basin = {}
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val in ["v", "^", "<", ">"]:
                basin[(x,y)] = [blizzard_to_direction(val)]
    
    blizzards = [basin]
    
    start = (0, 1)
    goal = (wall_bottom, wall_right-1)
    
    steps = traverse(start, goal, 0, wall_right, wall_bottom, blizzards)
    print("Part 1:", steps)
    steps = traverse(goal, start, steps, wall_right, wall_bottom, blizzards)
    steps = traverse(start, goal, steps, wall_right, wall_bottom, blizzards)
    print("Part 2:", steps)
