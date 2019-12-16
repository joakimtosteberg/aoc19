import sys
sys.path.append('../intcode')

import intcode

with open("day13.input") as file:
    program = [int(val) for val in file.read().split(',')]

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


arcade = intcode.IntCode()
arcade.load_program(program)
out_queue = arcade.get_output_queue()
board = {}
while not arcade.is_stopped():
    arcade.run_program()

    while not out_queue.empty():
        x = out_queue.get()
        y = out_queue.get()
        id = out_queue.get()
        if x == -1 and y == 0:
            pass
        else:
            board[(x,y)] = id

    num_blocks = 0
    for pos in board:
        if board[pos] == BLOCK:
            num_blocks += 1
    print(num_blocks)
