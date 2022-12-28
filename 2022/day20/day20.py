with open("input.txt", "r") as f:
    nums = list(map(int, f.readlines()))


class Node:
    def __init__(self, val, prv=None, nxt=None):
        self.val = val
        self.prv = prv
        self.nxt = nxt


def move(node, list_length):
    if node.val == 0:
        return
    moves = node.val % (list_length-1)
    if node.val < 0:
        moves = -(-node.val % (list_length-1))
    
    dest = node
    node.prv.nxt, node.nxt.prv = node.nxt, node.prv
    if moves > 0:
        for _ in range(moves):
            dest = dest.nxt
    else:
        for _ in range(-moves+1):
            dest = dest.prv
    
    node.prv, node.nxt = dest, dest.nxt
    dest.nxt.prv, dest.nxt = node, node


def pprint(node):
    tmp = node
    res = [str(tmp.val)]
    while tmp.nxt != node:
        tmp = tmp.nxt
        res.append(str(tmp.val))
    print(" -> ".join(res))


def link(nodes):
    for i in range(len(nodes)-1):
        nodes[i+1].prv = nodes[i]
        nodes[i].nxt = nodes[i+1]
    nodes[-1].nxt = nodes[0]
    nodes[0].prv = nodes[-1]


def find_zero(node):
    while node.val != 0:
        node = node.nxt 
    return node


def grove_coordinate_sum(nodes):
    zero = find_zero(nodes[0])
    res = 0
    tmp = zero
    for i in range(3001):
        if i in [1000,2000,3000]:
            res += tmp.val
        tmp = tmp.nxt
    return res


def part1():
    nodes = []
    for num in nums:
        nodes.append(Node(num))
    link(nodes)
    
    for node in nodes:
        move(node, len(nodes))
    print("Part 1:", grove_coordinate_sum(nodes))


def part2():
    nodes = []
    for num in nums:
        nodes.append(Node(num * 811589153))
    link(nodes)
    
    for _ in range(10):
        for node in nodes:
            move(node, len(nodes))

    print("Part 2:", grove_coordinate_sum(nodes))


if __name__ == "__main__":
    part1()
    part2()
