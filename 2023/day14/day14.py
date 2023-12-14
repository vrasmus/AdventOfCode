with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

num_rows = len(lines)
num_cols = len(lines[0])


def parse():
    cubes = set()
    rounds = set()
    for i, line in enumerate(lines):
        for j, point in enumerate(line):
            if point == "O":
                rounds.add((i,j))
            if point == "#":
                cubes.add((i,j))
    return cubes, rounds


def part1():
    cubes, rounds = parse()
    rounds = roll_north(rounds, cubes)
    return calculate_load(rounds)


def part2():
    initial_cycles = 1000

    cubes, rounds = parse()
    loads = [calculate_load(rounds)]
    for _ in range(initial_cycles):
        rounds = roll_north(rounds, cubes)
        rounds = roll_west(rounds, cubes)
        rounds = roll_south(rounds, cubes)
        rounds = roll_east(rounds, cubes)
        loads.append(calculate_load(rounds))
   
    
    for c in range(1, 100):
        test_cycle = [*loads[-c:]*5]
        if loads[-len(test_cycle):] == test_cycle:
            break
    
    skip_cycles = (1000000000-initial_cycles)//c

    cycle = initial_cycles + skip_cycles * c
    while cycle < 1000000000:
        rounds = roll_north(rounds, cubes)
        rounds = roll_west(rounds, cubes)
        rounds = roll_south(rounds, cubes)
        rounds = roll_east(rounds, cubes)
        loads.append(calculate_load(rounds))
    return loads[-1]


def roll_north(rounds, cubes):
    new_rounds = set()
    for x, y in rounds:
        while (x, y) in new_rounds:
            # Another one rolled to this spot... weird
            x += 1
        # Move north => decrease x
        while x > 0 and (x-1, y) not in new_rounds and (x-1, y) not in cubes:
            x -= 1
        new_rounds.add((x, y))
    return new_rounds


def roll_south(rounds, cubes):
    new_rounds = set()
    for x, y in rounds:
        while (x, y) in new_rounds:
            # Another one rolled to this spot... weird
            x -= 1
        # Move south => increase x
        while x < num_rows - 1 and (x+1, y) not in new_rounds and (x+1, y) not in cubes:
            x += 1
        new_rounds.add((x, y))
    return new_rounds


def roll_east(rounds, cubes):
    new_rounds = set()
    for x, y in rounds:
        while (x, y) in new_rounds:
            # Another one rolled to this spot... weird
            y -= 1
        # Move east => increase y
        while y < num_rows - 1 and (x, y+1) not in new_rounds and (x, y+1) not in cubes:
            y += 1
        new_rounds.add((x, y))
    return new_rounds


def roll_west(rounds, cubes):
    new_rounds = set()
    for x, y in rounds:
        while (x, y) in new_rounds:
            # Another one rolled to this spot... weird
            y += 1
        # Move west => decrease x
        while y > 0 and (x, y-1) not in new_rounds and (x, y-1) not in cubes:
            y -= 1
        new_rounds.add((x, y))
    return new_rounds


def calculate_load(rounds):
    total_load = 0
    for x, y in rounds:
        total_load += num_rows - x
    return total_load


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
