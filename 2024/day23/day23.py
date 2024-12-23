with open("input.txt","r") as f:
    pairs = [l.strip().split("-") for l in f.readlines()]


adj = {}
for a, b in pairs:
    if a not in adj:
        adj[a] = set()
    if b not in adj:
        adj[b] = set()
    adj[a].add(b)
    adj[b].add(a)


def part1():
    triples = set()
    nodes = sorted(list(adj.keys()))
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            if a in adj[b] and b in adj[a]:
                for c in adj[a] & adj[b]:
                    triple = tuple(sorted([a,b,c]))
                    triples.add(triple)

    result = 0
    for a, b, c in triples:
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            result += 1
    return result


def biggest_component(nodes):
    if len(nodes) == 0:
        return []

    additions = adj[nodes[0]]
    for n in nodes:
        additions &= adj[n]

    best = nodes
    for a in list(additions):
        biggest_with = biggest_component(nodes + [a])
        if len(biggest_with) > len(best):
            best = biggest_with
    return sorted(best)


def part2():
    best = []
    for node in adj.keys():
        best_with_node = biggest_component([node])
        if len(best_with_node) > len(best):
            best = best_with_node
    return ",".join(best)


print("Part 1:", part1())
print("Part 2:", part2())
