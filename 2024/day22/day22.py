with open("input.txt","r") as f:
    initial = list(map(int, f.readlines()))

def mix(secret, val):
    return secret ^ val

def prune(secret):
    return secret % 16777216

def evolve(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

def evolve_n_times(secret, n):
    result = [secret]
    for _ in range(n):
        secret = evolve(secret)
        result.append(secret)
    return result


def sequence_generator():
    for i1 in range(9, -10,-1):
        for i2 in range(9, -10,-1):
            for i3 in range(9, -10,-1):
                for i4 in range(9, -10,-1):
                    if -9 <= i1+i2+i3+i4 <= 9:
                        yield (i4,i3,i2,i1)


def seq_to_price_map(price, change):
    m = {}
    for i in range(len(change)):
        s = tuple(change[i-4:i])
        if s in m:
            continue
        m[s] = price[i]  
    return m


def optimize_sequence(prices):
    changes = []
    for price in prices:
        change = []
        for i in range(1, len(price)):
            change.append(price[i] - price[i-1])
        changes.append(change)
   
    # preprocess to get price per sequence per monkey
    seq_to_prices = []
    for p, c in zip(prices, changes):
        seq_to_prices.append(seq_to_price_map(p, c))
    
    best = 0
    for seq in sequence_generator():
        value = 0
        for m in seq_to_prices:
            value += m.get(seq,0)
        if value > best:
            best = value 

    return best


prices = []
result1 = 0
for secret in initial:
    sequence = evolve_n_times(secret, 2000)
    result1 += sequence[-1]
    prices.append(list(map(lambda x: x%10, sequence)))

print("Part 1:", result1)
print("Part 2:", optimize_sequence(prices))
