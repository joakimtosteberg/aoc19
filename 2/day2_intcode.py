import sys 
sys.path.append('../intcode')

import intcode

with open("day2.input") as file:
    program = [int(val) for val in file.read().split(',')]

program[1] = 12
program[2] = 2

computer = intcode.IntCode()
computer.load_program(program)
computer.run_program()
print(computer.memory[0])
print(computer.memory)

wanted = 19690720

for noun in range(0,100):
    for verb in range(0,100):
        program[1] = noun
        program[2] = verb
        computer.load_program(program)
        computer.run_program()
        if (computer.memory[0] == wanted):
            print(100*noun+verb)
            sys.exit(0)

print("Not found")
