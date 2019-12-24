import copy

layout = {}
width = 0
height = 0
with open("day24.input") as file:
    y = 0
    for line in file:
        x = 0
        for tile in line.rstrip():
            layout[(x,y)] = {'bug': 1 if tile == '#' else 0, 'adjacent': 0}
            x += 1
            width = max(x,width)
        y += 1
        height = max(y,height)

def get_tile(layout, x, y):
    return layout.get((x,y), {'bug': 0,'adjacent': 0})

def get_num_bugs(layout, x, y):
    return get_tile(layout, x, y)['bug']

def get_adjacent_bugs(layout, x, y):
    adjacent_bugs = 0
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        adj_x = x + step[0]
        adj_y = y + step[1]
        adjacent_bugs += get_num_bugs(layout, adj_x, adj_y)
    return adjacent_bugs

for y in range(height):
    for x in range(width):
        layout[(x,y)]['adjacent'] = get_adjacent_bugs(layout, x, y)

def update_tile(next_layout, x, y, bug):
    next_layout[(x,y)]['bug'] = bug
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        adj_x = x + step[0]
        adj_y = y + step[1]
        if ((adj_x,adj_y) not in next_layout):
            continue
        next_layout[(adj_x,adj_y)]['adjacent'] += 1 if bug else -1

def update(layout, widht, height):
    next_layout = copy.deepcopy(layout)
    for y in range(height):
        for x in range(width):
            if layout[(x,y)]['bug']:
                if layout[(x,y)]['adjacent'] != 1:
                    update_tile(next_layout, x, y, 0)
            else:
                if layout[(x,y)]['adjacent'] in [1,2]:
                    update_tile(next_layout, x, y, 1)
    return next_layout

def print_layout(layout, widht, height):
    for y in range(height):
        for x in range(width):
            if layout[(x,y)]['bug']:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('')
    print('')

def calculate_biodiversity(layout, widht, height):
    biodiversity = 0
    for y in range(height):
        for x in range(width):
            if layout[(x,y)]['bug']:
                biodiversity += pow(2,width*y + x)
    return biodiversity

layouts = [layout]
while True:
    layout = update(layout, width, height)
    if layout in layouts:
        print(calculate_biodiversity(layout, width, height))
        break
    layouts.append(layout)

