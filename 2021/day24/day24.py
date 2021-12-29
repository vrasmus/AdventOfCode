# The program has 14 similar blocks with only few changing values.
# Only three instructions are actually changing:
#   - an 'add x int' line
#   - a 'div z [1/26]' line
#   - an 'add y int' line
# These values are read from my input. 
addX = [13, 11, 12, 10, 14, -1, 14, -16, -8, 12, -16, -13, -6, -6]
divZ = [1, 1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 26, 26, 26]
addY = [6, 11, 5, 6, 8, 14, 9, 4, 7, 13, 11, 11, 6, 1]

# To ensure z can become zero in the last stage, it must not exceed the divisons with it,
# since this is where it is made smaller. Terminate early if this happens.
impossible = [26**7, 26**7, 26**7, 26**7, 26**7, 26**7, 26**6, 26**6, 26**5, 26**4, 26**4, 26**3, 26**2, 26]

# One of the 14 blocks are mathematically equivalent to making the following transformation to the z value.
# The other values doesn't matter, as they are always set to zero before being used in a stage.
def stage(stage, w, z):
    if z % 26 + addX[stage] == w:
        return z // divZ[stage]
    return 26 * (z // divZ[stage]) + w + addY[stage]

# Now we perform dfs to find valid values, searching all possible.
# This prints every valid input:
#  - the first one is the largest number (part 1)
#  - the last one is the smallest number (part 2)
def dfs(z, stack):
    if len(stack) == 14:
        if z == 0:
            print("".join(map(str, stack)))
        return

    if z > impossible[len(stack)]:
        return
        
    for i in range(9, 0, -1):
        newZ = stage(len(stack), i, z) 
        stack.append(i)
        dfs(newZ, stack)
        stack.pop()

dfs(0, [])
