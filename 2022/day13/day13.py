with open("input.txt", "r") as f:
    raw = f.read().strip()
    pairs = [p.split("\n") for p in raw.split("\n\n")]


def compare(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    
    for l, r in zip(left, right):
        if isinstance(l, list) or isinstance(r, list):
            cmp = compare(l, r)
            if cmp != 0:
                return cmp
        elif r - l != 0:
            return r - l

    return len(right) - len(left)


def compare_str(left, right):
    return compare(eval(left), eval(right))


# Very simple O(n^2) sorting algorithm
def sort(items):
    sorted_list = []
    for item in items:
        i = 0
        while i < len(sorted_list) and compare_str(item, sorted_list[i]) < 0:
            i += 1
        sorted_list = sorted_list[:i] + [item] + sorted_list[i:]
    return sorted_list
   

if __name__ == "__main__":
    part1 = 0
    for i, pair in enumerate(pairs):
        if compare_str(*pair) > 0:
            part1 += 1+i 
    print("Part 1:", part1)
    
    items = [p for pair in pairs for p in pair] + ["[[2]]", "[[6]]"]
    items = sort(items)
    
    part2 = 1
    for i, item in enumerate(items):
        if item in ("[[2]]", "[[6]]"):
            part2 *= 1 + i
    print("Part 2:", part2)
