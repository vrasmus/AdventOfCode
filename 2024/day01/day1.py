with open("input.txt", "r") as f:
    lines = [l.strip().split() for l in f.readlines()]
    
l1 = [int(l[0]) for l in lines]
l2 = [int(l[1]) for l in lines]
l1.sort()
l2.sort()


res = 0
for n1, n2 in zip(l1, l2):
    res += abs(n1 - n2)
print("Part 1:", res)


l2_counts = {}
for num in l2:
    l2_counts[num] = l2_counts.get(num, 0) + 1

res2 = 0
for num in l1:
    res2 += num * l2_counts.get(num, 0) 
print("Part 2:", res2)

