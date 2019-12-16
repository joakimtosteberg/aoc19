def calculate_orbits(orbitmap, center_object, depth):
    num_orbits = len(orbitmap[center_object]) * depth
    for orbiting_object in orbitmap[center_object]:
        if orbiting_object in orbitmap:
            num_orbits += calculate_orbits(orbitmap, orbiting_object, depth + 1)
    return num_orbits

def get_path(orbitmap, position, destination):
    if not position in orbitmap:
        return []

    if destination in orbitmap[position]:
        return [position]
    for orbiting_object in orbitmap[position]:
        path = get_path(orbitmap, orbiting_object, destination)
        if path:
            path.insert(0, position)
            return path
    return []

orbits = []
with open("day6.input") as file:
    for line in file:
        orbits.append(line.rstrip().split(")"))

orbitmap = {}
for orbit in orbits:
    if orbit[0] not in orbitmap:
        orbitmap[orbit[0]] = [orbit[1]]
    else:
        orbitmap[orbit[0]].append(orbit[1])

num_orbits = calculate_orbits(orbitmap, "COM", 1)
print("Number of direct and indirect orbits: %u" % num_orbits)

path_to_san = get_path(orbitmap, "COM", "SAN")
#print(path_to_san)
path_to_you  = get_path(orbitmap, "COM", "YOU")
#print(path_to_you)

for i in range(0,len(path_to_san)):
    if path_to_san[i] != path_to_you[i]:
        print("Orbital transfers to SAN: %u" % (len(path_to_san) + len(path_to_you) - 2*i))
        break
