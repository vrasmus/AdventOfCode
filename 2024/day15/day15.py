with open("input.txt","r") as f:
    content = f.read().split("\n\n")
    grid = [list(l) for l in content[0].split("\n")]
    moves = content[1].replace("\n","")

ROWS = len(grid)
COLS = len(grid[0])

walls = set()
boxes = set()
robot = None
for i, row in enumerate(grid):
    for j, field in enumerate(row):
        match field:
            case "#":
                walls.add((i,j))
            case "O":
                boxes.add((i,j))
            case "@":
                robot = (i,j)

DIRECTIONS = {
        "^": (-1, 0),
        "v": (1, 0),
        ">": (0, 1),
        "<": (0, -1),
    }


def move_boxes(first, d):
    if first not in boxes:
        # Nothing to move.
        return

    dx, dy = d
    nx, ny = first
    while (nx, ny) in boxes:
        nx, ny = nx + dx, ny + dy
    
    if (nx, ny) not in walls:
        boxes.remove(first)
        boxes.add((nx,ny))


def gps(x,y):
    return 100 * x + y


for move in moves:
    x, y = robot
    dx, dy = DIRECTIONS[move]
    nx, ny = x+dx, y+dy 

    move_boxes((nx,ny), DIRECTIONS[move]) 
    if (nx,ny) in boxes or (nx, ny) in walls:
        continue
    robot = (nx, ny)


print("Part 1:", sum(gps(*b) for b in boxes))
