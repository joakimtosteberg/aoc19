import sys
import copy
sys.path.append('../intcode')

import intcode

with open("day17.input") as file:
    program = [int(val) for val in file.read().split(',')]

system = intcode.IntCode()
system.load_program(program)

in_queue = system.get_input_queue()
out_queue = system.get_output_queue()

ship_map = {}

system.run_program()

def read_map(out_queue, ship_map, do_print):
    pos = (0,0)
    was_newline = False
    map_done = False
    while not out_queue.empty():
        obj = chr(out_queue.get())
        if do_print:
            print(obj, end='')
        if obj == '\n':
            if was_newline:
                map_done = True
            else:
                was_newline = True
                pos = (0, pos[1]+1)
        elif not map_done:
            was_newline = False
            ship_map[pos] = obj
            pos = (pos[0]+1, pos[1])

read_map(out_queue, ship_map, False)
checksum = 0
for pos in ship_map:
    if ((ship_map.get((pos[0], pos[1]), '.') == '#') and
        (ship_map.get((pos[0] + 1, pos[1]), '.') == '#') and
        (ship_map.get((pos[0] - 1, pos[1]), '.') == '#') and
        (ship_map.get((pos[0], pos[1] + 1), '.') == '#') and
        (ship_map.get((pos[0], pos[1] - 1), '.') == '#')):
        checksum += pos[0]*pos[1]

print("Alignemnt calibration=%u" % (checksum))
    
        
program[0] = 2
system.load_program(program)
system.run_program()
read_map(out_queue, ship_map, True)
