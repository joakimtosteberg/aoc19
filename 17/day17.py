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
                robot_dir = (0,1)
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
                    robot_dir = (0,1)
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
            nodes[pos] = {}
            ship_map[(pos)]['allowed_visits'] += 1
            checksum += pos[0]*pos[1]
        elif is_end(ship_map, pos) or is_corner(ship_map, pos):
            nodes[pos] = {}
    return nodes,checksum

def build_graph(ship_map, nodes):
    search_dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for node_pos in nodes:
        for direction in search_dirs:
            for length in itertools.count(1):
                pos = (node_pos[0] + direction[0] * length, node_pos[1] + direction[1] * length)
                if not pos in ship_map:
                    break
                if pos in nodes:
                    nodes[node_pos][pos] = length
                    break

def search_graph(graph, pos):
    search_sets = [(graph,pos)]
    while search_sets:
        next_search_sets = []
        print(len(search_sets))
        for search_set in search_sets:
            for node_pos in search_set[0][search_set[1]]:
                new_graph = copy.deepcopy(search_set[0])
                del new_graph[search_set[1]][node_pos]
                if not new_graph[search_set[1]]:
                    del new_graph[search_set[1]]
                del new_graph[node_pos][search_set[1]]
                if not new_graph[node_pos]:
                    del new_graph[node_pos]
                    if not new_graph:
                        print("PATH FOUND")
                        return
                    continue
                next_search_sets.append((new_graph,node_pos))
        search_sets = next_search_sets

program[0] = 2
system.load_program(program)
system.run_program()

robot_pos, robot_dir = read_map(out_queue, ship_map, True)
#robot_pos, robot_dir = read_map2(ship_map)
graph, checksum = get_nodes(ship_map, robot_pos)
print("Alignemnt calibration=%u" % (checksum))
build_graph(ship_map, graph)
search_graph(graph, robot_pos)
