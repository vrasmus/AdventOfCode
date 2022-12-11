with open("input.txt", "r") as f:
    program = [l.strip() for l in f.readlines()]


def signal_strength(cycle, x):
    return cycle * x


def draw(screen, cycle, x):
    pos = cycle - 1
    row = pos // 40
    col = pos % 40
    if x-1 <= col <= x+1:
        screen[row][col] = "#"


def display(screen):
    lines = []
    for i in range(6):
        lines.append("".join(screen[i]))
    return "\n".join(lines)


def calculate_signal_strength_sum(x_history):
    signal_strength_sum = 0
    for cycle in range(20,240,40):
        tmp = cycle
        if tmp not in x_history:
            tmp -= 1
        curr = x_history.get(tmp)
        signal_strength_sum += signal_strength(cycle, curr)
    return signal_strength_sum


def run_program(program):
    cycle = 1
    x = 1
    screen = [["."]*40 for _ in range(6)]
    
    x_history = {}
    for op in program:
        draw(screen, cycle, x)
        cycle += 1
        if op != "noop":
            draw(screen, cycle, x)
            x += int(op.removeprefix("addx "))
            cycle += 1
        x_history[cycle] = x
    
    print("Part 1:", calculate_signal_strength_sum(x_history))
    print("Part 2:\n", display(screen)) 


if __name__ == "__main__":
    run_program(program)
