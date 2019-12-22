import itertools

def find_next_label_part(pos, label_parts):
    next_pos = (pos[0]+1,pos[1])
    if next_pos in label_parts:
        return next_pos
    next_pos = (pos[0],pos[1]-1)
    if next_pos in label_parts:
        return next_pos

def read_maze(maze_file):
    maze = {}
    label_parts = {}
    labels = {}
    maze_max_x = 0
    maze_max_y = 0
    with open(maze_file) as file:
        y = 0
        for line in file:
            for x in range(0, len(line)-1):
                if line[x] == ' ':
                    continue
                if line[x] in "#.":
                    maze_max_x = max(x,maze_max_x)
                    maze_max_y = max(y,maze_max_y)
                    maze[(x,y)] = line[x]
                else:
                    label_parts[(x,y)] = {'name': line[x], 'used': False}
            y += 1

    for pos in label_parts:
        # Part already used for a label, don't re-use
        if label_parts[pos]['used']:
            continue

        next_pos = (pos[0],pos[1]+1)
        label_pos = None
        label_name = ""
        if next_pos in label_parts:
            label_name = label_parts[pos]['name'] + label_parts[next_pos]['name']
            label_pos = (next_pos[0],next_pos[1]+1)
            if maze.get(label_pos, '') != '.':
                label_pos = (pos[0],pos[1]-1)
        else:
            next_pos = (pos[0]+1,pos[1])
            label_name = label_parts[pos]['name'] + label_parts[next_pos]['name']
            label_pos = (next_pos[0]+1,next_pos[1])
            if maze.get(label_pos, '') != '.':
                label_pos = (pos[0]-1,pos[1])

        label_parts[pos]['used'] = True
        label_parts[next_pos]['used'] = True
        depth_change = 0
        if ((label_pos[0] in [2,maze_max_x]) or
            (label_pos[1] in [2,maze_max_y])):
            depth_change = -1
        else:
            depth_change = 1
        labels[label_pos] = (label_name,depth_change)
        
    return maze, labels

def find_label_pos(labels, label, exclude_pos = None):
    for pos in labels:
        if pos == exclude_pos:
            continue
        if labels[pos][0] == label:
            return pos

def explore_maze(maze, labels, start, end, recurse = False):
    tracks = {}
    tracks[0] = {start: 0}
    positions = [(start,0)]
    for steps in itertools.count(1):
        next_positions = []
        for pos in positions:
            for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0][0] + direction[0],
                            pos[0][1] + direction[1])
                depth = pos[1]

                # Exit found, stop exploration
                if next_pos == end and depth == 0:
                    tracks[depth][next_pos] = steps
                    return tracks

                # Do teleportation
                if maze.get(next_pos, ' ') == ' ':
                    depth_change = labels[pos[0]][1]
                    # Outer portal doesn't work on depth 0
                    if recurse and depth == 0 and depth_change == -1:
                        continue
                    next_pos = find_label_pos(labels, labels[pos[0]][0], pos[0])
                    if recurse:
                        depth += depth_change

                if next_pos in tracks[depth]:
                    continue

                if maze.get(next_pos, ' ') == '.':
                    next_positions.append((next_pos,depth))
                    tracks[depth][next_pos] = steps

        if not next_positions:
            break
        positions = next_positions
    return tracks

                

maze, labels = read_maze("day20.input")

start = find_label_pos(labels, "AA")
end = find_label_pos(labels, "ZZ")
tracks = explore_maze(maze, labels, start, end)
print(tracks[0][end])
