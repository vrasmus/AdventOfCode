with open("input.txt","r") as f:
    fs = list(map(int, f.read().strip()))


def part1():
    _fs = fs[:]
    left, right = 0, len(fs) - 1
    checksum = 0
    idx = 0
    block_empty = False
    while left <= right:
        while _fs[left] > 0:
            if not block_empty:
                checksum += left//2*idx
            else:
                checksum += right//2*idx
                _fs[right] -= 1
                if _fs[right] == 0:
                    right -= 2 # Skip empty
            _fs[left] -= 1
            idx += 1
        block_empty = not block_empty
        left += 1
    return checksum


# This is pretty ugly, but it works...
def part2():
    _fs = fs[:]
    left, right = 0, len(fs) - 1
    checksum = 0
    idx = 0
    block_empty = False
    while left <= right:
        while _fs[left] > 0:
            if not block_empty:
                checksum += left//2*idx
                _fs[left] -= 1
                idx += 1
            else:
                to_pack = right
                while _fs[to_pack] == 0 or _fs[to_pack] > _fs[left]: 
                    # It does not fit.
                    to_pack -= 2 # Skip empty.
                if to_pack <= left:
                    # Nothing fits at the left spot.
                    while _fs[left] > 0:
                        _fs[left] -= 1
                        idx += 1
                    break
                while _fs[to_pack] > 0:
                    checksum += to_pack//2*idx
                    _fs[left] -= 1
                    _fs[to_pack] -= 1
                    idx += 1
                if _fs[right] == 0:
                    right -= 2 # Skip empty

        block_empty = not block_empty
        left += 1
        if _fs[left] == 0 and fs[left] > 0:
            # was moved earlier, need to skip over now-empty spots...
            idx += fs[left]
    return checksum


print("Part 1:", part1())
print("Part 2:", part2())

