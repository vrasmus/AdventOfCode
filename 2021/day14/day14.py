with open("input.txt", "r") as f:
    content = f.read().strip().split("\n\n")
template = content[0]

rules = {}
for rule in content[1].split("\n"):
    s = rule.split(" -> ")
    rules[s[0]] = (s[0][0]+s[1], s[1]+s[0][1])

# To make computationally tractable (order doesn't matter) keep a map of pairs.
# All elements will appear twice (as first and last value of a pair.

pairs = {}
for i in range(len(template)):
    pair = template[i:i+2]
    pairs[pair] = pairs.get(pair, 0) + 1

def step(pairs):
    new = {}
    for pair in pairs:
        exp = rules.get(pair, [pair])
        for p in exp:
            new[p] = new.get(p, 0) + pairs[pair]
    return new

for _ in range(40):
    pairs = step(pairs)

# Count elements and find most/least common.
counter = {}
for key in pairs:
    counter[key[0]] = counter.get(key[0], 0) + pairs[key]

minVal = 1e99
maxVal = -1
for c in counter:
    maxVal = max(maxVal, counter[c])
    minVal = min(minVal, counter[c]) 
print(maxVal-minVal)
