import sys
import curses
sys.path.append('../intcode')

import intcode

def read_until_newline(stdscr):
    data = ""
    while True:
        c = stdscr.getkey()
        if c == '\n':
            break
        data += c
    return data

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
        stdscr.clear()
        stdscr.addstr(0, 0, response)
        stdscr.refresh()
        c = stdscr.getch()
        command = None
        if c == curses.KEY_LEFT:
            command = "west"
        elif c == curses.KEY_RIGHT:
            command = "east"
        elif c == curses.KEY_UP:
            command = "north"
        elif c == curses.KEY_DOWN:
            command = "south"
        elif c == ord('t'):
            command = "take " + read_until_newline(stdscr)
        elif c == ord('d'):
            command = "drop " + read_until_newline(stdscr)
        elif c == ord('i'):
            command = "inv"
        elif c == ord('c'):
            command = read_until_newline(stdscr)
        else:
            continue

        for char in command:
            in_queue.put(ord(char))
        in_queue.put(10)

curses.wrapper(main)
