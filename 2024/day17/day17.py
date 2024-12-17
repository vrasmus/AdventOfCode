FILE = "input.txt"

class Runner():
    def __init__(self, file):
        with open(file, "r") as f:
            content = [l.strip() for l in f.readlines()]
        self.A = int(content[0].split(": ")[-1])
        self.B = int(content[1].split(": ")[-1])
        self.C = int(content[2].split(": ")[-1])
        self.program = list(map(int, content[4].split(": ")[-1].split(",")))
        self.output = []
        self.ptr = 0
        self.halted = False


    def run(self):
        while not self.halted:
            self.operate()
        return ",".join(self.output)


    def operate(self):
        if self.ptr >= len(self.program) - 1:
            self.halted = True
            return

        instr, op = self.instruction()
        operand = op()
        instr(operand)
        self.ptr += 2


    def instruction(self):
        match self.program[self.ptr]:
            case 0:
                return self.adv, self.combo
            case 1:
                return self.bxl, self.literal
            case 2:
                return self.bst, self.combo
            case 3:
                return self.jnz, self.literal
            case 4:
                return self.bxc, self.literal # Literal ignored
            case 5:
                return self.out, self.combo
            case 6:
                return self.bdv, self.combo
            case 7:
                return self.cdv, self.combo


    def literal(self):
        return self.program[self.ptr + 1]


    def combo(self):
        val = self.program[self.ptr + 1]
        match val:
            case val if val < 4:
                return val
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise Exception("Invalid combo operand")


    def adv(self, combo):
        res = self.A // (2**combo)
        self.A = res


    def bxl(self, combo):
        res = self.B ^ combo
        self.B = res


    def bst(self, combo):
        self.B = combo % 8


    def jnz(self, combo):
        if self.A == 0:
            # Do nothing if A zero
            return
        self.ptr = combo
        self.ptr -= 2 # Will be increased again, keeps it steady.


    def bxc(self, combo):
        res = self.B ^ self.C
        self.B = res


    def out(self, combo):
        self.output.append(str(combo % 8))


    def bdv(self, combo):
        res = self.A // (2**combo)
        self.B = res


    def cdv(self, combo):
        res = self.A // (2**combo)
        self.C = res



def search():
    init = 106086382266778
    target = ",".join(map(str, Runner(FILE).program))
    while True:
        runner = Runner(FILE)
        runner.A = init
        output = runner.run()
        if len(output) < len(target):
            init *= 10
        if len(output) > len(target):
            return 
        if output == target:
            return init
        init += 1000000


print("Part 1:", Runner(FILE).run())
print("Part 2:", search())
