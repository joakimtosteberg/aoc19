import itertools

moons = []

class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        return ("x=%u, y=%u, z=%u" % (self.x, self.y, self.z))

class Moon:
    def __init__(self):
        self.pos = Coord()
        self.vel = Coord()

    def set_position(self, pos):
        self.pos.x = int(pos[0].split('=')[1])
        self.pos.y = int(pos[1].split('=')[1])
        self.pos.z = int(pos[2].split('=')[1])

    def __str__(self):
        return "pos=<%s>, vel=<%s>" % (str(self.pos), str(self.vel))

    def __repr__(self):
        return "(%s)" % (self.__str__())

with open("day12.input") as file:
    for line in file:
        moon = Moon()
        moon.set_position(line.strip('<>\n').split(', '))
        moons.append(moon)


def get_velocity_change(c1, c2):
    if c1 < c2:
        return 1
    elif c1 > c2:
        return -1
    else:
        return 0

def update_velocity(moon_pair):
    vel_change = get_velocity_change(moon_pair[0].pos.x, moon_pair[1].pos.x)
    moon_pair[0].vel.x += vel_change
    moon_pair[1].vel.x -= vel_change

    vel_change = get_velocity_change(moon_pair[0].pos.y, moon_pair[1].pos.y)
    moon_pair[0].vel.y += vel_change
    moon_pair[1].vel.y -= vel_change

    vel_change = get_velocity_change(moon_pair[0].pos.z, moon_pair[1].pos.z)
    moon_pair[0].vel.z += vel_change
    moon_pair[1].vel.z -= vel_change

def update_position(moon):
    moon.pos.x += moon.vel.x
    moon.pos.y += moon.vel.y
    moon.pos.z += moon.vel.z

def get_potential_energy(moon):
    return abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)

def get_kinetic_energy(moon):
    return abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)

def get_total_energy(moon):
    return get_potential_energy(moon) * get_kinetic_energy(moon)

iterations = 1000

for i in range(0,iterations):
    for pair in itertools.combinations(moons, 2):
        update_velocity(pair)
    for moon in moons:
        update_position(moon)

total_energy = 0
for moon in moons:
    print(moon)
    total_energy += get_total_energy(moon)

print(total_energy)
