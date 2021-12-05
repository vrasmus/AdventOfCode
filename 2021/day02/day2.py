with open('input.txt', 'r') as f:
    content = f.readlines()

moves = []
for line in content:
    tmp = line.split(" ")
    moves.append((tmp[0], int(tmp[1])))


depth = 0
pos = 0
for move, val in moves:
    if move == "forward":
        pos += val
    elif move == "down":
        depth += val
    else:
        depth -= val
print(depth*pos)


aim = 0
depth = 0
pos = 0
for move, val in moves:
    if move == "forward":
        pos += val
        depth += val * aim
    elif move == "down":
        aim += val
    else:
        aim -= val
print(depth*pos)
