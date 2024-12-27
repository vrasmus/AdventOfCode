with open("input.txt","r") as f:
    items = f.read().strip().split("\n\n")
    
    locks = []
    keys = []

    for item in items:
        pins = [-1] * 5
        for i, row in enumerate(item.split("\n")):
            for j, field in enumerate(row):
                if field == "#":
                    pins[j] += 1

        if item[0][0] == "#":
            locks.append(pins)
        else:
            keys.append(pins)

count = 0
for key in keys:
    for lock in locks:
        valid = True
        for pin1, pin2 in zip(key, lock):
            if pin1 + pin2 > 5:
                valid = False
                break
        if valid:
            count += 1

print("Part 1:", count)
