with open("input.txt","r") as f:
    lines = [l.strip() for l in f.readlines()]
    cards = [l.split(": ")[1] for l in lines]
    cards = [c.split(' | ') for c in cards]
    winners = list(map(set, [map(int, c[0].split()) for c in cards]))
    numbers = list(map(list, [map(int, c[1].split()) for c in cards]))


def part1():
    result = 0
    for w, nums in zip(winners, numbers):
        value = 0
        for num in nums:
            if num in w:
                if value == 0:
                    value = 1
                else:
                    value *= 2
        result += value
    return result


def part2():
    num_cards = {}
    result = 0
    
    for this, (w, nums) in enumerate(zip(winners, numbers)):
        num_of_this = num_cards.get(this, 1)
        matches = 0
        for num in nums:
            if num in w:
                matches += 1

        for card in range(this+1, this+1+matches):
            count = num_cards.get(card, 1)
            num_cards[card] = count + num_of_this
        
        result += num_of_this
    
    return result


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

