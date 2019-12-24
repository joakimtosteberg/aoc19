import copy

width = 5
height = 5

def create_empty_layer(width, height):
    layer = {}
    for y in range(height):
        for x in range(width):
            if x==2 and y==2:
                continue
            layer[(x,y)] = {'bug': 0, 'adjacent': 0}
    return layer

def get_adjacent_coords(layer_id, x, y, step, width, height):
    coords = []
    adj_x = x + step[0]
    adj_y = y + step[1]
    if adj_x == -1:
        coords.append([layer_id - 1, 1, 2])
    elif adj_x == width:
        coords.append([layer_id - 1, 3, 2])
    elif adj_y == -1:
        coords.append([layer_id - 1, 2, 1])
    elif adj_y == height:
        coords.append([layer_id - 1, 2, 3])
    elif adj_x==2 and adj_y==2:
        if step[0]:
            for i in range(height):
                coords.append([layer_id + 1, 0 if step[0] == 1 else width - 1, i])
        else:
            for i in range(width):
                coords.append([layer_id + 1, i, 0 if step[1] == 1 else height -1])
    else:
        coords.append([layer_id, adj_x, adj_y])
    return coords

def update_tile(layers, layer_id, x, y, bug_change, width, height):
    layers[layer_id][(x,y)]['bug'] += bug_change
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        for coord in get_adjacent_coords(layer_id, x, y, step, width, height):
            if coord[0] not in layers:
                layers[coord[0]] = create_empty_layer(width, height)
            #if coord[0] == 1:
            #print("change=%d, layer=%u, pos=(%u,%u), adj_to=(%u,%u,%u)" % (bug_change, coord[0], coord[1], coord[2], layer_id, x, y))
            layers[coord[0]][(coord[1],coord[2])]['adjacent'] += bug_change

def update(layers, widht, height):
    next_layers = copy.deepcopy(layers)
    for layer_id in layers:
        for y in range(height):
            for x in range(width):
                if (x,y) not in layers[layer_id]:
                    continue
                if layers[layer_id][(x,y)]['bug']:
                    if layers[layer_id][(x,y)]['adjacent'] != 1:
                        update_tile(next_layers, layer_id, x, y, -1, width, height)
                else:
                    if layers[layer_id][(x,y)]['adjacent'] in [1,2]:
                        update_tile(next_layers, layer_id, x, y, 1, width, height)
    return next_layers

def print_layer(layer, widht, height, adjacent):
    for y in range(height):
        for x in range(width):
            if (x,y) not in layer:
                print(' ', end ='')
            elif adjacent:
                print(layer[(x,y)]['adjacent'], end='')
            elif layer[(x,y)]['bug']:
                print('#', end='')
            else:
                print('.', end='')
        print('')

def print_layers(layers, widht, height, adjacent = False):
    for layer_id in sorted(layers):
        print("LAYER: %d" % (layer_id))
        print_layer(layers[layer_id], width, height, adjacent)

def count_bugs_in_layer(layer):
    bugs = 0
    for y in range(height):
        for x in range(width):
            bugs += layer.get((x,y), {'bug':0})['bug']
    return bugs

def count_bugs(layers):
    bugs = 0
    for layer_id in layers:
        bugs += count_bugs_in_layer(layers[layer_id])
    return bugs

layers = {}
layers[0] = create_empty_layer(width,height)

with open("day24.input") as file:
    y = 0
    for line in file:
        x = 0
        for tile in line.rstrip():
            if tile == '#':
                update_tile(layers, 0, x, y, 1, 5, 5)
            x += 1
        y += 1

for i in range(200):
    layers = update(layers, width, height)

print(count_bugs(layers))
