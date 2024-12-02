import sympy
from sympy.abc import t, s

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"{self.x},{self.y},{self.z}"


with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    
    hails = []
    for line in lines:
        pos, vel = line.split(" @ ")
        p = tuple(map(int, pos.split(",")))
        v = tuple(map(int, vel.split(",")))
        hails.append((Point(*p),Point(*v)))
       

def intersection(hail_a, hail_b):
    a, va = hail_a
    b, vb = hail_b

    solution = sympy.solve([
        a.x + t*va.x - (b.x + s*vb.x),
        a.y + t*va.y - (b.y + s*vb.y)
    ])

    if t in solution:
        t_sol = solution[t]
        s_sol = solution[s]
        if t_sol < 0 or s_sol < 0:
            return None
        return Point(a.x + t_sol*va.x, a.y + t_sol*va.y, None)
    return None


def in_test_area(p):
    return 200000000000000 <= p.x <= 400000000000000 \
            and 200000000000000 <= p.y <= 400000000000000


def part1():
    result = 0
    for i, hail in enumerate(hails):
        for other in hails[i+1:]:
            i = intersection(hail, other)
            if i and in_test_area(i):
                result += 1
    return result


def part2():
    from sympy.abc import x, y, z, a, b, c, t, s, u
    
    # 9 equations, 9 unknowns:
    #   - 3 variables from start position
    #   - 3 variables from throw velocity
    #   - 3 variables from collision time with 3 hails.

    p1, v1 = hails[0]
    p2, v2 = hails[1]
    p3, v3 = hails[2]
    equations = [
        p1.x + t*v1.x - (x + t*a),
        p1.y + t*v1.y - (y + t*b),
        p1.z + t*v1.z - (z + t*c),
        p2.x + s*v2.x - (x + s*a),
        p2.y + s*v2.y - (y + s*b),
        p2.z + s*v2.z - (z + s*c),
        p3.x + u*v3.x - (x + u*a),
        p3.y + u*v3.y - (y + u*b),
        p3.z + u*v3.z - (z + u*c),
    ]
    solution = sympy.solve(equations)[0]
    return solution[x] + solution[y] + solution[z]

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
