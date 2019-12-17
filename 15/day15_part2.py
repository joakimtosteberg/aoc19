import sys
import copy
sys.path.append('../intcode')

import intcode

with open("day15.input") as file:
    program = [int(val) for val in file.read().split(',')]

droid = intcode.IntCode()
droid.load_program(program)

in_queue = droid.get_input_queue()
out_queue = droid.get_output_queue()

ship_map = {}
pos = (0,0)
goal = None

ship_map[pos] = 0

directions = [[1, 2, (-1, 0)], [2, 1, (1,0)], [3, 4, (0,1)], [4, 3, (0,-1)]]

def goto_oxygen(ship_map, pos, droid, depth):
    for direction in directions:
        droid.get_input_queue().put(direction[0])
        droid.run_program()
        status = droid.get_output_queue().get()
        if status == 0:
            continue
        new_pos = (pos[0]+direction[2][0],pos[1]+direction[2][1])
        if new_pos not in ship_map or depth < ship_map[new_pos]:
            ship_map[new_pos] = depth
            if status == 1:
                oxy_pos = goto_oxygen(ship_map, new_pos, droid, depth + 1)
                if oxy_pos is not None:
                    return oxy_pos
            elif status == 2:
                return new_pos

        # Backtrack
        droid.get_input_queue().put(direction[1])
        droid.run_program()
        droid.get_output_queue().get()
    return None

def explore(ship_map, pos, droid, depth):
    for direction in directions:
        droid.get_input_queue().put(direction[0])
        droid.run_program()
        status = droid.get_output_queue().get()
        if status == 0:
            continue
        new_pos = (pos[0]+direction[2][0],pos[1]+direction[2][1])
        if new_pos not in ship_map or depth < ship_map[new_pos]:
            ship_map[new_pos] = depth
            if status == 1:
                explore(ship_map, new_pos, droid, depth + 1)

        # Backtrack
        droid.get_input_queue().put(direction[1])
        droid.run_program()
        droid.get_output_queue().get()

oxy_pos = goto_oxygen(ship_map, pos, droid, 1)

ship_map = {}
ship_map[oxy_pos] = 0
explore(ship_map, pos, droid, 1)

max_distance = 0
for pos in ship_map:
    max_distance = max(max_distance, ship_map[pos])

print(max_distance)

