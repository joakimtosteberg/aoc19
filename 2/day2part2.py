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

program = []
pc = 0

opcodes = {}
opcodes[1] = {'name': 'add',
              'func': opcode_add}
opcodes[2] = {'name': 'mult',
              'func': opcode_mult}
opcodes[99] = {'name': 'exit',
               'func': opcode_exit}

with open("day2.input") as file:
    program = [int(val) for val in file.read().split(',')]

wanted = 19690720

for noun in range(0,100):
    for verb in range(0,100):
        pc = 0
        mem = program[:]
        mem[1] = noun
        mem[2] = verb
        while pc >= 0:
            opcode = mem[pc]
            if not opcode in opcodes:
                break
            pc = opcodes[opcode]["func"](mem, pc)
        if mem[0] == wanted:
            print(100*noun+verb)
            exit(0)

print("Exit program")
print(mem)
