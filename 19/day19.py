import sys
import itertools
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
for y in range(50):
    for x in range(50):
        system.load_program(program)
        in_queue.put(x)
        in_queue.put(y)
        system.run_program()
        space_map[(x,y)] = out_queue.get()
        if space_map[(x,y)] == 1:
            affected_points += 1

print(affected_points)

def scan_location(space_map, system, program, x,y):
    system.load_program(program)
    system.get_input_queue().put(x)
    system.get_input_queue().put(y)
    system.run_program()
    response = system.get_output_queue().get()
    if response == 1:
        space_map[(x,y)] = 1
        return True
    return False

def find_start(space_map, system, program):
    for start_y in itertools.count(0):
        y = start_y
        x = 0
        for x in range(0,start_y):
            if scan_location(space_map, system, program, x, y):
                return (x,y)

        for y in range(x, 0, -1):
            if scan_location(space_map, system, program, x, y):
                return(x,y)

def check_for_square(space_map, system, program, pos, size):
    if pos[1] < size:
        return False

    if (scan_location(space_map, system, program, pos[0], pos[1] - (size - 1)) and
        scan_location(space_map, system, program, pos[0] + (size - 1), pos[1] - (size - 1))):
        return True

    return False

def find_next_pos(space_map, system, program, pos):
    x = pos[0]
    y = pos[1] + 1
    while not scan_location(space_map, system, program, x, y):
        x = x + 1
    return (x,y)

pos = find_start(space_map, system, program)

while not check_for_square(space_map, system, program, pos, 100):
    pos = find_next_pos(space_map, system, program, pos)
    #print(pos)

print(pos[0] * 10000 + (pos[1] - 99))
