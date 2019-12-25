import sys
import curses
sys.path.append('../intcode')

import intcode

def main(stdscr):
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
            response += chr(out_queue.get())
        stdscr.addstr(0, 0, response)
        stdscr.refresh()
        c = stdscr.getkey()
        command = None
        if c == curses.KEY_LEFT:
            command = "west"
        elif c == curses.KEY_RIGHT:
            command = "east"
        elif c == curses.KEY_UP:
            command = "north"
        elif c == curses.KEY_DOWN:
            command = "south"
        else:
            continue
        for char in command:
            in_queue.put(ord(char))

curses.wrapper(main)
