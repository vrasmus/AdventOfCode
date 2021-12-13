with open("input.txt", "r") as f:
    content = f.read().strip()
    content = content.split("\n\n")

coords = []
for line in content[0].split("\n"):
    line.strip()
    line = line.split(",")
    coords.append((int(line[0]), int(line[1])))
coords = set(coords)

folds = []
for line in content[1].split("\n"):
    line.strip()
    line = line[11:].split("=")
    folds.append((line[0], int(line[1])))

def foldAlongX(inCoords, x):
    out = set()
    for x_, y_ in inCoords:
        new = (x_, y_)
        if x_ > x:
            diff = x_ - x
            new = (x_ - 2*diff, y_)
        out.add(new)
    return out

def foldAlongY(inCoords, y):
    out = set()
    for x_, y_ in inCoords:
        new = (x_, y_)
        if y_ > y:
            diff = y_ - y
            new = (x_, y_ - 2*diff)
        out.add(new)
    return out

for fold in folds:
    if fold[0] == "x":
        coords = foldAlongX(coords, fold[1])
    if fold[0] == "y":
        coords = foldAlongY(coords, fold[1])
    print(len(coords))

draw = [["."]*40 for _ in range(6)] 
for x,y in coords:
    draw[y][x] = "#"

for line in draw:
    print("".join(line))
