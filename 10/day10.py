import math

astroid_locations = {}
X=0
Y=0
map_width = 0
with open("day10.input") as file:
    for line in file:
        for pos in line:
            if pos == '#':
                astroid_locations[(X,Y)] = 1
            X += 1
        map_width = X
        X = 0
        Y += 1

map_height = Y

def get_blocked_positions(position, astroid, width, height):
    delta_x = astroid[0] - position[0]
    delta_y = astroid[1] - position[1]
    gcd = math.gcd(delta_x, delta_y)
    delta_x /= gcd
    delta_y /= gcd
    next_blocked = astroid
    blocked_positions = []
    while True:
        next_blocked = (next_blocked[0] + delta_x, next_blocked[1] + delta_y)
        if next_blocked[0] < 0 or next_blocked[0] >= width or next_blocked[1] < 0 or next_blocked[1] >= height:
            break
        blocked_positions.append(next_blocked)
    return blocked_positions
    

def print_map(astroid_locations, width, height):
    print(width)
    print(height)
    for y in range(0,height):
        for x in range(0,width):
            if (x,y) in astroid_locations:
                print(astroid_locations[(x,y)], end = '')
            else:
                print('.', end = '')
        print('')
            

def get_visible_astroids(position, astroid_locations, width, height):
    astroid_locations[position] = 0
    for astroid in astroid_locations:
        if astroid_locations[astroid] != 1:
            continue
        blocked_positions = get_blocked_positions(position, astroid, width, height)
        for blocked_position in blocked_positions:
            if blocked_position in astroid_locations:
                astroid_locations[blocked_position] = 0

    return astroid_locations


    num_visible = 0
    for astroid in astroid_locations:
        num_visible += astroid_locations[astroid]
    # astroid_locations[position] = 'M'
    # print_map(astroid_locations, width, height)
    # astroid_locations[position] = 0
    return num_visible

def get_next_laser_target(laser_target, astroid_locations):
    #(0,-1)
    #(X, Y)
    for location in astroid_locations:
        angle = (0*X - Y)
        -location[1] / (1 + ( ((location[0] ** 2) + (location[1] ** 2)) ** 0.5))
        pass
    
def shoot_laser(astroid_locations, station_location):
    normalized_locations = {(key[0]-station_location[0],key[1]-station_location[1]):val for key, val in astroid_locations.items() if val == 1}
    location_angles = {}
    for location in normalized_locations:
        if location[0] >= 0:
            location_angles[location] = math.acos(-location[1] / (1 * ( ((location[0] ** 2) + (location[1] ** 2)) ** 0.5)))
        else:
            location_angles[location] = 2 * math.pi - math.acos(-location[1] / (1 * ( ((location[0] ** 2) + (location[1] ** 2)) ** 0.5)))

    hit_order = sorted(location_angles, key=location_angles.get)
    print("Value=%u" % ((hit_order[199][0] + station_location[0]) * 100 + (hit_order[199][1] + station_location[1])))


best_pos = None
best_num = 0
best_visible_locations = None
for position in astroid_locations:
    visible_astroids = get_visible_astroids(position, dict(astroid_locations), map_width, map_height)
    num_visible = 0
    for astroid in visible_astroids:
        num_visible += visible_astroids[astroid]
    if num_visible > best_num:
        best_num = num_visible
        best_pos = position
        best_visible_locations = visible_astroids

shoot_laser(best_visible_locations, best_pos)
print("Best position is %s seeing %u astroids" % (best_pos, best_num))
#(3,4) -> (2,2) -> (1,0)


#(2,2) blocks (2 + X, 2 + 2X)

#(A,B) -> (C,D) then (C,D) blocks all (C+X(C-A), D
