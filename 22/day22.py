import itertools


state = {'deck': list(range(0,10007))}

def deal_with_increment(state, increment):
    tmp_deck = state['deck'][:]
    for i in range(len(tmp_deck)):
        state['deck'][(i*increment) % len(tmp_deck)] = tmp_deck[i]

def cut(state, increment):
    state['deck'] = state['deck'][increment:] + state['deck'][0:increment]

def deal_into_new_stack(state):
    state['deck'].reverse()

with open("day22.input") as file:
    for line in file:
        if "deal with increment" in line:
            deal_with_increment(state, int(line.split(" ")[3]))
        elif "cut" in line:
            cut(state, int(line.split(" ")[1]))
        elif "deal into new stack" in line:
            deal_into_new_stack(state)

for i in range(len(state['deck'])):
    if state['deck'][i] == 2019:
        print(i)
