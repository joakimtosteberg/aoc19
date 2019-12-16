import sys 
sys.path.append('../intcode')

import intcode

directions  = [(0,-1), (1,0), (0,1), (-1,0)]
hull = {}

def get_color(hull, pos):
    if pos in hull:
        return hull[pos]
    else:
        return 0

with open("day11.input") as file:
    program = [int(val) for val in file.read().split(',')]



i = 0

def paint_hull(program, hull):
    paintbot = intcode.IntCode()
    paintbot.load_program(program)

    global directions
    pos = (0,0)
    direction = 0

    while True:
        paintbot.run_program()
        if paintbot.is_stopped():
            break
        if not paintbot.get_output_queue().empty():
            color = paintbot.get_output_queue().get()
            turn = paintbot.get_output_queue().get()
            direction = (direction + (-1 if turn == 0 else  1)) % len(directions)
            hull[pos] = color
            pos = (pos[0]+directions[direction][0], pos[1]+directions[direction][1])
        paintbot.get_input_queue().put(get_color(hull, pos))
    return hull

hull = paint_hull(program, hull)

print(len(hull))
    
def print_hull(hull):
    max_x = None
    max_y = None
    min_x = None
    min_y = None
    for item in hull:
        if max_x is None:
            max_x = min_x = item[0]
            max_y = min_y = item[1]
        max_x = max(max_x, item[0])
        min_x = min(min_x, item[0])
        max_y = max(max_y, item[1])
        min_y = min(min_y, item[1])

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in hull:
                if hull[(x,y)] == 1:
                    print('1', end='')
                else:
                    print(' ', end='')
            else:
                print(' ', end='')
        print('')

hull = {}
hull[(0,0)] = 1
hull = paint_hull(program, hull)
print_hull(hull)
