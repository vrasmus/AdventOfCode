with open("input.txt", "r") as f:
    lines = [l.strip().split(",") for l in f.readlines()]
    points = set([tuple(map(int, l)) for l in lines])


def neighbors(point):
    x, y, z = point
    for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
        yield x+dx, y+dy, z+dz 


def surface_area(points, outer_area = False):
    global_min = min(min(p) for p in points)
    global_max = max(max(p) for p in points)

    area = 0
    for point in points:
        for n in neighbors(point):
            if n not in points:
                # Only count the area for part 2 if it's in exterior point
                if not outer_area or is_exterior_point(n, points, global_min, global_max):
                    area += 1
    return area


# Use simple BFS to discover if point is an exterior point (see if we can reach outside)
def is_exterior_point(point, points, global_min, global_max, visited=set()):
    queue = [point]
    visited = set(queue)
    while queue:
        p = queue.pop()

        # If search reaches the outer bounds, we must have started on the exterior
        if any(global_max < c or global_min > c for c in p):
            return True

        for n in neighbors(p):
            if n in points:
                continue

            if n not in visited:
                queue.append(n)
                visited.add(n)

    # If search terminates, we couldn't get outside, so we must be on interior
    return False


if __name__ == "__main__":
    print("Part 1:", surface_area(points, outer_area=False))
    print("Part 2:", surface_area(points, outer_area=True))

