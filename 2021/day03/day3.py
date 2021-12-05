with open("input.txt", "r") as f:
    content = f.readlines()

report = []
for line in content:
    report.append(line.strip())
    
def mostLeastCommonBits(report):
    oneCounts = [0]*len(report[0])
    for line in report:
        for i, bit in enumerate(line):
            if bit == "1":
                oneCounts[i]+=1
    gamma = [1 if c >= len(report)/2 else 0 for c in oneCounts]
    eps = [1 if c < len(report)/2 else 0 for c in oneCounts]
    return gamma, eps

def toDec(binary):
    val = 0
    for i in range(len(binary)):
        val = val<<1
        val += int(binary[i])
    return val

def filterReport(report, i, val):
    filtered = []
    for entry in report:
        if entry[i] == val:
            filtered.append(entry)
    return filtered

gamma, eps = mostLeastCommonBits(report)
print(toDec(gamma)*toDec(eps))

filteredO2 = report
for i in range(len(report[0])):
    if len(filteredO2) == 1:
        break
    gamma, eps = mostLeastCommonBits(filteredO2)
    filteredO2 = filterReport(filteredO2, i, str(gamma[i]))

filteredCO2 = report
for i in range(len(report[0])):
    if len(filteredCO2) == 1:
        break
    gammaC, epsC = mostLeastCommonBits(filteredCO2)
    filteredCO2 = filterReport(filteredCO2, i, str(epsC[i]))

print(toDec(filteredO2[0])*toDec(filteredCO2[0]))
