with open("input.txt", "r") as f:
    content = f.read().split("\n\n")
    rules = [list(map(int,r.split("|"))) for r in content[0].split()]
    updates = [list(map(int,r.split(","))) for r in content[1].split()]


priorRuleMap = {}
for rule in rules:
    a, b = rule[0],rule[1]
    cannotBeBefore = priorRuleMap.get(a, set())
    cannotBeBefore.add(b)
    priorRuleMap[a] = cannotBeBefore


def find_next(curr, remains):
    mustBeConcluded = priorRuleMap.get(curr, [])
    for val in mustBeConcluded:
        if val in remains:
            return find_next(val, remains)
    return curr


def sort_invalid(update):
    result = []
    remains = set(update)
    for val in update:
        while val in remains:
            nxt = find_next(val, remains)
            result.append(nxt)
            remains.remove(nxt)
    return result


validMiddleNumbers = []
middleNumbersOfSortedInvalid = []
for update in updates:
    seen = set()
    valid = True
    for page in update:
        mustNotHaveSeen = priorRuleMap.get(page, set())
        if len(seen & mustNotHaveSeen) > 0:
            valid = False
            break
        seen.add(page)
    if valid:
        validMiddleNumbers.append(update[len(update)//2])
    else:
        update = sort_invalid(update)
        middleNumbersOfSortedInvalid.append(update[len(update)//2])


print("Part 1:", sum(validMiddleNumbers))
print("Part 2:", sum(middleNumbersOfSortedInvalid))
