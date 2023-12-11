with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]
    galaxies = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                galaxies.append((i,j))


def calculate_pairwise_distance(expansion=2):
    empty_rows = [True]*len(lines)
    empty_cols = [True]*len(line)
    for x, y in galaxies:
        empty_rows[x] = False
        empty_cols[y] = False
    
    total_pairwise_dist = 0
    for i, (x1,y1) in enumerate(galaxies):
        for j, (x2,y2) in enumerate(galaxies[i+1:]):
            extra_rows = sum(empty_rows[min(x1,x2):max(x1,x2)]) 
            extra_cols = sum(empty_cols[min(y1,y2):max(y1,y2)])
            extra_rows *= expansion - 1
            extra_cols *= expansion - 1

            dist = abs(x2 - x1) + extra_rows + abs(y2 - y1) + extra_cols
            total_pairwise_dist += dist
    return total_pairwise_dist

if __name__ == "__main__":
    print(f"Part 1: {calculate_pairwise_distance()}")
    print(f"Part 2: {calculate_pairwise_distance(1000000)}")
