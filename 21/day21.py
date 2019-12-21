import sys
import itertools
sys.path.append('../intcode')

import intcode

with open("day21.input") as file:
    program = [int(val) for val in file.read().split(',')]

system = intcode.IntCode()
system.load_program(program)

in_queue = system.get_input_queue()
out_queue = system.get_output_queue()

spring_program = ["NOT A J",
                  "NOT B T",
                  "OR T J",
                  "NOT C T",
                  "OR T J",
                  "AND D J",
                  "WALK"]

for instruction in spring_program:
    for character in instruction:
        in_queue.put(ord(character[0]))
    in_queue.put(ord('\n'))
system.run_program()

while not out_queue.empty():
    output = out_queue.get()
    try:
        print(chr(output), end='')
    except:
        print(output)
