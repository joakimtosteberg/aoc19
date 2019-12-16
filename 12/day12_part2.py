import itertools
import copy
import math

moons = []

class Moon:
    def __init__(self):
        self.pos = [0,0,0]
        self.vel = [0,0,0]

    def set_position(self, pos):
        self.pos[0] = int(pos[0].split('=')[1])
        self.pos[1] = int(pos[1].split('=')[1])
        self.pos[2] = int(pos[2].split('=')[1])

    def __str__(self):
        return "pos=%s, vel=%s" % (str(self.pos), str(self.vel))

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

def update_velocity(moon_pair, coord):
    vel_change = get_velocity_change(moon_pair[0].pos[coord], moon_pair[1].pos[coord])
    moon_pair[0].vel[coord] += vel_change
    moon_pair[1].vel[coord] -= vel_change

def update_position(moon, coord):
    moon.pos[coord] += moon.vel[coord]

def find_cycle_length(moons, coord):
    cycle_found = False
    initial_moons = [copy.deepcopy(moon) for moon in moons]
    iterations = 0
    while not cycle_found:
        iterations += 1
        for pair in itertools.combinations(moons, 2):
            update_velocity(pair, coord)
        cycle_found = True
        for i in range(0,len(moons)):
            update_position(moons[i], coord)
            if moons[i].pos[coord] != initial_moons[i].pos[coord] or moons[i].vel[coord] != initial_moons[i].vel[coord]:
                cycle_found = False
    return iterations


x_cycle = find_cycle_length(moons, 0)
y_cycle = find_cycle_length(moons, 1)
z_cycle = find_cycle_length(moons, 2)

def lcm(a,b):
    return abs(a*b) // math.gcd(a, b)

print("cycles=%u" % (lcm(lcm(x_cycle, y_cycle), z_cycle)))
