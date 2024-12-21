with open("input.txt","r") as f:
    codes = f.read().strip().split()


UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
DIRECTIONS = {LEFT:"<", UP: "^", DOWN:"v", RIGHT: ">"}


def keypad_positions(keypad):
    positions = {}
    for i, row in enumerate(keypad):
        for j, item in enumerate(row):
            if item:
                positions[item] = (i,j)
    return positions


def shortest_path(keypad, at, to):
    queue = [(at, "")]
    while queue:
        _at, _path = queue[0]
        if _at == to:
            break
        queue = queue[1:]

        if not keypad.contains(_at):
            continue
        
        x, y = _at
        for (dx, dy), s in DIRECTIONS.items():
            queue.append(((x+dx,y+dy), _path + s))
   
    options = []
    while queue:
        _at, _path = queue[0]
        queue = queue[1:]
        if _at == to:
            options.append(_path)
        if len(options) > 0 and len(options[0]) < len(_path):
            continue

    
    best = None
    best_changes = 1e99
    for o in options:
        changes = 0
        for i in range(1, len(o)):
            if o[i] != o[i-1]:
                changes += 1

        if changes < best_changes:
            best = o
            best_changes = changes
    return best + "A"


class Keypad:
    def __init__(self, values, start):
        self.start = start
        self.keypad = values
        self.prepare()

    def prepare(self):
        self.start = self.at
        self.positions = keypad_positions(self.keypad)
        self.path_cache = {}        


    def path_to(self, target):
        t = self.positions[target] 
        if not (self.at, t) in self.path_cache:
            self.path_cache[(self.at, t)] = shortest_path(self, self.at, t)

        res = self.path_cache[(self.at,t)]
        self.at =    t
        return res


    def contains(self, loc):
        x, y = loc
        try:
            return self.keypad[x][y] != None
        except:
            return False


    def path(self, code):
        self.at = self.start
        result = []
        for num in code:
            p = self.path_to(num)
            result.append(p)
        return "".join(result)


class Numeric(Keypad):
    def __init__(self):
        self.at = (3,2)
        self.keypad = [
                [ "7", "8", "9"],
                [ "4", "5", "6"],
                [ "1", "2", "3"],
                [None, "0", "A"],
        ]
        self.prepare()


class Directional(Keypad):
    def __init__(self):
        self.at = (0,2)
        self.keypad = [
                [None, "^", "A"],
                [ "<", "v", ">"],
        ]
        self.prepare()


def best_moves_for_chain(chain):
    result = 0
    for code in codes:
        _code = code
        for keypad in chain:
            _code = keypad.path(_code)
        result += int(code[:-1]) * len(_code)
    return result


numeric = Numeric()
directional = Directional()
chain1 = [numeric, directional, directional]
chain2 = [numeric] + [directional] * 25

print("Part 1:", best_moves_for_chain(chain1))
print("Part 2:", best_moves_for_chain(chain2))
