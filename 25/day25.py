import sys
sys.path.append('../intcode')

import intcode

def main():
    with open("day25.input") as file:
        program = [int(val) for val in file.read().split(',')]

    droid = intcode.IntCode()
    droid.load_program(program)

    in_queue = droid.get_input_queue()
    out_queue = droid.get_output_queue()

    while True:
        droid.run_program()
        response = ""
        while not out_queue.empty():
            print(chr(out_queue.get()),end='')

        command = input()
        for char in command:
            in_queue.put(ord(char))
        in_queue.put(10)

main()
