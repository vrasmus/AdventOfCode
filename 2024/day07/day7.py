with open("input.txt","r") as f:
    lines = [l.strip() for l in f.readlines()]
    targets = [int(l.split(":")[0]) for l in lines]
    equations = [list(map(int,l.split(":")[1].split())) for l in lines]


def can_work(target, equation, curr = 0, part2=False):
    if curr > target:
        return False

    if len(equation) == 0:
        return curr == target

    val = equation[0]
    next_eq = equation[1:]
    if part2 and curr > 0:
        if  can_work(target, next_eq, int(str(curr)+str(val)),part2):
            return True
    return can_work(target, next_eq, curr+val,part2) or can_work(target, next_eq, curr*val,part2) 

res1 = 0
res2 = 0
for target, equation in zip(targets, equations):
    if can_work(target, equation):
        res1 += target
    if can_work(target, equation, part2 = True):
        res2 += target

print("Part 1:", res1)
print("Part 2:", res2)


