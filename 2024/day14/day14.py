with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

    robots = []
    for l in lines:
        pos = tuple(map(int,l.split(" ")[0][2:].split(",")))
        vel = tuple(map(int,l.split("=")[-1].split(",")))
        robots.append([pos, vel])


XLIM, YLIM = 101, 103

def step(robots):
    result = []
    for (x,y), (dx,dy) in robots:
        nx, ny = (x + dx) % XLIM, (y + dy) % YLIM
        result.append([(nx,ny),(dx,dy)])
    return result


def safety_factor(robots):
    quads = [0] * 4
    for (x,y), _ in robots:
        idx = 0
        if x == XLIM//2:
            continue
        if x > XLIM//2:
            idx += 2
        if y == YLIM//2:
            continue
        if y > YLIM//2:
            idx += 1
        quads[idx] += 1
    
    return quads[0]*quads[1]*quads[2]*quads[3]


min_val, max_val = 1e99, 0
for i in range(100000):
    robots = step(robots)
    score = safety_factor(robots)
    if i == 99:
        print("Part 1:", score)
    if score < min_val:
        print(f"new min at {i+1} seconds = {score}")
        min_val = score
    if score > max_val:
        print(f"new max at {i+1} seconds = {score}")
        max_val = score
