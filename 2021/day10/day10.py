with open("input.txt", "r") as f:
   lines = [l.strip() for l in f.readlines()]

# Definitions from the exercise
opens = set(["[", "(", "{", "<"])
closes = {"]":"[", ")":"(", "}":"{", ">":"<"}
scores = {"]":57, ")":3, "}":1197, ">":25137}
autoc = {"(":1, "[":2, "{":3, "<":4}

# Find valid/invalid lines by pushing/popping to/from a stack
validLineStacks = []
syntaxScore = 0
for line in lines:
    stack = []
    valid = True
    for x in line:
        if x in opens:
            stack.append(x)
        if x in closes:
            y = closes[x]
            if stack[-1] != y:
                # This means we have an invalid closer
                syntaxScore += scores[x]
                valid = False
                break
            stack.pop()
    if valid: # save stack for part 2
        validLineStacks.append(stack)

def stackScore(stack):
    score = 0
    while stack:
        score *= 5
        x = stack.pop()
        score += autoc[x]
    return score

autocScores = []
for stack in validLineStacks:
    autocScores.append(stackScore(stack))
autocScores.sort()

print(syntaxScore)
print(autocScores[len(autocScores)//2])
