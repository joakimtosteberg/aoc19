import itertools
cave = {}
pos = None
num_keys = 0
with open("day18.input.example") as file:
    y = 0
    for line in file:
        for x in range(0, len(line)):
            cave[(x,y)] = line[x]
            if line[x] == '@':
                cave[(x,y)] = '.'
                pos = (x,y)
            elif line[x].islower():
                num_keys += 1
        y += 1

def is_key(tile):
    return tile.islower()

def is_door(tile):
    return tile.isupper()

def is_empty(tile):
    return tile == '.'

def length_to_keys(cave, keys, start_pos):
    track = {start_pos: 0}
    found_keys = {}
    positions = [start_pos]
    for steps in itertools.count(1):
        next_positions = []
        for pos in positions:
            for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0] + direction[0],
                            pos[1] + direction[1])

                # Skip positions we have reached in fewer steps
                if next_pos in track and steps >= track[next_pos]:
                    continue

                tile = cave[next_pos]

                # Don't move through doors we can't open
                if is_door(tile) and tile.lower() not in keys:
                    continue

                # Now step onto the tile if we can
                if is_key(tile) or is_empty(tile) or is_door(tile):
                    # Shortest path to key found, save it
                    if is_key(tile) and tile not in keys:
                        found_keys[tile] = (next_pos,steps)
                    track[next_pos] = steps
                    next_positions.append(next_pos)

        if not next_positions:
            break
        positions = next_positions
    return found_keys
        

def find_all_keys(cave, found_keys, keys, steps, total_num_keys):
    if len(keys) == total_num_keys:
        return steps

    best_steps_to_end = None
    for key in found_keys:
        current_keys = keys + [key]
        new_keys = length_to_keys(cave, current_keys, found_keys[key][0])
        steps_to_end = find_all_keys(cave, new_keys, current_keys, steps + found_keys[key][1], total_num_keys)
        if steps_to_end:
            if not best_steps_to_end:
                best_steps_to_end = steps_to_end
            else:
                best_steps_to_end = min(steps_to_end, best_steps_to_end)

    return best_steps_to_end

    
found_keys = length_to_keys(cave, [], pos)
print(find_all_keys(cave, found_keys, [], 0, num_keys))
