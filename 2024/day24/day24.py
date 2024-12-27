class Gate:
    def __init__(self, desc):
        s = desc.split(" ")
        self.in1 = s[0]
        self.in2 = s[2]
        self.out = s[4]
        self.op = s[1]
        self.val = None

    def __repr__(self):
        return f"{self.in1} {self.op} {self.in2} -> {self.out}"

    def __call__(self, a, b):
        match self.op:
            case "AND":
                return a & b
            case "OR":
                return a | b
            case "XOR":
                return a ^ b
        

with open("input.txt", "r") as f:
    content = f.read().strip().split("\n\n")
    inputs = {}
    for line in content[0].split("\n"):
        key, val = line.split(": ")
        inputs[key] = int(val)

    outputs = []
    gates = {}
    for line in content[1].split("\n"):
        g = Gate(line)
        gates[g.out] = g
        if g.out.startswith("z"):
            outputs.append(g.out)
    outputs.sort()


def evaluate(g):
    if g in inputs:
        return inputs[g]
    node = gates[g]
    if node.val == None:
        node.val = node(evaluate(node.in1), evaluate(node.in2))
    return node.val

    
def solve(gates):
    binary = []
    for o in reversed(outputs):
        binary.append(evaluate(o))

    res = 0
    for v in binary:
        res = res << 1 
        res = res | v
    return res

print("Part 1:", solve(gates))
