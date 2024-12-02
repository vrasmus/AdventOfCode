with open("input.txt", "r") as f:
    lines = [list(map(int, l.strip().split())) for l in f.readlines()]


def max_diff(l):
    max_diff = 0
    prev = l[0]
    for curr in l[1:]:
        max_diff = max(max_diff, abs(curr-prev))
        prev = curr
    return max_diff

def is_increasing(l):
    prev = l[0]
    for curr in l[1:]:
        if curr <= prev:
            return False
        prev = curr
    return True

def is_decreasing(l):
    prev = l[0]
    for curr in l[1:]:
        if curr >= prev:
            return False
        prev = curr
    return True

def safe(l): 
    if max_diff(l) > 3:
        return False

    return is_decreasing(l) or is_increasing(l)

def safe_with_removal(l):
    for i in range(len(l)):
        tmp = l[:i] + l[i+1:]
        if safe(tmp):
            return True
    return False

res1 = 0
res2 = 0
for l in lines:
    if safe(l):
        res1 += 1
    if safe_with_removal(l):
        res2 += 1
print("Part 1:", res1)
print("Part 2:", res2)
