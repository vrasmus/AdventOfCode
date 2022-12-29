with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]


def evaluate(op, num1, num2):
    match op:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            return num1 / num2


def yell(monkeys, name):
    job = monkeys[name.strip()]
    if job.isnumeric():
        result = int(job)
    else:
        op = job[5]
        monkey1, monkey2 = job.split(op)
        result = evaluate(op, yell(monkeys, monkey1), yell(monkeys, monkey2))
    return result


def part2(monkeys):
    rootjob = monkeys["root"]
    left, right = rootjob[:4], rootjob[-4:]

    # Binary search to find the correct number to yell...
    lsearch, rsearch = 0, 10000000000000
    while lsearch < rsearch:
        guess = (rsearch + lsearch) // 2
        monkeys["humn"] = str(guess)
        lres, rres = yell(monkeys, left), yell(monkeys, right)
        if lres == rres:
            return guess
        elif lres > rres:
            lsearch = guess + 1
        else:
            rsearch = guess - 1


if __name__ == "__main__":
    monkeys = {}
    for l in lines:
        name, job = l.split(": ")
        monkeys[name] = job
    
    print("Part 1:", int(yell(monkeys, "root")))
    print("Part 2:", part2(monkeys))
