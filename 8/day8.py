width = 25
height = 6

data = []
with open("day8.input") as file:
    data = [int(pixel) for pixel in file.read()]

layers = []
layer_info = {}
pixel_pos = 0
while pixel_pos < len(data):
    layer = []
    for row in range(0, height):
        layer.append(data[pixel_pos:pixel_pos+width])
        pixel_pos += width
    layer_info[len(layers)] = {0: sum(x.count(0) for x in layer),
                               1: sum(x.count(1) for x in layer),
                               2: sum(x.count(2) for x in layer)}
    layers.append(layer)

best_layer = None
for layer in layer_info:
    if not best_layer:
        best_layer = layer
    elif layer_info[layer][0] < layer_info[best_layer][0]:
        best_layer = layer

print(best_layer)
print(layer_info[best_layer][1]*layer_info[best_layer][2])

visible = []
for layer in reversed(layers):
    if not visible:
        visible = layer
    else:
        for row in range(0, height):
            for column in range(0, width):
                if layer[row][column] != 2:
                    visible[row][column] = layer[row][column]

for row in visible:
    for pixel in row:
        print('*' if pixel else ' ', end = '')
    print()
        

        

