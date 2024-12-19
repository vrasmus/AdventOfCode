with open("input.txt","r") as f:
    content = f.read().strip().split("\n\n")
    towels = content[0].split(", ")
    patterns = content[1].split("\n")


cache = {}
def ways_to_make(pattern):
    if len(pattern) == 0:
        return 1
    if pattern in cache:
        return cache[pattern]
    
    ways = 0
    for t in towels:
        if len(t) > len(pattern):
            continue
        if not pattern[:len(t)] == t:
            continue
        ways += ways_to_make(pattern[len(t):])
    cache[pattern] = ways
    return ways


result1 = 0
result2 = 0
for p in patterns:
    ways = ways_to_make(p)
    result1 += 1 if ways > 0 else 0
    result2 += ways
print("Part 1:", result1)
print("Part 2:", result2)
