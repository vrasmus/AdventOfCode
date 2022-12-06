with open("input.txt", "r") as f:
    inStart, inMoves = f.read().split("\n\n")


def parse_start(data):
    lines = data.split("\n")[::-1][1:]
    stacks = [[] for i in range(9)]
    for line in lines:
        line = line[1::4]
        for i in range(len(line)):
            if line[i] != " ":
                stacks[i].append(line[i])
    return stacks


def parse_moves(data):
    moves = []
    for line in data.strip().split("\n"):
        print(line)
        from_split = line[5:].split(" from ")
        to_split = from_split[1].split(" to ")
        count = int(from_split[0])
        from_stack = int(to_split[0])
        to_stack = int(to_split[1])
        moves.append((count, (from_stack, to_stack)))
    return moves


def move_blocks(stacks, move):
    count, (src, dst) = move
    while count > 0:
        block = stacks[src-1].pop()
        stacks[dst-1].append(block)
        count -= 1


def move_blocks_jointly(stacks, move):
    count, (src, dst) = move
    moving = []
    while count > 0:
        block = stacks[src-1].pop()
        moving.append(block)
        count -= 1

    while moving:
        m = moving.pop()
        stacks[dst-1].append(m)


def top(stacks):
    return "".join([s[-1] for s in stacks])


if __name__ == "__main__":
    stacks = parse_start(inStart)
    stacks_copy = parse_start(inStart)
    moves = parse_moves(inMoves)

    for move in moves:
        move_blocks(stacks, move)
        move_blocks_jointly(stacks_copy, move)

    print("Part 1:", top(stacks))
    print("Part 2:", top(stacks_copy))
