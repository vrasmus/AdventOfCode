class Part:
    def __init__(self, rating):
        categories = rating[1:-1].split(",")
        self.x = int(categories[0][2:])
        self.m = int(categories[1][2:])
        self.a = int(categories[2][2:])
        self.s = int(categories[3][2:])

    def __repr__(self):
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"

    def is_true(self, key, operator, value):
        val = None
        if key == "x":
            val = self.x
        if key == "m":
            val = self.m
        if key == "a":
            val = self.a
        if key == "s":
            val = self.s

        if operator == "<":
            return val < value
        if operator == ">":
            return val > value

        

def parse_step(s):
    if ":" not in s:
        return [s]
    last = s[2:].split(":")
    return [s[0], s[1], int(last[0]), last[1]]  


def run_workflow(steps, part):
    for step in steps:
        if len(step) == 1:
            return step[0]
        
        if part.is_true(step[0], step[1], step[2]):
            return step[3]


def part1():
    result = 0
    for part in parts:
        at = "in"
        while at not in "RA":
            at = run_workflow(workflows[at], part)
        if at == "A":
            result += part.x + part.m + part.a + part.s
    return result


with open("input.txt", "r") as f:
    unparsed_workflows, unparsed_parts = f.read().split("\n\n")
    parts = []
    for up in unparsed_parts.strip().split("\n"):
        parts.append(Part(up))

    workflows = {}
    for wf in unparsed_workflows.strip().split("\n"):
        wf_parts = wf[:-1].split('{')
        name = wf_parts[0]
        steps = [parse_step(s) for s in wf_parts[1].split(",")]
        workflows[name] = steps
       

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
