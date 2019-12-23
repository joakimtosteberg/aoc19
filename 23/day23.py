import sys
sys.path.append('../intcode')

import intcode

with open("day23.input") as file:
    program = [int(val) for val in file.read().split(',')]

computers = [intcode.IntCode() for i in range(50)]

for i in range(len(computers)):
    computers[i].load_program(program)
    # Set network address
    computers[i].get_input_queue().put(i)

nat_value = None
prev_nat_value = None
first_nat_value = True
idle_iterations = 0
while True:
    all_output_empty = True
    for computer in computers:
        computer.run_program()
        src = computer.get_output_queue()
        computer.get_input_queue().put(-1)
        while not src.empty():
            all_output_empty = False
            addr = src.get()
            x = src.get()
            y = src.get()
            if addr == 255:
                nat_value = (x,y)
                if first_nat_value:
                    first_nat_value = False
                    print("First packet to NAT: %s" % str(nat_value))
            else:
                dest = computers[addr].get_input_queue()
                dest.put(x)
                dest.put(y)

    all_input_empty = True
    for computer in computers:
        if computer.get_input_queue().size() > 1:
            all_empty = False
            break

    if all_input_empty and all_output_empty:
        idle_iterations += 1
        if idle_iterations > 1:
            if (prev_nat_value and
                prev_nat_value[1] == nat_value[1]):
                print("First packet from NAT with same y as previous: %s" % str(nat_value))
                break

            prev_nat_value = nat_value
            computers[0].get_input_queue().put(nat_value[0])
            computers[0].get_input_queue().put(nat_value[1])
    else:
        idle_iterations = 0
