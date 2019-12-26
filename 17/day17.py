import sys
import copy
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
                robot_dir = (0,-1)
                ship_map[pos] = {'visits': 0,  'allowed_visits': 1}
            pos = (pos[0]+1, pos[1])
    return robot_pos, robot_dir

def read_map2(ship_map):
    with open("day17.part2.input.example") as file:
        robot_pos = None
        robot_dir = None
        pos = (0,0)
        for line in file:
            for obj in line.rstrip():
                if obj == '#':
                    ship_map[pos] = {'visits': 0,  'allowed_visits': 1}
                elif obj == '^':
                    robot_pos = pos
                    robot_dir = (0,-1)
                    ship_map[pos] = {'visits': 0,  'allowed_visits': 1}
                pos = (pos[0]+1, pos[1])
            pos = (0, pos[1]+1)
        return robot_pos, robot_dir

def is_corner(ship_map, pos):
    total_num_paths = 0
    for step in [(1,0),(0,1)]:
        next_pos1 = (pos[0] + step[0], pos[1] + step[1])
        next_pos2 = (pos[0] - step[0], pos[1] - step[1])
        num_paths = 0
        if ((next_pos1 in ship_map and next_pos2 in ship_map) or
            (next_pos1 not in ship_map and next_pos2 not in ship_map)):
            return False
    return True

def is_end(ship_map, pos):
    num_paths = 0
    for step in [(1,0),(-1,0),(0,1),(0,-1)]:
        num_paths += 1 if (pos[0] + step[0], pos[1] + step[1]) in ship_map else 0
    return num_paths == 1

def get_nodes(ship_map, robot_pos):
    checksum = 0
    nodes = {robot_pos:{}}
    for pos in ship_map:
        if (((pos[0] + 1, pos[1]) in ship_map) and
            ((pos[0] - 1, pos[1]) in ship_map) and
            ((pos[0], pos[1] + 1) in ship_map) and
            ((pos[0], pos[1] - 1) in ship_map)):
            checksum += pos[0]*pos[1]
        elif is_end(ship_map, pos) or is_corner(ship_map, pos):
            nodes[pos] = None
    return nodes,checksum

def find_next_node(ship_map, nodes, node_pos, prev = None):
    search_dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for direction in search_dirs:
        for length in itertools.count(1):
            next_pos = (node_pos[0] + direction[0] * length, node_pos[1] + direction[1] * length)
            if not next_pos in ship_map:
                if length > 1:
                    next_pos = (node_pos[0] + direction[0] * (length - 1), node_pos[1] + direction[1] * (length - 1))
                    if next_pos != prev:
                        return next_pos,direction,(length-1)
                break
    return None,None,None

def get_turn(current_direction, next_direction):
    directions = [(0,-1), (1,0), (0,1), (-1,0)]
    if ((directions.index(current_direction) + 1) % len(directions)) == directions.index(next_direction):
        return "R"
    else:
        return "L"

def get_path(ship_map, nodes, robot_pos, robot_dir):
    prev_node = None
    cur_node = robot_pos
    cur_dir = robot_dir
    path = []
    while True:
        next_node,next_dir,length = find_next_node(ship_map, nodes, cur_node, prev_node)
        if not next_node:
            return path

        path.append(get_turn(cur_dir, next_dir))
        path.append(str(length))

        nodes[cur_node] = next_node
        prev_node = cur_node
        cur_node = next_node
        cur_dir = next_dir

def input_string(string, in_queue):
    for ch in string:
        in_queue.put(ord(ch))
    in_queue.put(ord('\n'))

program[0] = 2
system.load_program(program)
system.run_program()

robot_pos, robot_dir = read_map(out_queue, ship_map, True)
#robot_pos, robot_dir = read_map2(ship_map)
nodes, checksum = get_nodes(ship_map, robot_pos)
print("Alignemnt calibration=%u" % (checksum))
path = get_path(ship_map, nodes, robot_pos, robot_dir)
print(''.join(path))

A="R,8,L,4,R,4,R,10,R,8"
B="L,12,L,12,R,8,R,8"
C="R,10,R,4,R,4"
seq="A,A,B,C,B,C,B,C,C,A"

input_string(seq, in_queue)
input_string(A, in_queue)
input_string(B, in_queue)
input_string(C, in_queue)
input_string("n", in_queue)
system.run_program()
while not out_queue.empty():
    data = out_queue.get()
    if data > 400:
        print(data)
    else:
        print(chr(data), end='')
