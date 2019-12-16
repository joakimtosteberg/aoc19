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
target_paddle_pos = None
first = True

def get_ball_impact(cur_pos, prev_pos, base_y):
    dx = cur_pos[0] - ball_pos[0]
    dy = cur_pos[1] - ball_pos[1]
    return (cur_pos[0] + dx * (base_y - cur_pos[1]),y)

def print_board(board, width, height):
    for y in range(0,height):
        for x in range(0, width):
            tile = EMPTY
            if (x,y) in board:
                tile = board[(x,y)]
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
                if ball_pos is not None:
                    if y > ball_pos[1]:
                        target_paddle_pos = get_ball_impact((x,y), ball_pos, paddle_pos[1])
                        print("paddle target=%s" % (str(target_paddle_pos)))
                    else:
                        target_paddle_pos = paddle_pos
                ball_pos = (x,y)
            elif id == PADDLE:
                paddle_pos = (x,y)
                if target_paddle_pos is None:
                    target_paddle_pos = paddle_pos
            max_x = max(x,max_x)
            max_y = max(x,max_y)
            board[(x,y)] = id

    #    print_board(board, max_x+1, max_y+1)
    print("ball_target=%s" % (str(ball_pos)))
    if paddle_pos == target_paddle_pos:
        in_queue.put(0)
    elif paddle_pos[0] < target_paddle_pos[0]:
        in_queue.put(1)
    else:
        in_queue.put(-1)
