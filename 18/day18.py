import itertools
cave = {}
start_positions = []
num_keys = 0
key_length_cache = {}
best_steps_to_end = None

def read_map(map_file):
    global cave
    global start_positions
    global num_keys
    global key_length_cache
    global best_steps_to_end

    cave = {}
    start_positions = []
    num_keys = 0
    key_length_cache = {}
    best_steps_to_end = None

    with open(map_file) as file:
        y = 0
        for line in file:
            for x in range(0, len(line)):
                cave[(x,y)] = line[x]
                if line[x] == '@':
                    cave[(x,y)] = '.'
                    start_positions.append((x,y))
                elif line[x].islower():
                    num_keys += 1
            y += 1

def is_key(tile):
    return tile.islower()

def is_door(tile):
    return tile.isupper()

def is_empty(tile):
    return tile == '.'

def length_to_keys(cave, start_pos):
    global key_length_cache
    if start_pos in key_length_cache:
        return key_length_cache[start_pos]

    track = {start_pos: (0, [])}
    found_keys = {}
    positions = [start_pos]
    for steps in itertools.count(1):
        next_positions = []
        for pos in positions:
            for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0] + direction[0],
                            pos[1] + direction[1])


                # We are doing BFS, so any square we have visisted
                # will already have the shorted possible path to it
                if next_pos in track:
                    continue

                tile = cave[next_pos]

                # Now step onto the tile if we can
                if is_key(tile) or is_empty(tile) or is_door(tile):
                    required_keys = track[pos][1][:]

                    # Add key requirement if it is a door
                    if is_door(tile):
                        required_keys += [tile.lower()]

                    track[next_pos] = (steps, required_keys)

                    # Shortest path to key found, save it
                    if is_key(tile):
                        found_keys[tile] = {'pos': next_pos, 'steps': steps, 'required_keys': required_keys}

                    next_positions.append(next_pos)

        if not next_positions:
            break
        positions = next_positions

    key_length_cache[start_pos] = found_keys
    return found_keys


def find_all_keys(cave, found_keys, keys, steps, total_num_keys, state_map):
    global best_steps_to_end
    if best_steps_to_end and steps >= best_steps_to_end:
        return None

    if len(keys) == total_num_keys:
        return steps

    for i in range(len(found_keys)):
        for key in found_keys[i]:
            # Don't try to get a key we already have
            if key in keys:
                continue
            # Don't try to get a key we can't reach
            if not set(found_keys[i][key]['required_keys']).issubset(keys):
                continue
            current_keys = ''.join(sorted(keys)) + key
            current_steps = steps + found_keys[i][key]['steps']
            if current_keys in state_map and current_steps >= state_map[current_keys]:
                continue
            state_map[current_keys] = current_steps
            new_keys = found_keys[:]
            new_keys[i] = length_to_keys(cave, found_keys[i][key]['pos'])
            steps_to_end = find_all_keys(cave, new_keys, current_keys, current_steps, total_num_keys, state_map)
            if steps_to_end:
                if not best_steps_to_end:
                    best_steps_to_end = steps_to_end
                else:
                    best_steps_to_end = min(steps_to_end, best_steps_to_end)

    return best_steps_to_end


def solve_map(cave, start_positions, num_keys):
    found_keys = []
    for start_position in start_positions:
        found_keys.append(length_to_keys(cave, start_position))

    return find_all_keys(cave, found_keys, "", 0, num_keys, {})


read_map("day18.input")
print("Steps for part 1=%u" % (solve_map(cave, start_positions, num_keys)))

read_map("day18.part2.input")
print("Steps for part 2=%u" % (solve_map(cave, start_positions, num_keys)))

