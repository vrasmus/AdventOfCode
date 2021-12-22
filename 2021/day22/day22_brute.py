with open("input.txt", "r") as f:
    content = f.readlines()

class Step:
    def __init__(self, line):
        tmp = line.strip().split(" ")
        self.on = 1 if tmp[0] == "on" else 0
        
        tmp = tmp[1].split(",")
        x = (tmp[0][2:].split(".."))
        y = (tmp[1][2:].split(".."))
        z = (tmp[2][2:].split(".."))
 
        self.xmin = int(x[0])
        self.ymin = int(y[0])
        self.zmin = int(z[0])
        self.xmax = int(x[1])
        self.ymax = int(y[1])
        self.zmax = int(z[1])

    def range(self):
        for x in range(max(-50,self.xmin), min(50,self.xmax)+1):
            for y in range(max(-50,self.ymin), min(50, self.ymax)+1):
                for z in range(max(-50,self.zmin), min(50,self.zmax)+1):
                    yield(x,y,z)

steps = []
for line in content:
    steps.append(Step(line))

cuboid = {}
for step in steps:
    for x, y, z in step.range():
        cuboid[(x,y,z)] = step.on

count = 0
for key in cuboid:
    count += cuboid[key]
print(count)
