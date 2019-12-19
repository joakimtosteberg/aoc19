import sys
import copy
sys.path.append('../intcode')

import intcode

with open("day19.input") as file:
    program = [int(val) for val in file.read().split(',')]

system = intcode.IntCode()
system.load_program(program)

in_queue = system.get_input_queue()
out_queue = system.get_output_queue()

space_map = {}
affected_points = 0
for x in range(50):
    for y in range(50):
        system.load_program(program)
        in_queue.put(x)
        in_queue.put(y)
        system.run_program()
        space_map[(x,y)] = out_queue.get()
        if space_map[(x,y)] == 1:
            affected_points += 1

print(affected_points)
