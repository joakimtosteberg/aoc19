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
    with open(maze_file) as file:
        y = 0
        for line in file:
            for x in range(0, len(line)-1):
                if line[x] == ' ':
                    continue
                if line[x] in "#.":
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
        labels[label_pos] = label_name
        
    return maze, labels

def find_label_pos(labels, label, exclude_pos = None):
    for pos in labels:
        if pos == exclude_pos:
            continue
        if labels[pos] == label:
            return pos

def explore_maze(maze, labels, start):
    track = {start: 0}
    positions = [start]
    for steps in itertools.count(1):
        next_positions = []
#       print(next_positions)
        for pos in positions:
            for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                next_pos = (pos[0] + direction[0],
                            pos[1] + direction[1])

                # Do teleportation
                if maze.get(next_pos, ' ') == ' ':
                    next_pos = find_label_pos(labels, labels[pos], pos)

                if next_pos in track:
                    continue

                track[next_pos] = steps
                if maze.get(next_pos, ' ') == '.':
                    next_positions.append(next_pos)
        if not next_positions:
            break
        positions = next_positions
    return track

                

maze, labels = read_maze("day20.input")

start = find_label_pos(labels, "AA")
track = explore_maze(maze, labels, start)
end = find_label_pos(labels, "ZZ")
print(track[end])
