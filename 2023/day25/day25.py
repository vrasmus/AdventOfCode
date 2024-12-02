import networkx

G = networkx.Graph()

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    for line in lines:
        left, neighbors = line.split(": ")
        for right in neighbors.split():
            G.add_edge(left, right)

min_edge_cut = networkx.minimum_edge_cut(G)
print(min_edge_cut)
G.remove_edges_from(min_edge_cut)
component_sizes = [len(c) for c in networkx.connected_components(G)]
size1, size2 = component_sizes
print(size1*size2)
