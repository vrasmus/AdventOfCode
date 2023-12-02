with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    games = [l.split(": ")[1] for l in lines]
    games = [g.split("; ") for g in games]


def part1():
    bag = {"red": 12, "green":13, "blue":14}

    def is_possible(game):
        for grab in game:
            for counts in grab.split(", "):
                num, color = counts.split(" ")
                num = int(num)
                if num > bag[color]:
                    return False
        return True
    
    result = 0
    for i, game in enumerate(games):
        if is_possible(game):
            result += 1 + i
    return result


def part2():
    result = 0
    for game in games:
        mins = {}
        for grab in game:
            for counts in grab.split(", "):
                num, color = counts.split(" ")
                num = int(num)
                mins[color] = max(mins.get(color, 0), num)
        result += mins.get("red",0) * mins.get("green",0) * mins.get("blue",0)
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
