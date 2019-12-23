import sys
sys.path.append('../intcode')

import intcode

with open("day23.input") as file:
    program = [int(val) for val in file.read().split(',')]

computers = [intcode.IntCode() for i in range(50)]

for i in range(len(computers)):
    computers[i].load_program(program)
    # Set network address
    computers[i].get_input_queue().put(i)

while True:
    for computer in computers:
        computer.run_program()
        src = computer.get_output_queue()
        computer.get_input_queue().put(-1)
        while not src.empty():
            addr = src.get()
            x = src.get()
            y = src.get()
            if addr == 255:
                print(y)
                sys.exit(0)
            dest = computers[addr].get_input_queue()
            dest.put(x)
            dest.put(y)
