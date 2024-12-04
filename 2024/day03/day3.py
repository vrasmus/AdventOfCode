import re

with open("input.txt", "r") as f:
    content = f.read()

def mul(s):
    parts = s.split(",")
    left = parts[0].split("(")[1]
    right = parts[1][:-1]
    return int(left)*int(right)

def sum_mul(s):
    matches = re.findall("mul\([0-9]+,[0-9]+\)", s)
    res = 0
    for m in matches:
        res += mul(m)
    return res

print("Part 1:", sum_mul(content))

do_not_split = re.split("don't()", content)
to_do = [do_not_split[0]] # Starts with an implicit do
for s in do_not_split[1:]:
    do_split = re.split("do()", s, 1)
    if len(do_split) > 2:
        to_do.append(do_split[2])
dont_removed = "".join(to_do)
print("Part 2:", sum_mul(dont_removed))
