inputString = "1117 0 8 21078 2389032 142881 93 385"
stones = list(map(int,inputString.split(" ")))

def transform(stone):
    if stone == 0:
        return [1]
    s = str(stone)
    if len(s)%2 == 0:
        return [int(s[:len(s)//2]),int(s[len(s)//2:])]
    return [stone*2024]


cache = {}
def cache_key(stone, blinks):
    return tuple([stone,blinks])


def transform_n_times(stone, blinks):
    key = cache_key(stone, blinks)
    if key not in cache:
        products = transform(stone)
        if blinks == 1:
            return len(products)
        cache[key] =  sum(transform_n_times(s, blinks-1) for s in products)
    return cache[key]


def transform_all(stones, blinks):
    return sum(transform_n_times(s, blinks) for s in stones)


print("Part 1:", transform_all(stones, 25))
print("Part 2:", transform_all(stones, 75))

