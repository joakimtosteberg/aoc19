import math

prod_chart = {}
available_resources = {}
basic_requirements = {}

with open("day14.input") as file:
    for line in file:
        items = line.rstrip().split(' => ')
        requirements = {}
        for pair in items[0].split(', '):
            requirement = pair.split(' ')
            requirements[requirement[1]] = int(requirement[0])
        production = items[1].split(' ')
        prod_chart[production[1]] = { 'amount': int(production[0]),
                                      'req': requirements }

def produce_resource(prod_chart, available_resources, resource, amount):
    #print("PRODUCE %u of %s" % (amount, resource))
    if not resource in available_resources:
        available_resources[resource] = 0
    to_produce = max(0, amount - available_resources[resource])
    if to_produce > 0:
        if resource not in prod_chart:
            if resource not in basic_requirements:
                basic_requirements[resource] = 0
            basic_requirements[resource] += amount
            available_resources[resource] += amount
        else:
            production_rounds = math.ceil(to_produce / prod_chart[resource]["amount"])
            for requirement in prod_chart[resource]["req"]:
                produce_resource(prod_chart, available_resources, requirement, prod_chart[resource]["req"][requirement] * production_rounds)
                #print("USE %u of %s" % (prod_chart[resource]["req"][requirement] * to_produce, requirement))
                available_resources[requirement] -= prod_chart[resource]["req"][requirement] * production_rounds
            #print(resource)
            available_resources[resource] += prod_chart[resource]["amount"] * production_rounds

produce_resource(prod_chart, available_resources, "FUEL", 1)
print(basic_requirements)
print(available_resources)
#print(prod_chart)
