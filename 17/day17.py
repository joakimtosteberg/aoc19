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

pos = (0,0)
while not out_queue.empty():
    obj = chr(out_queue.get())
    if obj == '\n':
        pos = (0, pos[1]+1)
    else:
        ship_map[pos] = obj
        pos = (pos[0]+1, pos[1])

checksum = 0
for pos in ship_map:
    if ((ship_map.get((pos[0], pos[1]), '.') == '#') and
        (ship_map.get((pos[0] + 1, pos[1]), '.') == '#') and
        (ship_map.get((pos[0] - 1, pos[1]), '.') == '#') and
        (ship_map.get((pos[0], pos[1] + 1), '.') == '#') and
        (ship_map.get((pos[0], pos[1] - 1), '.') == '#')):
        checksum += pos[0]*pos[1]

print("Alignemnt calibration=%u" % (checksum))
    
        
