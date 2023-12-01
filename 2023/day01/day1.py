def part1():
    total = 0
    for line in lines:
        for i in range(len(lines)):
            if line[i].isnumeric():
                left = int(line[i])
                break

        for i in range(len(lines)):
            if line[-1-i].isnumeric():
                right = int(line[-1-i])
                break
        total += 10*left + right
    return total


def get_int(line, pos):
    if line[pos].isnumeric():
        return int(line[pos])

    if line[pos:pos+3] == "one":
        return 1
    if line[pos:pos+3] == "two":
        return 2
    if line[pos:pos+5] == "three":
        return 3
    if line[pos:pos+4] == "four":
        return 4
    if line[pos:pos+4] == "five":
        return 5
    if line[pos:pos+3] == "six":
        return 6
    if line[pos:pos+5] == "seven":
        return 7
    if line[pos:pos+5] == "eight":
        return 8
    if line[pos:pos+4] == "nine":
        return 9
    if line[pos:pos+4] == "zero":
        return 0


def part2():
    total = 0
    for line in lines:
        for i in range(len(line)):
            left = get_int(line, i)
            if left:
                break

        for i in range(len(line)-1, -1, -1):
            right = get_int(line, i)
            if right:
                break

        total += 10*left + right
    return total

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = [l.strip() for l in f.readlines()]

    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
