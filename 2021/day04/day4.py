with open("input.txt") as f:
    content = f.read()
content = content[:-1]

class Board():
    def __init__(self):
        self.vals = dict()
        self.rows = [0]*5
        self.cols = [0]*5
        self.done = False

    def number(self, val):
        if self.done:
            return
        pos = self.vals.get(int(val), "")
        if pos != "":
            self.rows[pos[0]] += 1
            self.cols[pos[1]] += 1
            self.vals[int(val)] = None

    def check(self):
        if self.done:
            return

        for row in self.rows:
            if row == 5:
                self.done = True
                return True
        for col in self.cols:
            if col == 5:
                self.done = True
                return True
        return False
               
    def score(self):
        s = 0
        for val in self.vals:
            if self.vals[val] != None:
                s += val
        return s

def parse(board):
    new = Board()
    rows = board.split("\n")
    for i, row in enumerate(rows):
        for j in range(5):
            val = int(row[3*j:3*(j+1)])
            new.vals[val] = (i,j)
    return new

content = content.split("\n\n")
numbers = content[0]

boards = []
for board in content[1:]:
    boards.append(parse(board))

done = False
for num in numbers.split(","):
    for board in boards:
        board.number(num)
        if board.check():
            print(int(num)*board.score())
