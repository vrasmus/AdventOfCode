with open("input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]


def priority(char):
    o = ord(char)
    if ord('A') <= o <= ord('Z'):
        return o - ord('A') + 27
    return o - ord('a') + 1


def common_elements(*args):
    if len(args) == 0:
        return []
    common = set(args[0])
    for a in args[1:]:
        common = common.intersection(a)
    return common if len(common) > 1 else list(common)[0]


totalPart1 = 0
for rucksack in data:
    n = len(rucksack)
    c1, c2 = rucksack[:n//2], rucksack[n//2:]
    overlapping = common_elements(c1, c2)
    totalPart1 += priority(overlapping)

totalPart2 = 0
for group in range(len(data)//3):
    rucksacks = data[group*3:(group+1)*3]
    common = common_elements(*rucksacks)
    totalPart2 += priority(common)
    
print("Part 1:", totalPart1)
print("Part 2:", totalPart2)
