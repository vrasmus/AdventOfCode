with open("input.txt", "r") as f:
    grid = [list(l.strip()) for l in f.readlines()]

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)


num_rows = len(grid)
num_cols = len(grid[0])

for row in range(num_rows):
    for col in range(num_cols): 
        if grid[row][col] == "S":
            start = (row, col)
            break
grid[row][col] = "."


queue = [(start, 0, 1)]
steps_taken = 0
while steps_taken + 1 <= 64:
    steps_taken = queue[0][1]
    next_positions = {}
    for queue_item in queue:
        (curr_pos_row, curr_pos_col), steps, ways = queue_item
        for drow, dcol in [UP, DOWN, LEFT, RIGHT]:
            r, c = curr_pos_row + drow, curr_pos_col + dcol
            if grid[r][c] in "S.":
                next_positions[(r,c)] = next_positions.get((r, c), 0) + ways
    queue = []

    for pos, ways in next_positions.items():
        queue.append((pos, steps_taken + 1, ways)) 

    if steps_taken + 1 in [64]:
        print(steps_taken + 1, len(next_positions))
