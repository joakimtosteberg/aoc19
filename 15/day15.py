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


def recursive_move(ship_map, pos, droid, depth):
    global goal
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
                recursive_move(ship_map, new_pos, droid, depth + 1)
            elif status == 2:
                goal = new_pos

        # Backtrack
        droid.get_input_queue().put(direction[1])
        droid.run_program()
        droid.get_output_queue().get()

recursive_move(ship_map, pos, droid, 1)

print(ship_map[goal])
