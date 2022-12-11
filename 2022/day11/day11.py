with open("input.txt", "r") as f:
    monkey_texts = f.read().split("\n\n")


class Monkey:
    def __init__(self, items, op, test, worry_func=lambda x: x//3):
        self.items = items
        self.op = op
        self.test = test
        self.inspections = 0
        self.worry_func = worry_func

    def test_items(self):
        for item in self.items:
            self.inspections += 1
            item = self.op(item) 
            item = self.worry_func(item)
            yield item, self.test(item)
        self.items = []

    def catch(self, item):
        self.items.append(item)

    def __repr__(self):
        return "{} inspections, items: {}".format(self.inspections, self.items)


def parse_items(text):
    text = text.strip().removeprefix("Starting items: ")
    return list(map(int, text.split(",")))


def parse_operation(text):
    optext = text.strip().removeprefix("Operation: new = ")
    if optext == "old * old":
        return lambda x: x*x
    parts = optext.split(" ")
    val = int(parts[-1])
    if parts[1] == "+":
        return lambda x: x+val
    if parts[1] == "*":
        return lambda x: x*val


def parse_test(text):
    val = [int(t.split(" ")[-1]) for t in text]
    return lambda x: val[1] if x % val[0] == 0 else val[2]


def parse_monkey(text, worry_func):
    lines = text.split("\n")
    items = parse_items(lines[1])
    op = parse_operation(lines[2])
    test = parse_test(lines[3:6])
    return Monkey(items, op, test, worry_func)


def run(rounds, worry_func):
    monkeys = [parse_monkey(text, worry_func) for text in monkey_texts]
    
    for _ in range(rounds):
        for monkey in monkeys:
            for item, to in monkey.test_items():
                monkeys[to].catch(item)

    activity = [m.inspections for m in monkeys]
    activity.sort()
    return activity[-2]*activity[-1]


if __name__ == "__main__":
    print("Part 1:", run(20, worry_func=lambda x: x//3))

    test_prod = 11*17*5*13*19*2*3*7 # Modulo this won't change any tests
    print("Part 2:", run(10000, worry_func=lambda x: x%test_prod))
