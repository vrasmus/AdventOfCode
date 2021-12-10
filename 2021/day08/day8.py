with open("input.txt", "r") as f:
    content = f.readlines()

inputs = []
outputs = []
for line in content:
    tmp = line.strip().split(" | ")
    inputs.append(tmp[0].split(" "))
    outputs.append(tmp[1].split(" "))


# Part 1
count1378 = 0
for output in outputs:
    for val in output:
        if len(val) in [2,3,4,7]:
            count1378 += 1
print(count1378)

# Part 2


i, o = inputs[0], outputs[0]

def findMapping(inputs):    
    i = sorted(inputs, key=len)
    i = list(map(set, i))
    
    mapping = [""]*10
    # find easy ones
    mapping[1] = i[0]
    mapping[7] = i[1]
    mapping[4] = i[2]
    mapping[8] = i[9]
    
    aa = mapping[7].difference(mapping[1])
    
    for j in [6,7,8]:
        # Removing the 7 part leaves the 6 digit with 3 remaining but 0 and 9 with 4 remaining
        if len(i[j].difference(mapping[7])) == 4:
            mapping[6] = i[j]
    
        # Removing 4 and the top makes 1 part remain of the 9
        if len(i[j].difference(mapping[4].union(aa))) == 1:
            mapping[9] = i[j]

    # Only 1 remains with 6 parts
    for j in [6,7,8]:
        if i[j] != mapping[6] and i[j] != mapping[9]:
            mapping[0] = i[j]

    for j in [3,4,5]:
        # 2 shares only 4 segments with 9, others 5
        if len(mapping[9].intersection(i[j])) == 4:
            mapping[2] = i[j]

    for j in [3,4,5]:
        diff = len(i[j].difference(mapping[2]))
        if diff == 1:
            mapping[3] = i[j]
        if diff == 2:
            mapping[5] = i[j]

    reverse = dict()
    for i in range(10):
        key = "".join(sorted(mapping[i]))
        reverse[key] = i
    return reverse


res = 0
for i, out in zip(inputs, outputs):

    mapper = findMapping(i)
    val = ""
    for o in out:
        o = "".join(sorted(o))
        val += str(mapper[o])
    res += int(val)

print(res)
