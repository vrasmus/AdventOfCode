with open("input.txt", "r") as f:
    content = f.read()

content = content.split("\n\n")
alg = content[0].strip()

img = {}
for i, line in enumerate(content[1].split("\n")):
    for j, char in enumerate(line.strip()):
        img[(i,j)] = char

# The outside edge may flip each time. Keep track of what it is "far away"
x = 1000000000
img[(x,x)] = "."

def binval(i, j):
    b = 0
    for i_ in [i-1, i, i+1]:
        for j_ in [j-1, j, j+1]:
            b <<= 1
            b += 1 if img.get((i_, j_), img[(x,x)]) == "#" else 0
    return b

def enhance(img):
    mini, minj, maxi, maxj = 1e99,1e99,-1e99,-1e99
    for key in img:
        if key == (x,x):
            continue
        i, j = key
        mini = min(mini, i)
        maxi = max(maxi, i)
        minj = min(minj, i)
        maxj = max(maxj, i)

    new = {}
    for i in range(mini-2, maxi+3):
        for j in range(minj-2, maxj+3):
            b = alg[binval(i, j)]
            new[(i,j)] = b
    new[(x,x)] = alg[binval(x, x)]
    return new

def lit(img):
    count = 0
    for key in img:
        count += 1 if img[key] == "#" else 0
    return count

for _ in range(1, 51):
    img = enhance(img)
    if _ in [2, 50]:
        print(lit(img))
