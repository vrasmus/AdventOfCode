with open("input.txt", "r") as f:
    nums = [l.strip() for l in f.readlines()]


def single_to_decimal(snafu):
    match snafu:
        case "-":
            return -1
        case "=":
            return -2
        case _:
            return int(snafu)


def single_to_snafu(decimal):
    match decimal:
        case "-1":
            return "-"
        case "-2":
            return "="
        case _:
            return str(decimal)

def to_decimal(snafu):
    res = 0
    multiplier = 1
    for i in range(len(snafu)-1, -1, -1):
        res += single_to_decimal(snafu[i]) * multiplier
        multiplier *= 5
    return res


def to_snafu(decimal):
    if decimal == 0:
        return ""
    
    y = decimal // 5
    match x := decimal % 5:
        case 3:
            return to_snafu(1 + y) + "="
        case 4:
            return to_snafu(1 + y) + "-"
        case _:
            return to_snafu(y) + str(x)


if __name__ == "__main__":
    sums = sum([to_decimal(snafu) for snafu in nums])
    print("Part 1:", to_snafu(sums))
