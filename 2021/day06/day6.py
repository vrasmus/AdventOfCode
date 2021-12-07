with open("input.txt") as f:
    content = f.read().strip()

fish = map(int, content.split(","))

counts = dict()

for time in fish:
    counts[time] = counts.get(time, 0) + 1

num_days = 256
for _ in range(num_days):
    new = dict()
    for i in range(0,8):
        new[i] = counts.get(i+1, 0)
    spawning = counts.get(0,0)
    new[6] += spawning
    new[8] = spawning
    counts = new 

total = 0
for i in counts:
    total += counts[i]

print(total)

