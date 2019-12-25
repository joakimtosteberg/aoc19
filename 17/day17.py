import sys
import itertools
sys.path.append('../intcode')

import intcode

with open("day17.input") as file:
    program = [int(val) for val in file.read().split(',')]

system = intcode.IntCode()
system.load_program(program)

in_queue = system.get_input_queue()
out_queue = system.get_output_queue()

ship_map = {}

system.run_program()

def read_map(out_queue, ship_map, do_print):
    pos = (0,0)
    robot_pos = None
    robot_dir = None
    was_newline = False
    map_done = False
    while not out_queue.empty():
        obj = chr(out_queue.get())
        if do_print:
            print(obj, end='')
        if obj == '\n':
            if was_newline:
                map_done = True
            else:
                was_newline = True
                pos = (0, pos[1]+1)
        elif not map_done:
            was_newline = False
            if obj == '#':
                ship_map[pos] = {'visits': 0,  'allowed_visits': 1}
            elif obj == '^':
                robot_pos = pos
                robot_dir = (1,0)
            pos = (pos[0]+1, pos[1])
    return robot_pos, robot_dir

def get_intersections(ship_map):
    checksum = 0
    intersections = {}
    for pos in ship_map:
        if (((pos[0] + 1, pos[1]) in ship_map) and
            ((pos[0] - 1, pos[1]) in ship_map) and
            ((pos[0], pos[1] + 1) in ship_map) and
            ((pos[0], pos[1] - 1) in ship_map)):
            intersections[pos] = 1
            ship_map[(pos)]['allowed_visits'] += 1
            checksum += pos[0]*pos[1]
    return intersections,checksum

def is_end(ship_map, pos):
    num_paths = 0
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        num_paths += 1 if (pos[0] + step[0], pos[1] + step[1]) in ship_map else 0
    return num_paths == 1

def all_visited(ship_map):
    for pos in ship_map:
        if ship_map[pos]['visits'] == 0:
            return False
    return True

def search(ship_map, robot_pos, robot_dir, depth=0):
    destinations = {}
    has_destinations = True
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        length = 0
        for length in itertools.count(1):
            if depth == 0:
                print(length)
            pos = (robot_pos[0] + step[0] * length, robot_pos[1] + step[1] * length)
            next_search = None
            if pos in ship_map:
                ship_map[pos]['visits'] += 1
                if ship_map[pos]['visits'] > ship_map[pos]['allowed_visits']:
                    length += 1
                    break
                elif ship_map[pos]['allowed_visits'] == 2:
                    next_search = pos
            elif length > 1:
                next_search = (robot_pos[0] + step[0] * (length - 1), robot_pos[1] + step[1] * (length -1))

            if next_search:
                if is_end(ship_map, next_search):
                    if all_visited(ship_map):
                        print("ALL VISISTED")
                else:
                    search(ship_map, next_search, robot_dir, depth+1)
                    destinations[next_search] = 1

            if pos not in ship_map:
                break

        for length in reversed(range(1,length)):
            pos = (robot_pos[0] + step[0] * length, robot_pos[1] + step[1] * length)
            if pos in ship_map:
                ship_map[pos]['visits'] -= 1

    return destinations


program[0] = 2
system.load_program(program)
system.run_program()

robot_pos, robot_dir = read_map(out_queue, ship_map, True)
intersections, checksum = get_intersections(ship_map)

print("Alignemnt calibration=%u" % (checksum))

print(search(ship_map, robot_pos, robot_dir))
