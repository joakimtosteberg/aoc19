import sys 
sys.path.append('../intcode')

import intcode


with open("day9.input") as file:
    program = [int(val) for val in file.read().split(',')]

    
computer = intcode.IntCode()
print("Run BOOST diag")
computer.get_input_queue().put(1)
computer.load_program(program)
computer.run_program()

while not computer.get_output_queue().empty():
    print(computer.get_output_queue().get())

print("Run BOOST")
computer.get_input_queue().put(2)
computer.load_program(program)
computer.run_program()

while not computer.get_output_queue().empty():
    print(computer.get_output_queue().get())
