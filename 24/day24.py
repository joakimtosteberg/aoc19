import copy

width = 5
height = 5

def update_tile(next_layout, x, y, bug_change):
    next_layout[(x,y)]['bug'] += bug_change
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        adj_x = x + step[0]
        adj_y = y + step[1]
        if ((adj_x,adj_y) not in next_layout):
            continue
        next_layout[(adj_x,adj_y)]['adjacent'] += bug_change

def create_empty_layer(width, height):
    layer = {}
    for y in range(height):
        for x in range(width):
            layer[(x,y)] = {'bug': 0, 'adjacent': 0}
    return layer

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

def update(layout, widht, height):
    next_layout = copy.deepcopy(layout)
    for y in range(height):
        for x in range(width):
            if layout[(x,y)]['bug']:
                if layout[(x,y)]['adjacent'] != 1:
                    update_tile(next_layout, x, y, -1)
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

layout = create_empty_layer(width,height)

with open("day24.input") as file:
    y = 0
    for line in file:
        x = 0
        for tile in line.rstrip():
            if tile == '#':
                update_tile(layout, x, y, 1)
            x += 1
        y += 1

layouts = [layout]
while True:
    layout = update(layout, width, height)
    if layout in layouts:
        print(calculate_biodiversity(layout, width, height))
        break
    layouts.append(layout)

