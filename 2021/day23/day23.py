cspots = [0,1,3,5,7,9,10] # Spots to stop in corridor

roomLocs = [2,4,6,8]
keys = ["A","B","C","D"]
properRoom = {"A":0,"B":1,"C":2,"D":3}
targets = {"A":2,"B":4,"C":6,"D":8}
costs = {"A":1,"B":10,"C":100,"D":1000}


def ready(room, key):
    for k in room:
        if k != key:
            return False
    return True

def done(room, key):
    if len(room) != MAX_ROOM_NUM: 
        return False
    for k in room:
        if k != key:
            return False
    return True

def copy(rooms, corridor):
    return [room[:] for room in rooms], corridor[:]
    #newRooms = list(map(list, map(tuple, rooms)))
    #newCorridor = list(tuple(corridor))
    #return newRooms, newCorridor

def outMoves(rooms, corridor):
    for i in range(4):
        if done(rooms[i], keys[i]):
            continue
        if len(rooms[i]) == 0:
            continue

        moved = 1 + MAX_ROOM_NUM - len(rooms[i]) # To move up
        top = rooms[i].pop()
        for pos in range(roomLocs[i]-1, -1, -1):
            if corridor[pos] != ".":
                break
            r, c = copy(rooms, corridor)
            c[pos] = top
            steps = moved + roomLocs[i] - pos
            yield steps*costs[top], r, c
        for pos in range(roomLocs[i]+1, len(corridor)):
            if corridor[pos] != ".":
                break
            r, c = copy(rooms, corridor)
            c[pos] = top
            steps = moved + pos - roomLocs[i]
            yield steps*costs[top], r, c
        rooms[i].append(top)
        
def canMoveTo(loc, target, corridor):
    for d in range(loc, target, -1 if target<loc else 1):
        if d == loc:
            continue
        if corridor[d] != ".":
            return False
    return True

def inMoves(rooms, corridor):
    for c in cspots:
        this = corridor[c]
        if this != ".":
            goalRoom = rooms[properRoom[this]]
            if not ready(goalRoom, this):
                continue
            target = targets[corridor[c]]
            if canMoveTo(c, target, corridor):
                steps = max(c - target, target - c) 
                steps = steps + MAX_ROOM_NUM - len(goalRoom)

                goalRoom.append(this)
                r_, c_ = copy(rooms, corridor)
                c_[c] = "."
                yield costs[this]*steps, r_, c_
                goalRoom.pop()
                

def complete(rooms):
    for room in rooms:
        if len(room) != MAX_ROOM_NUM:
            return False

    for room, key in zip(rooms, keys):
        if not done(room, key):
            return False
    return True

MAX_ROOM_NUM = 4 # 2 for part 1, 4 for part 2

corridor = ["."]*11
#rooms = [["A", "B"], ["D", "C"], ["C","B"], ["A", "D"]]
#rooms = [["B", "D"], ["C", "D"], ["A","B"], ["C", "A"]]
#rooms = [["A", "D", "D", "B"], ["D", "B", "C", "C"], ["C", "A", "B", "B"], ["A", "C", "A", "D"]]
rooms = [["B", "D", "D", "D"], ["C", "B", "C", "D"], ["A", "A", "B", "B"], ["C", "C", "A", "A"]]

import heapq

visited = set()
queue = [(0, rooms, corridor)]
while queue:
    cost, rooms, corridor = heapq.heappop(queue)
    fp = (tuple(map(tuple, rooms)), tuple(corridor))
    if fp in visited:
        continue
    
    visited.add(fp)
    if cost%100 == 0:
        print(cost)
    if complete(rooms):
        print("done", cost)
        break

    beforeIn = len(queue)
    for cost_, rooms_, corridor_ in inMoves(rooms, corridor):
        heapq.heappush(queue, (cost + cost_, rooms_, corridor_))

    if len(queue) == beforeIn:
        for cost_, rooms_, corridor_ in outMoves(rooms, corridor):
            heapq.heappush(queue, (cost + cost_, rooms_, corridor_))

