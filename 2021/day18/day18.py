with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

class Num:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        if self.val != None:
            return self.val
        return "({},{})".format(self.left.__repr__(), self.right.__repr__())

    def explode(self, level = 1):
        global exploded, mustExplode, prior
        if mustExplode and self.val != None:
            self.val += mustExplode
            mustExplode = 0
        
        if self.val != None:
            prior = self

        if not exploded and level == 5 and self.left:
            exploded = True
            if prior:
                prior.val += self.left.val
            mustExplode = self.right.val
            self.left, self.right, self.val = None, None, 0

        if self.left:
            self.left.explode(level+1)
        if self.right:
            self.right.explode(level+1)
       
    def split(self):
        global hasSplit

        if hasSplit:
            return

        if self.val and self.val >= 10:
            self.left = Num(self.val//2)
            self.right = Num(self.val//2 + self.val%2)
            self.val = None
            hasSplit = True

        if self.left:
            self.left.split()
        if self.right:
            self.right.split()

    def magnitude(self):
        if self.val != None:
            return self.val
        return 3*self.left.magnitude() + 2*self.right.magnitude()

def add(x, y):
    global exploded, prior, hasSplit, mustExplode
    z = Num(left = x, right = y)
    
    while True:
        mustExplode, prior, exploded, hasSplit = None, None, False, False
        z.explode()
        while exploded:
            mustExplode, prior, exploded, hasSplit = None, None, False, False
            z.explode()
        mustExplode, prior, exploded, hasSplit = None, None, False, False
        z.split()
        if not hasSplit:
            break
    
    return z


def parseNum(x):
    if len(x) == 1:
        return Num(val=int(x)) 
    if len(x) == 5:
        return Num(left=parseNum(x[1]), right=parseNum(x[3]))

    if x[1] == "[":
        o = 1
        for i in range(1, len(x)):
            if x[i] not in ["[", "]"]:
                continue
            if x[i] == "[":
                o += 1
            if x[i] == "]":
                o -= 1
            if o == 1:
                return Num(left=parseNum(x[1:i+1]), right=parseNum(x[i+2:-1]))
    else:
        return Num(left=parseNum(x[1]), right=parseNum(x[3:-1]))

nums = []
for line in lines:
    nums.append(parseNum(line))

mustExplode, prior, exploded, hasSplit = None, None, False, False
res = nums[0]
for num in nums[1:]:
    res = add(res, num)
print(res, res.magnitude())

maxval = -1
for i in range(len(lines)):
    for j in range(len(lines)):
        if i == j:
            continue
        m1 = add(parseNum(lines[i]), parseNum(lines[j])).magnitude()
        maxval = max(maxval, m1)
print(maxval)

