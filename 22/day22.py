def deal_with_increment(tracked_card_pos, deck_size, increment):
    return (tracked_card_pos * increment) % deck_size

def cut(tracked_card_pos, deck_size, increment):
    return tracked_card_pos - increment % deck_size

def deal_into_new_stack(tracked_card_pos, deck_size):
    return  (deck_size - 1) - tracked_card_pos

instructions = []
with open("day22.input") as file:
    for line in file:
        if "deal with increment" in line:
            instructions.append(('d',int(line.split(" ")[3])))
        elif "cut" in line:
            instructions.append(('c',int(line.split(" ")[1])))
        elif "deal into new stack" in line:
            instructions.append(('s',None))

def shuffle_deck(tracked_card_pos, deck_size, iterations):
    for i in range(iterations):
        for instruction in instructions:
            if instruction[0] == 'd':
                tracked_card_pos = deal_with_increment(tracked_card_pos, deck_size, instruction[1])
            elif instruction[0] == 'c':
                tracked_card_pos = cut(tracked_card_pos, deck_size, instruction[1])
            elif instruction[0] == 's':
                tracked_card_pos = deal_into_new_stack(tracked_card_pos, deck_size)
    return tracked_card_pos

print(shuffle_deck(2019, 10007, 1))
