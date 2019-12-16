def get_direction(move):
    if move[0] == 'U':
        return (1,0)
    elif move[0] == 'D':
        return (-1,0)
    elif move[0] == 'L':
        return (0,-1)
    elif move[0] == 'R':
        return (0,1)
    else:
        print("Invalid direction: %s" % move[0])
        exit(-1)

def get_steps(move):
    return int(move[1:])

paths = []
with open("day3.input") as file:
    for line in file:
        path = line.split(',')
        paths.append(path)

grids = []

for path in paths:
    pos = (0,0)
    delay = 0
    grid = {}
    grid[pos] = 1
    for move in path:
        direction = get_direction(move)
        steps = get_steps(move)
        for i in range(0, steps):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            delay += 1
            if not pos in grid:
                grid[pos] = delay
    grids.append(grid)

min_dist = 999999999999999999999999
min_delay = 999999999999999999999999

for pos in grids[0]:
    if pos in grids[1] and pos != (0,0):
        distance = abs(pos[0]) + abs(pos[1])
        if distance < min_dist:
            min_dist = distance
        delay = grids[0][pos] + grids[1][pos]
        if delay < min_delay:
            min_delay = delay

print(min_dist)
print(min_delay)
