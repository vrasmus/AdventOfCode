with open("input.txt", "r") as f:
    content = f.read()

def allRotations(x, y, z):
    return [(x, y, z), (x, z, -y), (-z, x, -y), 
            (z, -x, -y), (z, -y, x), (y, z, x),
            (-z, y, x), (-y, -z, x), (-y, x, z),
            (-x, -y, z), (y, -x, z), (-x, -z, -y),
            (-z, -x, y), (x, -z, y), (z, x, y),
            (-x, z, y), (-x, y, -z), (-y, -x, -z),
            (x, -y, -z), (y, x, -z), (y, -z, -x),
            (z, y, -x), (-y, z, -x), (-z, -y, -x)]

def diff(x, y):
    return x[0] - y[0], x[1] - y[1], x[2] - y[2]

def add(x,y):
    return x[0] + y[0], x[1] + y[1], x[2] + y[2]

class Scanner:
    def __init__(self, report):
        self.loc = None
        self.done = False
        self.known = []
        self.rotations = [set() for _ in range(24)]
        beacons = report.split("\n")[1:]
        for b in beacons:
            x, y, z = tuple(map(int, b.split(",")))
            for i, r in enumerate(allRotations(x,y,z)):
                self.rotations[i].add(r)

scanners = []
for group in content.split("\n\n"):
    scanners.append(Scanner(group.strip()))

# All scanner0's beacons are already known:
done = 1
scanners[0].loc = (0,0,0)
scanners[0].done = True
scanners[0].known = scanners[0].rotations[0]

while done < len(scanners):
    print(done)
    for scanner in scanners:
        if scanner.done:
            continue
        for rot in scanner.rotations:
            for ds in scanners:
                new = False
                for p1 in ds.known:
                    if new:
                        break
                    for p2 in rot:
                        d = diff(p1,p2)
                        overlap = 0
                        for p2 in rot:
                            p_ = add(p2, d)
                            if p_ in ds.known:
                                overlap += 1
                        if overlap >= 12:
                            loc = d
                            new = set()
                            for p2 in rot:
                                new.add(add(p2, d))
                if new != False:
                    scanner.done = True
                    scanner.known = new
                    scanner.loc = loc
                    done += 1
                    break

known = set()
for scanner in scanners:
    known = known.union(scanner.known)
print(len(known))

def manhattan(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])

dist = -1e99
for i in range(len(scanners)):
    for j in range(i+1, len(scanners)):
        dist = max(dist, manhattan(scanners[i].loc, scanners[j].loc))
print(dist)
