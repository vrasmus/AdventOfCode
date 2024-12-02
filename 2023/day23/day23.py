import sys
sys.setrecursionlimit(25000)

with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

num_rows, num_cols = len(grid), len(grid[0])

def find_start():
    for col in range(num_cols):
        if grid[0][col] == ".":
            return (0, col)


def find_end():
    for col in range(num_cols):
        if grid[num_rows-1][col] == ".":
            return (num_rows-1, col)


def in_grid(r, c):
    return 0 <= r < num_rows and 0 <= col < num_cols


def next_positions_part1(pos):
    result = []
    for d in [UP, DOWN, LEFT, RIGHT]: 
        new_row = pos[0] + d[0]
        new_col = pos[1] + d[1]
        tile = grid[new_row][new_col]
        if tile == ".":
            result.append((new_row,new_col))
        if (tile == ">" and d == RIGHT) or \
            (tile == "<" and d == LEFT) or \
            (tile == "v" and d == DOWN) or \
            (tile == "^" and d == UP):
            result.append((new_row, new_col))
    return result 


def next_positions_part2(pos):
    result = []
    for d in [UP, DOWN, LEFT, RIGHT]: 
        new_row = pos[0] + d[0]
        new_col = pos[1] + d[1]
        tile = grid[new_row][new_col]
        if tile in ".><^v":
            result.append((new_row,new_col))
    return result 


def dfs(pos, step_generator, visited = set()):
    global longest,end
    if pos == end:
        if len(visited) > longest:
            print(len(visited))
        longest = max(longest, len(visited))
        return
    
    for p in step_generator(pos):
        if p in visited:
            continue
        
        visited.add(p)
        dfs(p, step_generator, visited)
        visited.remove(p)


if __name__ == "__main__":
    longest = 0
    start = find_start()
    end = find_end()
    dfs(start, next_positions_part1, set())
    print("Part 1:", longest)
    dfs(start, next_positions_part2, set())
    # This took like 2 hours to brute-force...
    print("Part 2:", longest)
