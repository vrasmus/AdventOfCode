with open("input.txt", "r") as f:
    patterns = [[row for row in grid.split("\n") if row] for grid in f.read().split("\n\n")]


def transpose(pattern):
    return ["".join([row[j] for row in pattern]) for j in range(len(pattern[0]))]


def dist(row1, row2):
    return sum([c1 != c2 for (c1, c2) in zip(row1, row2)])


def horizontal_value(pattern, target_dist):
    for i in range(len(pattern) - 1):
        total_dist = 0
        for row1, row2 in zip(pattern[i + 1:], pattern[i::-1]):
            total_dist += dist(row1, row2)
        if total_dist == target_dist:
            return i + 1
    return 0


def get_value(pattern, target_dist):
    return horizontal_value(pattern, target_dist) * 100 + horizontal_value(transpose(pattern), target_dist)


def solution(target_dist):
    return sum([get_value(pattern, target_dist) for pattern in patterns])


if __name__ == "__main__":
    print(f"Part 1: {solution(0)}")
    print(f"Part 2: {solution(1)}")
