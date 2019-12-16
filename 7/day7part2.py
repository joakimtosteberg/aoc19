import sys 
sys.path.append('../intcode')

import intcode
import itertools

signal = 0
read_signal = False
phase_setting = 0


with open("day7.input") as file:
    program = [int(val) for val in file.read().split(',')]

    
amplifiers = [ intcode.IntCode(),
               intcode.IntCode(),
               intcode.IntCode(),
               intcode.IntCode(),
               intcode.IntCode() ]

prev_amplifier = None
for amplifier in amplifiers:
    amplifier.load_program(program)
    if prev_amplifier:
        amplifier.set_input_queue(prev_amplifier.get_output_queue())
    prev_amplifier = amplifier

amplifiers[0].set_input_queue(amplifiers[4].get_output_queue())

max_signal = 0
max_signal_settings = []

for phase_settings in itertools.permutations([9, 8, 7, 6, 5]):

    for i in range(0,len(amplifiers)):
        amplifiers[i].load_program(program)
        amplifiers[i].get_input_queue().put(phase_settings[i])

    amplifiers[0].get_input_queue().put(0)
    program_done = False
    while not program_done:
        program_done = True
        for amplifier in amplifiers:
            if not amplifier.is_stopped():
                amplifier.run_program()
                program_done = False
    signal = amplifiers[4].get_output_queue().get()
    if signal > max_signal:
        max_signal = signal
        max_signal_settings = phase_settings


print(max_signal)
print(max_signal_settings)
