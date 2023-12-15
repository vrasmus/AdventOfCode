with open("input.txt", "r") as f:
    sequence = f.read().strip().split(",")
    

def hash(string):
    digest = 0
    for char in string:
        digest += ord(char)
        digest *= 17
        digest %= 256
    return digest


def part1():
    result = 0
    for s in sequence:
        result += hash(s)
    return result


def operation(string, boxes):
    if "=" in string:
        label, val = string.split("=")
        return add(label, val, boxes)
    else:
        return rm(string[:-1], boxes)


def add(label, val, boxes):
    box = boxes[hash(label)]
    for i, lens in enumerate(box):
        if lens[0] == label:
            box[i] = (label, val)
            return
    box.append((label, val))
    return boxes


def rm(label, boxes):
    box = boxes[hash(label)]
    for i, lens in enumerate(box):
        if lens[0] == label:
            del box[i]
    return boxes


def focusing_power(boxes):
    result = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            result += (i+1) * (j+1) * int(lens[1])
    return result


def part2():
    boxes = [[] for _ in range(256)]
    for s in sequence:
        op = operation(s, boxes)
    return focusing_power(boxes)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

