def get_fuel(mass):
    fuel = (int(mass/3)-2)
    if fuel < 0:
        fuel = 0
    return fuel

def get_fuel_recursively(mass):
    fuel = get_fuel(mass)
    if (fuel > 0):
        return fuel + get_fuel_recursively(fuel)
    return 0

total_module_fuel = 0
total_fuel = 0
with open("day1.input") as file:
    for line in file:
        fuel = get_fuel(int(line))
        total_module_fuel += get_fuel(int(line))
        total_fuel += fuel + get_fuel_recursively(fuel)

print("Fuel for module only: %s" % total_module_fuel)
print("Fuel for module and fuel: %s" % total_fuel)
