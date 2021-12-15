import heapq

with open("input.txt", "r") as f:
    content = f.readlines()

grid = []
for line in content:
    grid.append(list(map(int,list(line.strip()))))

repeats = 5 
expGrid = []
for i in range(repeats):
    for line in grid:
        newLine = []
        for j in range(repeats):
            for element in line:
                newElement = element + i + j
                if newElement >= 10:
                    newElement = newElement%10 + 1
                newLine.append(newElement)
        expGrid.append(newLine)

def findShortestPath(grid):
    def add(i,j, cost):
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[i]):
            return
        heapq.heappush(queue, (grid[i][j]+cost,i,j))
    
    queue = []
    risks = {}
    add(0, 0, -grid[0][0])
    while queue:
        cost,i,j = heapq.heappop(queue)
        if (i,j) in risks:
            continue
        risks[(i,j)] = cost
        add(i+1, j, cost)
        add(i-1, j, cost)
        add(i, j+1, cost)
        add(i, j-1, cost)
    return risks[(len(grid)-1, len(grid[0])-1)]

print(findShortestPath(grid))
print(findShortestPath(expGrid))
