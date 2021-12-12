with open("input.txt", "r") as f:
    connectionList = [l.strip().split("-") for l in f.readlines()]

# form bidirectional cave connection dictionary
connections = dict()
for conn in connectionList:
    tmp = connections.get(conn[0], [])
    tmp.append(conn[1])
    connections[conn[0]] = tmp

    tmp = connections.get(conn[1], [])
    tmp.append(conn[0])
    connections[conn[1]] = tmp

# peform a dfs, keeping track of num visits to each cave
visits = dict()
paths = set()
def dfs(at, stack, doubleVisit):
    if at == "start" and len(stack) != 0:
        return
    
    stack.append(at)
    if at == "end":
        paths.add(tuple(stack))
        stack.pop()
        return
    
    visits[at] = visits.get(at, 0) + 1
    for to in connections.get(at,[]):
        if visits.get(to, 0) <= 0 or to.isupper():
            dfs(to, stack, doubleVisit)
            continue

        # for part 2 we can revisit ONE cave
        if visits.get(to, 0) == 1 and doubleVisit:
            dfs(to, stack, False)

    stack.pop()
    visits[at] -= 1

dfs("start", [], False)
print(len(paths))
dfs("start", [], True)
print(len(paths))
