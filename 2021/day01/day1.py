with open("day1.data", "r") as f:
    content = f.readlines()

sonar = []
for line in content:
    sonar.append(int(line))

deeperCount = 0
for i in range(len(sonar)-1):
    if sonar[i+1] > sonar[i]:
        deeperCount += 1

slidingDeeperCount = 0
for i in range(len(sonar)-3):
    if sum(sonar[i:i+3]) < sum(sonar[i+1:i+4]):
        slidingDeeperCount += 1

print(deeperCount, slidingDeeperCount)
