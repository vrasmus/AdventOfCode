import re

with open("input.txt", "r") as f:
    lines = f.readlines()


class Blueprint:
    def __init__(self, line):
        line = line.strip()
        nums = list(map(int, re.findall('\d+', line)))
        self.num = nums[0]
        self.costs = [
                (nums[1], 0, 0, 0),
                (nums[2], 0, 0, 0),
                (nums[3], nums[4], 0, 0),
                (nums[5], 0, nums[6], 0)
                ]
        self.most_geodes = 0
        self.most_geodes_at_32 = 0


def calculate_missing(current, required):
    return 0 if current >= required else required-current


def time_to_build(missing_resources, robots):
    time = -1
    for i in range(len(robots)):
        if robots[i] == 0:
            if missing_resources[i] > 0: 
                return float("inf")
            continue
        to_mine = missing_resources[i]//robots[i] 
        to_mine = to_mine if missing_resources[i]%robots[i] == 0 else to_mine + 1
        time = max(time, to_mine)
    return time


def most_geodes_at(last_step, step, resources, robots):
    return resources[-1]+(last_step-step)*robots[-1]


def dfs(bp, step=0, resources=(0,0,0,0), robots=(1,0,0,0)):
    last_step = 24
    if bp.num <= 3:
        last_step = 32
    
    if step > last_step:
        return

    bp.most_geodes_at_32 = max(bp.most_geodes_at_32, most_geodes_at(32, step, resources, robots))
    bp.most_geodes = max(bp.most_geodes, most_geodes_at(24, step, resources, robots))
    
    theoretical_max = most_geodes_at(last_step, step, resources, robots)
    for i in range(last_step-step):
        # One geode bot built every step from here is the best case...
        theoretical_max += i

    if bp.num <= 3 and bp.most_geodes_at_32 > theoretical_max:
        return
    if bp.most_geodes > theoretical_max:
        return
    
    for i in range(len(robots)):
        if i != 3 and robots[i] >= max([c[i] for c in bp.costs]):
            # Don't build more of any robot than can be consumed per round
            continue
        missing_resources = [calculate_missing(resources[j], bp.costs[i][j]) for j in range(len(resources))]
        ttb = time_to_build(missing_resources, robots)
        if ttb < float("inf"):
            new_resources = [resources[j] + (ttb+1)*robots[j] - bp.costs[i][j] for j in range(len(robots))]
            new_robots = [robots[j] for j in range(len(robots))]
            new_robots[i] += 1
            dfs(bp, step+ttb+1, tuple(new_resources), tuple(new_robots))
        

if __name__ == "__main__":
    blueprints = []
    for line in lines:
        blueprints.append(Blueprint(line))

    part1 = 0
    part2 = 1
    for bp in blueprints:
        dfs(bp)
        part1 += bp.num*bp.most_geodes
        part2 *= 1 if bp.num > 3 else bp.most_geodes_at_32
    
    print("Part 1:", part1)
    print("Part 2:", part2)
    # Somewhat painful, but it finally works...
