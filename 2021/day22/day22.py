with open("input.txt", "r") as f:
    content = f.readlines()

def parse(line):
    tmp = line.strip().split(" ")
    on = 1 if tmp[0] == "on" else -1
    
    tmp = tmp[1].split(",")
    x = (tmp[0][2:].split(".."))
    y = (tmp[1][2:].split(".."))
    z = (tmp[2][2:].split(".."))
    
    return Cube(on, (int(x[0]), int(x[1])), (int(y[0]), int(y[1])), (int(z[0]), int(z[1])))

def intersection(a, b):
    left = max(a[0], b[0])
    right = min(a[1], b[1])
    return None if right <= left else (left, right)

class Cube:
    def __init__(self, sign, x, y, z):
        self.sign = sign
        self.x = x
        self.y = y
        self.z = z

    def intersection(self, other):
        x = intersection(self.x, other.x)
        y = intersection(self.y, other.y)
        z = intersection(self.z, other.z)
        if x and y and z:
            sign = -other.sign
            return Cube(sign, x, y, z)
        return None

    def size(self):
        x = self.x[1] - self.x[0] + 1
        y = self.y[1] - self.y[0] + 1
        z = self.z[1] - self.z[0] + 1
        return self.sign * x*y*z

    def __repr__(self):
        return "{},{},{}:{}".format(self.x,self.y,self.z, self.sign)


# For every step, we identify all currently processed cubes that it intersects with.
# This allows us to remove the effect of the prior cubes first, then if the new
# cube is an 'on' cube, we add it.

steps = []
for line in content:
    steps.append(parse(line))

res = [steps[0]]
for i, step in enumerate(steps):
    for cube in res.copy():
        overlap = step.intersection(cube)
        if overlap:
            res.append(overlap)
    if step.sign == 1:
        res.append(step)

    if i == 19 or i == len(steps) - 1:
        count = 0
        for cube in res:
             count += cube.size()
        print(count)
