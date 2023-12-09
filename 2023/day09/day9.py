with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    histories = [list(map(int, l.split())) for l in lines]


def extrapolate(sequence):
    if all([s == 0 for s in sequence]):
        return 0
    diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    return sequence[-1] + extrapolate(diffs)


def part1():
    result = 0
    for history in histories:
        result += extrapolate(history) 
    return result


def part2():
    result = 0
    for history in histories:
        result += extrapolate(history[::-1]) 
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
