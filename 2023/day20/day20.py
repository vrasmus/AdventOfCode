class Node:
    def __init__(self, t, name, out):
        self.type = t
        self.name = name
        self.outputs = out.split(", ")
        self.inputs = []
        self.input_vals = None
        self.flip_flop_val = 0


    def __repr__(self):
        return
    #return f"{self.type}{self.name} -> {self.outputs}"


    def handle(self, i, pulse):
        if self.type == "$":
            # Button:
            return self.outputs, 0
        elif self.type == "@":
            # Broadcaster
            return self.outputs, pulse
        elif self.type == "%":
            # Flip-flop
            return self.handle_flip_flop(i, pulse)
        elif self.type == "&":
            return self.outputs, self.handle_conjunction(i, pulse)

        return [], 0

    def handle_flip_flop(self, i, pulse):
        if pulse == 1:
            return [], 0

        self.flip_flop_val = (self.flip_flop_val + 1) % 2
        return self.outputs, self.flip_flop_val


    def handle_conjunction(self, i, pulse):
        if not self.input_vals:
            self.input_vals = {}
            for node in self.inputs:
                self.input_vals[node] = 0
        self.input_vals[i] = pulse
        for val in self.input_vals.values():
            if val == 0:
                return 1
        return 0 # Remembers high for all.



nodes = {}
nodes["button"] = Node("$", "button", "broadcaster")
with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

    for line in lines:
        i, o = line.split(" -> ")
        if i == "broadcaster":
            i = "@broadcaster"
        t, name = i[0], i[1:]
        n = Node(t, name, o)
        nodes[name] = n


for n in nodes.values():
    for out in n.outputs:
        if out not in nodes:
            continue
        o = nodes[out]
        o.inputs.append(n.name)
        nodes[out] = o



pulses = [0, 0]
for _ in range(10000000000):
    # Res = 243081086866483
    queue = [("broadcaster", "button", 0)]
    while queue and i:
        dest, src, pulse = queue[0]
        queue = queue[1:]
        pulses[pulse] += 1
        if dest == "rx" and pulse == 0:
            print(_)
            break
        n = nodes.get(dest, Node("", "", ""))
        new_destinations, p = n.handle(src, pulse)
        for d in new_destinations:
            queue.append((d, dest, p))

    if _ == 999:
        print(pulses[0] * pulses[1])


