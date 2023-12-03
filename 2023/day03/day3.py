def data():
    with open("input.txt", "r") as f:
        lines = [list(l.strip()) for l in f.readlines()]
    return lines


# Find all part numbers surrounding an origin point.
def find_part_numbers(lines, i, j):
    part_numbers = []
    possible_neighbors = [(1,0),(1,1),(1,-1),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    for di, dj in possible_neighbors:
        if lines[i+di][j+dj].isnumeric():
            find_part_number_extent(lines, i+di, j+dj, part_numbers)
    return part_numbers

# Find the entirety of a number that has presence at i,j.
# Mutates the input to avoid grabbign same numbers multiple times.
def find_part_number_extent(lines, i, j, part_numbers):
    left = j
    right = j
    while left > 0 and lines[i][left-1].isnumeric():
        left -= 1
    while right < len(lines[i])-1 and lines[i][right+1].isnumeric():
        right += 1

    number = int("".join(lines[i][left:right+1]))
    for k in range(left, right+1):
        lines[i][k] = "."
    part_numbers.append(number)


def part1():
    lines = data()
    all_part_numbers = []

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != "." and not char.isnumeric():
                part_numbers = find_part_numbers(lines, i,j)
                for num in part_numbers:
                    all_part_numbers.append(num)
    return sum(all_part_numbers)


def part2():
    lines = data()
    gear_ratios = []

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "*":
                part_numbers = find_part_numbers(lines, i,j)
                if len(part_numbers) == 2:
                    gear_ratios.append(part_numbers[0]*part_numbers[1])
    return sum(gear_ratios)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
