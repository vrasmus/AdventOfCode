def playDeterministic(positions, scores):
    winner = 1000
    roll = 1
    rollCount = 0
    while max(scores) < winner:
        for player in [0, 1]:
            for _ in range(3):
                rollCount += 1
                positions[player] = (positions[player] + roll)%10
                roll = roll % 100 + 1
            scores[player] += 10 if positions[player] == 0 else positions[player]
            if max(scores) >= winner:
                break
    return min(scores)*rollCount

cache = {}
def play(p1, p2, s1, s2, current, remainingTurns):
    if (p1, p2, s1, s2, current, remainingTurns) not in cache:
        if s1 >= 21:
            return 1, 0
        if s2 >= 21:
            return 0, 1
    
        if remainingTurns == 0:
            if current == 0:
                s1 += 10 if p1 == 0 else p1
            else:
                s2 += 10 if p2 == 0 else p2
            current = (current + 1)%2
            return play(p1, p2, s1, s2, current, 3)

        w1, w2 = 0, 0
        for roll in [1, 2, 3]:
            if current == 0:
                w1_, w2_ = play((p1 + roll)%10, p2, s1, s2, current, remainingTurns - 1)
            else:
                w1_, w2_ = play(p1, (p2 + roll)%10, s1, s2, current, remainingTurns - 1)
            w1 += w1_
            w2 += w2_
        cache[(p1, p2, s1, s2, current, remainingTurns)] = (w1, w2)
    return cache[(p1, p2, s1, s2, current, remainingTurns)]
   

#p1, p2 = 4, 8 ## Test input (4, 8)
p1, p2 = 8, 0 ## My input (8, 10)
print(playDeterministic([p1,p2], [0,0]))
print(max(play(p1,p2,0,0, 0, 3)))
