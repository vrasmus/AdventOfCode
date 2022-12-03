with open("input.txt", "r") as f:
    data = f.read().strip()
rounds = [r.split(" ") for r in data.split("\n")]

STONE = "A"
PAPER = "B"
SCISSOR = "C"

def part1(them, key):
    if key == "X":
        return STONE
    if key == "Y":
        return PAPER
    if key == "Z":
        return SCISSOR


def part2(them, key):
    if key == "X":
        # Must lose.
        if them == STONE:
            return SCISSOR
        if them == PAPER:
            return STONE
        if them == SCISSOR:
            return PAPER
    if key == "Y":
        # Must draw
        return them
    if key == "Z":
        # Must win
        if them == STONE:
            return PAPER
        if them == PAPER:
            return SCISSOR
        if them == SCISSOR:
            return STONE

def score(them, key, handFunc):
    s = 0
    me = handFunc(them, key)
    if me == STONE:
        s += 1
    elif me == PAPER:
        s += 2
    elif me == SCISSOR:
        s += 3
    
    if me == them:
        return s + 3
    
    if me == STONE and them == SCISSOR:
        return s + 6
    if me == SCISSOR and them == PAPER:
        return s + 6
    if me == PAPER and them == STONE:
        return s + 6
    
    return s # loss

totalPart1 = 0
totalPart2 = 0
for them, key in rounds:
    totalPart1 += score(them, key, part1)
    totalPart2 += score(them, key, part2)

print("Part 1:", totalPart1)
print("Part 2:", totalPart2)
