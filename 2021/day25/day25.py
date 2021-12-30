with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
N, M = len(lines), len(lines[0])

east = set()
south = set()
for n in range(N):
    for m in range(M):
        if lines[n][m] == ">":
            east.add((n,m))
        elif lines[n][m] == "v":
            south.add((n,m))

def step(east, south):
    east = stepEast(east, south)
    south = stepSouth(east, south)
    return east, south

def stepEast(east, south):
    new = set()
    for pos in east:
        row, col = pos
        moveTo = (row, (col + 1) % M)
        if moveTo in east or moveTo in south:
            new.add(pos)
        else:
            new.add(moveTo)
    return new

def stepSouth(east, south):
    new = set()
    for pos in south:
        row, col = pos
        moveTo = ((row + 1) % N, col)
        if moveTo in east or moveTo in south:
            new.add(pos)
        else:
            new.add(moveTo)
    return new

steps = 0
oldEast, oldSouth = set(), set()
while east != oldEast or south != oldSouth:
    oldEast, oldSouth = east, south
    east, south = step(east, south)
    steps += 1
print(steps)
