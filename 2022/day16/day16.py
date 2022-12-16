with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]


class Valve:
    def __init__(self, name, flow, paths):
        self.name = name
        self.flow = flow
        self.paths = paths

    def __repr__(self):
        return f"{self.name}->{self.paths}"


def make_valve(line):
    equal_split = line.split("=")[1]
    flow = int(equal_split.split(";")[0])
    split = line.split(" ")
    name = split[1]
    paths = [s.removesuffix(",") for s in split[9:]]
    return Valve(name, flow, paths)


def all_shortest_paths(graph):
    # Floyd–Warshall algorithm
    T = {x: {y: 1 if y in graph[x].paths else float('+inf') for y in graph} for x in graph}
    for k in T:
        for i in T:
            for j in T:
                T[i][j] = min(T[i][j], T[i][k]+T[k][j])
    return T


def dfs(nonzero, shortest, node, steps, visited = [], score = 0, state={}):
    if steps <= 0:
        state[tuple(visited[1:])] = score
        return score
    if node in visited:
        state[tuple(visited[1:])] = score
        return score

    visited.append(node)
    best_score = 0
    for nz, flow in nonzero.items():
        dist = shortest[node][nz]
        tmp_score = score + nonzero.get(node,0)*steps
        nz_score = dfs(nonzero, shortest, nz, steps-dist-1, visited, tmp_score, state) 
        best_score = max(best_score, nz_score)
    visited.pop()
    return best_score


def part2(nonzero, shortest):
    # Same DFS as part 1, but track all possible paths that can be taken. Find 2 non-overlapping ones.
    state = {}
    dfs(nonzero, shortest, "AA", 26, state=state)
  
    # Pick the best path visiting each potential set of nodes
    best_states = {}
    for s,score in state.items():
        s = tuple(sorted(s))
        best_states[s] = max(best_states.get(s,0),score)

    # Look for the best pair of paths, that is the solution for part 2.
    best_pair = 0
    for human_path, hscore in best_states.items():
        for elephant_path, escore in best_states.items():
            valid = True
            for node in elephant_path:
                if node in human_path:
                    valid = False
                    break
            if valid:
                best_pair = max(best_pair, hscore+escore)
    return best_pair


if __name__ == "__main__":
    graph = {}
    for line in lines:
        v = make_valve(line)
        graph[v.name] = v

    # Prune non-zero edges and calculate all shortest paths between nodes in the graph
    nonzero = {x.name: x.flow for x in graph.values() if x.flow > 0}
    shortest = all_shortest_paths(graph)

    # Simple DFS to find best score for one user.
    print("Part 1:", dfs(nonzero, shortest, "AA", 30)) 
    print("Part 2:", part2(nonzero, shortest)) 
    
