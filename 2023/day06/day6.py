with open("input.txt","r") as f:
    content = [l.strip() for l in f.readlines()]
    times = list(map(int, content[0].split()[1:]))
    records = list(map(int, content[1].split()[1:]))


def ways_to_win(time, record):
    ways = 0
    for hold_time in range(0, time+1):
        speed = hold_time
        distance = speed * (time-hold_time)
        if distance > record:
            ways += 1
    return ways


def part1():
    result = 1
    for time, record in zip(times, records):
        result *= ways_to_win(time, record)
    return result


def part2():
    time = int("".join(content[0].split()[1:]))
    record = int("".join(content[1].split()[1:]))
    return ways_to_win(time, record)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
