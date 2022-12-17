with open("input.txt", "r") as f:
    stream = f.read().strip()

#stream = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

def rocks():
    order = ["-", "+", "_|", "|", "#"]
    i = 0
    while True:
        yield order[i%len(order)]
        i+=1


def direction(gust):
    if gust == ">":
        return (1, 0)
    if gust == "<":
        return (-1, 0)


def move(coord, direction):
    x, y = coord
    dx, dy = direction
    return x+dx, y+dy


class Rock:
    def __init__(self, shape, highest_other):
        start_x, start_y = (2, highest_other+4)
        if shape == "-":
            self.loc = [(x + start_x, y+start_y) for x, y in [(0, 0),(1,0),(2,0),(3,0)]]
        elif shape == "+":
            self.loc = [(x + start_x, y+start_y) for x, y in [(0, 1),(1,0),(1,1),(1,2),(2,1)]]
        elif shape == "_|":
            self.loc = [(x + start_x, y+start_y) for x, y in [(0, 0),(1,0),(2,0),(2,1),(2,2)]]
        elif shape == "|":
            self.loc = [(x + start_x, y+start_y) for x, y in [(0, 0),(0,1),(0,2),(0,3)]]
        elif shape == "#":
            self.loc = [(x + start_x, y+start_y) for x, y in [(0, 0),(0,1),(1,0),(1,1)]]

    def push(self, gust):
        d = direction(gust)
        new_loc = [move(l, d) for l in self.loc]
        return new_loc

    def fall(self):
        d = (0, -1)
        new_loc = [move(l, d) for l in self.loc]
        return new_loc
         
    def move(self, loc):
        self.loc = loc


class Chamber:
    def __init__(self):
        self.chamber = {}
        self.max_y = -1
        self.deltas = []

    def free(self, loc):
        for c in loc:
            x, y = c
            if not (0 <= x < 7) or y < 0:
                return False
            if c in self.chamber:
                return False
        return True

    def land(self, loc):
        prior_y = self.max_y
        for c in loc:
            self.chamber[c] = "#"
            self.max_y = max(self.max_y, c[1])
        self.deltas.append(self.max_y - prior_y)

    def __repr__(self):
        return f"{self.chamber}"

    
def find_cycle(deltas):
    deltas = deltas[500:]
    n = len(deltas)
    for cycle_len in range(1, n//2):
        pattern = deltas[:cycle_len]
        groups = n//cycle_len - 1
        matches = True
        for i in range(1, groups+1):
            to_match = deltas[i*cycle_len:(i+1)*cycle_len]
            if pattern != to_match:
                matches = False
                break
        if matches:
            return cycle_len, sum(pattern)


if __name__ == "__main__":
    chamber = Chamber()
    rocks_landed = 0
    step = 0
    for shape in rocks():
        if rocks_landed == 2022:
            print("Part 1:", chamber.max_y + 1)
        
        if rocks_landed == 10000:
            break
    
        rock = Rock(shape, chamber.max_y)
        while True:
            gust = stream[step%len(stream)]
            step += 1
            
            new = rock.push(gust)
            if chamber.free(new):
                rock.move(new)
    
            new = rock.fall()
            if chamber.free(new):
                rock.move(new)
            else:
                chamber.land(rock.loc)
                rocks_landed += 1
                break
           
    
    cycle_len, h = find_cycle(chamber.deltas)
    target_steps = 1000000000000
    cycles = target_steps // cycle_len
    initial_steps = target_steps - cycle_len * cycles
    print("Part 2:", sum(chamber.deltas[:initial_steps]) + cycles * h)

    # This is so ugly, but it works!!!
