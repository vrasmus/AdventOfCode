with open("input.txt", "r") as f:
    content = f.readlines()

def parseCoord(coord):
    return tuple(map(int, coord.split(",")))

def parseLine(line):
    start, end = line.split(" -> ")
    return parseCoord(start), parseCoord(end)

lines = []
for line in content:
    lines.append(parseLine(line.strip()))

def solve(onlyHV):
    size = 1000
    diagram = [[0]*size for i in range(size)]
    for line in lines:
        dx = 1 if line[0][0] < line[1][0] else -1
        dy = 1 if line[0][1] < line[1][1] else -1
      
        if line[0][0] == line[1][0]:
            dx = 0
        if line[0][1] == line[1][1]:
            dy = 0
    
        if onlyHV and not (dx == 0 or dy == 0):
            continue
    
        x, y = line[0][0], line[0][1]
        while dx*x < dx*line[1][0] or dy*y < dy*line[1][1]:
            diagram[y][x] += 1
            x += dx
            y += dy
        diagram[y][x] += 1
    
    overlaps = 0
    for row in diagram:
        for val in row:
            if val > 1:
                overlaps += 1
    return overlaps

print(solve(True), solve(False))

