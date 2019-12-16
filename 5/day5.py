import sys 
sys.path.append('../intcode')

import intcode

def print_output(val):
    print(val)

with open("day5.input") as file:
    program = [int(val) for val in file.read().split(',')]

    
computer = intcode.IntCode()
print("Run air condition diagnostics")
computer.attach_io(lambda : 1,
                   print_output)
computer.load_program(program)
computer.run_program()

print("Run thermal radiator diagnostics")
computer.attach_io(lambda : 5,
                   print_output)
computer.load_program(program)
computer.run_program()
