import gmpy2

def deal_with_increment(tracked_card_pos, deck_size, increment):
    return (tracked_card_pos * increment) % deck_size

def deal_with_increment_inv(tracked_card_pos, deck_size, increment):
    return gmpy2.invert(increment, deck_size) * tracked_card_pos % deck_size
    return (tracked_card_pos * increment) % deck_size

def cut(tracked_card_pos, deck_size, increment):
    return (tracked_card_pos - increment) % deck_size

def cut_inv(tracked_card_pos, deck_size, increment):
    return cut(tracked_card_pos, deck_size, -increment)

def deal_into_new_stack(tracked_card_pos, deck_size):
    return  (deck_size - 1) - tracked_card_pos

def deal_into_new_stack_inv(tracked_card_pos, deck_size):
    return deal_into_new_stack(tracked_card_pos, deck_size)

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

def reverse_shuffle_deck(tracked_card_pos, deck_size, iterations):
    for i in range(iterations):
        for instruction in reversed(instructions):
            if instruction[0] == 'd':
                tracked_card_pos = deal_with_increment_inv(tracked_card_pos, deck_size, instruction[1])
            elif instruction[0] == 'c':
                tracked_card_pos = cut_inv(tracked_card_pos, deck_size, instruction[1])
            elif instruction[0] == 's':
                tracked_card_pos = deal_into_new_stack_inv(tracked_card_pos, deck_size)
    return tracked_card_pos

print(shuffle_deck(2019, 10007, 1))

# F(x) = A*x + B (due to all operations being linear under modulus space)
# F(x) - F(x+1) = A*x + B - A*(x+1) + B = -A => A = F(x+1) - F(x)
# F(x) = A*x + B => B = A*x - F(x)

deck_size = 119315717514047
iterations = 101741582076661
F0 = reverse_shuffle_deck(2020, deck_size, 1)
F1 = reverse_shuffle_deck(2021, deck_size, 1)
A = F1 - F0
B = F0 - A * 2020

# F(F(F(...(F(x))))) = (A^n)*x + (A^(n-1) + A^(n-2) + ... + A + 1)*B = (A^n)*x + ((A^n-1) / (A-1)) * B mod S = (A^n)*x + ((A^n-1)*modinv(A-1,S))*B mod S

print((pow(A, iterations, deck_size) * 2020 + ((pow(A, iterations, deck_size) - 1) * gmpy2.invert(A-1,deck_size)*B)) % deck_size)
