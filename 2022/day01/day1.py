with open("input.txt", "r") as f:
    data = f.read()

elfs = []
dataByElf = data.strip().split("\n\n")
for data in dataByElf:
    elfs.append(list(map(int, data.split("\n"))))

totals = [sum(calories) for calories in elfs]
print("Part 1:", max(totals))

totals = sorted(totals,reverse=True)
print("Part 2:", sum(totals[:3]))
