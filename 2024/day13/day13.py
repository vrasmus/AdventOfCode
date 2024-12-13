with open("input.txt", "r") as f:
    machines = [m.split() for m in f.read().split("\n\n")]
    
a = []
b = []
prize = []
for machine in machines:
    a.append((int(machine[2][2:-1]),int(machine[3][2:])))
    b.append((int(machine[6][2:-1]),int(machine[7][2:])))
    prize.append((int(machine[9][2:-1]),int(machine[10][2:])))
prize2 = [(p[0] + 10000000000000,p[1] + 10000000000000) for p in prize]


def cost(push_a, push_b):
    if push_a == None or push_b == None:
        return 1e99 # Inf
    return 3 * push_a + push_b


def brute_force(machine):
    best = 1e99
    for push_a in range(101):
        for push_b in range(101):
            x = a[machine][0] * push_a + b[machine][0] * push_b
            y = a[machine][1] * push_a + b[machine][1] * push_b
            if (x,y) == prize[machine]:
                best = min(best, cost(push_a, push_b))

    return best if best != 1e99 else None


def calc(a, b, prize):
    """
    [a_x a_y] [push_a] = [prize_x]
    [b_x b_y] [push_b]   [prize_y]
    """

    push_a = round((prize[1] - ((b[1] * prize[0]) / b[0])) / (a[1] - ((b[1] * a[0]) / b[0])))
    push_b = round((prize[0] - a[0] * push_a) / b[0])
    if a[0] * push_a + b[0] * push_b == prize[0] and a[1] * push_a + b[1] * push_b == prize[1]: 
        return cost(push_a, push_b)


part1 = 0
part2 = 0
for i in range(len(machines)):
    best1 = brute_force(i)
    if best1:
        part1 += best1
    best2 = calc(a[i], b[i], prize2[i])
    if best2:
        part2 += best2
print("Part 1:", part1)
print("Part 2:", part2)


