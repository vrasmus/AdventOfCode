#xmin, xmax, ymin, ymax = 20, 30, -10, -5
xmin, xmax, ymin, ymax = 79, 137, -176, -117

def inRange(x, y):
    if x < xmin or x > xmax:
        return False
    if y < ymin or y > ymax:
        return False
    return True

# Simple brute-force solution today
count = 0
maxyhit = -1e99
for i in range(0, 1000):
    for j in range(-1000, 1000):
        x, y = 0, 0
        dx, dy = i, j
        maxy = 0
        for _ in range(1000):
            x += dx
            y += dy
            maxy = max(y, maxy)
            if dx != 0:
                dx -= 1 if dx > 0 else 1
            dy -= 1
            if inRange(x, y):
                count += 1
                maxyhit = max(maxyhit, maxy)
                break
            if y < ymin or x > xmax:
                # break early if this can't be a solution
                break

print(maxyhit)
print(count)
