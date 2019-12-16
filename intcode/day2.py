def opcode_add(mem, pc):
    arg1 = mem[pc+1]
    arg2 = mem[pc+2]
    dest = mem[pc+3]
    mem[dest] = mem[arg1] + mem[arg2]
    return pc + 4

def opcode_mult(mem, pc):
    arg1 = mem[pc+1]
    arg2 = mem[pc+2]
    dest = mem[pc+3]
    mem[dest] = mem[arg1] * mem[arg2]
    return pc + 4

def opcode_exit(mem, pc):
    return -1

mem = []
pc = 0

opcodes = {}
opcodes[1] = {'name': 'add',
              'func': opcode_add}
opcodes[2] = {'name': 'mult',
              'func': opcode_mult}
opcodes[99] = {'name': 'exit',
               'func': opcode_exit}

with open("day2.input") as file:
    mem = [int(val) for val in file.read().split(',')]

mem[1] = 12
mem[2] = 2
    
while pc >= 0:
    opcode = mem[pc]
    if not opcode in opcodes:
        print("Invalid opcode %u" % opcode)
        exit(1)
#    print("%s @ %u" % (opcodes[opcode]["name"], pc))
    pc = opcodes[opcode]["func"](mem, pc)

print("Exit program")
print(mem)
