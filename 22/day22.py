import itertools


tracked_card_pos = 2019
deck_size = 10007


def deal_with_increment(tracked_card_pos, deck_size, increment):
    return (tracked_card_pos * increment) % deck_size

def cut(tracked_card_pos, deck_size, increment):
    if increment > 0:
        if tracked_card_pos < increment:
            return (deck_size - increment) + tracked_card_pos
        else:
            return tracked_card_pos - increment
    else:
        if tracked_card_pos < (deck_size + increment):
            return tracked_card_pos - increment
        else:
            return tracked_card_pos - (deck_size + increment)

def deal_into_new_stack(tracked_card_pos, deck_size):
    return  (deck_size - 1) - tracked_card_pos

with open("day22.input") as file:
    for line in file:
        if "deal with increment" in line:
            tracked_card_pos = deal_with_increment(tracked_card_pos, deck_size, int(line.split(" ")[3]))
        elif "cut" in line:
            tracked_card_pos = cut(tracked_card_pos, deck_size, int(line.split(" ")[1]))
        elif "deal into new stack" in line:
            tracked_card_pos = deal_into_new_stack(tracked_card_pos, deck_size)

print(tracked_card_pos)
