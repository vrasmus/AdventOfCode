with open("input.txt", "r") as f:
    content = f.read().strip()

def fuelToMove(start, end, part2 = False):
    diff = abs(start-end)   
    if not part2:
        return diff
    return diff * (diff+1) // 2

def cost(position, counts, part2=False):
    total = 0
    for p in counts:
        total += counts[p]*fuelToMove(p, position, part2)
    return total

def solve(part2 = False):
    minFuel = 1e99
    for pos in range(min(positions), max(positions)+1):
        fuel = cost(pos, counts, part2)
        if fuel < minFuel:
            minFuel = fuel
    return minFuel

positions = list(map(int, content.split(",")))

counts = dict()
for pos in positions:
    counts[pos] = counts.get(pos, 0) + 1 

print(solve(False), solve(True))
