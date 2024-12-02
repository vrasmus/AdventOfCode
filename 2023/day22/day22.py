def parse_brick(line):
    left, right = line.strip().split("~")
    
    left = tuple(map(int, left.split(",")))
    right = tuple(map(int, right.split(",")))

    if left[2] > right[2]:
        left,right = right,left
    return left, right

def drop_brick(grid, brick):
    # Find biggest x, y that the brick will hit
    lands_at = 0
    for x in range(brick[0][0], brick[1][0]+1):
        for y in range(brick[0][1], brick[1][1]+1):
            lands_at = max(lands_at, grid.get((x,y), 0) + 1)
    return (brick[0][0], brick[0][1], lands_at), (brick[1][0], brick[1][1], lands_at + brick[1][2] - brick[0][2])  


def gravity(bricks):
    tallest = {}
    result = []
    fall_count = 0
    for brick in bricks:
        dropped = drop_brick(tallest, brick)
        if dropped != brick:
            fall_count += 1
        for x in range(dropped[0][0], dropped[1][0]+1):
            for y in range(dropped[0][1], dropped[1][1]+1):
                tallest[(x,y)] = dropped[1][2]
        result.append(dropped)
    return result, fall_count


def part1(bricks):
    bricks = bricks.copy()
    bricks, _ = gravity(bricks)
    result = 0
    for i in range(len(bricks)):
        removed = bricks[:i] + bricks[i + 1:]
        _, fall_count = gravity(removed)
        if fall_count == 0:
            result += 1
    return result 


def part2(bricks):
    bricks = bricks.copy()
    bricks, _ = gravity(bricks)
    result = 0
    for i in range(len(bricks)):
        removed = bricks[:i] + bricks[i + 1:]
        _, fall_count = gravity(removed)
        result += fall_count
    return result 


with open("input.txt", "r") as f:
    bricks = [parse_brick(l) for l in f.readlines()]
    bricks = sorted(bricks, key = lambda b: b[1][2]) # Sort by brick's highest z coordinate


if __name__ == "__main__":
    print(f"Part 1: {part1(bricks)}")
    print(f"Part 2: {part2(bricks)}")
