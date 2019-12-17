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
arcade.memory[0] = 2
out_queue = arcade.get_output_queue()
in_queue = arcade.get_input_queue()
board = {}
max_x = 0
max_y = 0
ball_pos = None
paddle_pos = None

def get_paddle_direction(paddle_pos, ball_pos):
    if paddle_pos[0] < ball_pos[0]:
        return 1
    elif paddle_pos[0] > ball_pos[0]:
        return -1
    return 0

def print_board(board, width, height):
    for y in range(0,height):
        for x in range(0, width):
            tile = board.get((x,y),EMPTY)
            out = ''
            if tile == EMPTY:
                out = ' '
            elif tile == WALL:
                out = 'W'
            elif tile == BLOCK:
                out = 'B'
            elif tile == PADDLE:
                out = '-'
            elif tile == BALL:
                out = '*'
            print(out, end='')
        print('')

while not arcade.is_stopped():
    arcade.run_program()

    while not out_queue.empty():
        x = out_queue.get()
        y = out_queue.get()
        id = out_queue.get()
        if x == -1 and y == 0:
            print("Score: %u" % (id))
        else:
            if id == BALL:
                ball_pos = (x,y)
            elif id == PADDLE:
                paddle_pos = (x,y)
            else:
                board[(x,y)] = id
                max_x = max(x,max_x)
                max_y = max(x,max_y)

    paddle_direction = get_paddle_direction(paddle_pos, ball_pos)
    in_queue.put(paddle_direction)
