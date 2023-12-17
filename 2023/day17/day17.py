import heapq

with open("input.txt", "r") as f:
    grid = [list(map(int, l.strip())) for l in f.readlines()]
num_rows = len(grid)
num_cols = len(grid[0])


UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
DESTINATION = (num_rows - 1, num_cols - 1)


def in_grid(pos):
    row, col = pos
    if not 0 <= row < num_rows:
        return False
    if not 0 <= col < num_cols:
        return False
    return True


def part1():
    def potential_moves(pos, last_moves):
        moves = [UP, DOWN, LEFT, RIGHT]
        
        if len(last_moves) > 0:
            # Cannot reverse direction immediately
            last_move = last_moves[-1]
            if last_move == DOWN:
                moves.remove(UP)
            if last_move == UP:
                moves.remove(DOWN)
            if last_move == RIGHT:
                moves.remove(LEFT)
            if last_move == LEFT:
                moves.remove(RIGHT)
        
        if len(last_moves) >= 3:
            # Cannot continue more than 3 times in the same direction
            last_move = last_moves[-1]
            if last_move == last_moves[-2] == last_moves[-3]:
                moves.remove(last_move)
    
    
        valid_moves = []
        row, col = pos
        for move in moves:
            drow, dcol = move
            if in_grid((row+drow, col+dcol)):
                valid_moves.append(move)
        return valid_moves

    return best_path(potential_moves, 3)


def part2():
    def potential_moves(pos, last_moves):
        moves = [UP, DOWN, LEFT, RIGHT]
        
        if len(last_moves) > 0:
            # Cannot reverse direction immediately
            last_move = last_moves[-1]
            if last_move == DOWN:
                moves.remove(UP)
            if last_move == UP:
                moves.remove(DOWN)
            if last_move == RIGHT:
                moves.remove(LEFT)
            if last_move == LEFT:
                moves.remove(RIGHT)

            steps_without_turning = 0
            for move in last_moves[::-1]:
                if move != last_move:
                    break
                steps_without_turning += 1
           
            if steps_without_turning < 4: 
                moves = [last_move]

            if steps_without_turning >= 10:
                moves.remove(last_move) 
    
        valid_moves = []
        row, col = pos
        for move in moves:
            drow, dcol = move
            if in_grid((row+drow, col+dcol)):
                valid_moves.append(move)
        return valid_moves

    return best_path(potential_moves, 10)


def best_path(move_generator, step_lookback):
    visits = set()
    pos = (0, 0)

    queue = []
    heapq.heappush(queue, (0, pos, []))
    while queue:
        cost, pos, last_moves = heapq.heappop(queue)
        
        key = (pos, tuple(last_moves))
        if key in visits:
            continue
        visits.add(key)
        
        if pos == DESTINATION:
            break

        for move in move_generator(pos, last_moves):
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            new_cost = cost + grid[new_pos[0]][new_pos[1]]
            new_last_moves = last_moves[-(step_lookback-1):] + [move]
            heapq.heappush(queue, (new_cost, new_pos, new_last_moves))
    
    return cost 



if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
