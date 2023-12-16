import sys 

sys.setrecursionlimit(10000)

with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]
num_rows, num_cols = len(grid), len(grid[0])


DOWN, UP, RIGHT, LEFT = (1, 0), (-1, 0), (0, 1), (0, -1)


def count_energized(start, direction):
    visited = set()
    cached = set()
    
    def move(pos, direction):
        row, col = pos
        if not 0 <= row < num_rows:
            return
        if not 0 <= col < num_cols:
            return
        if (pos,direction) in cached:
            return
        
        cached.add((pos,direction))
        visited.add(pos)
    
        if grid[row][col] == ".":
            drow, dcol = direction
            new_pos = (row + drow, col + dcol)
            move(new_pos, direction)
    
        if grid[row][col] == "/":
            if direction == RIGHT: 
                drow, dcol = UP
            elif direction == LEFT:
                drow, dcol = DOWN
            elif direction == DOWN:
                drow, dcol = LEFT
            elif direction == UP:
                drow, dcol = RIGHT
    
            new_pos = (row + drow, col + dcol)
            move(new_pos, (drow, dcol))
        
        if grid[row][col] == "\\":
            if direction == RIGHT: 
                drow, dcol = DOWN
            elif direction == LEFT:
                drow, dcol = UP
            elif direction == DOWN:
                drow, dcol = RIGHT
            elif direction == UP:
                drow, dcol = LEFT
    
            new_pos = (row + drow, col + dcol)
            move(new_pos, (drow, dcol))
    
        if grid[row][col] == "|":
            if direction == UP or direction == DOWN:
                drow, dcol = direction
                new_pos = (row + drow, col + dcol)
                move(new_pos, direction)
            if direction == LEFT or direction == RIGHT:
                for direction in [UP, DOWN]:
                    drow, dcol = direction
                    new_pos = (row + drow, col + dcol)
                    move(new_pos, (drow, dcol))
    
        if grid[row][col] == "-":
            if direction == LEFT or direction == RIGHT:
                drow, dcol = direction
                new_pos = (row + drow, col + dcol)
                move(new_pos, direction)
            if direction == UP or direction == DOWN:
                for direction in [LEFT, RIGHT]:
                    drow, dcol = direction
                    new_pos = (row + drow, col + dcol)
                    move(new_pos, (drow, dcol))
    
    move(start, direction)
    return len(visited)



def part1():
    return count_energized((0,0), RIGHT)


def part2():
    max_energized = 0
    for row in range(num_rows):
        energized = count_energized((row, 0), RIGHT)
        max_energized = max(max_energized, energized)

        energized = count_energized((row, num_cols-1), LEFT)
        max_energized = max(max_energized, energized)

    for col in range(num_cols):
        energized = count_energized((0, col), DOWN)
        max_energized = max(max_energized, energized)
        
        energized = count_energized((num_rows-1, col), UP)
        max_energized = max(max_energized, energized)
    return max_energized


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

