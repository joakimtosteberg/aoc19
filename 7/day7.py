import sys 
sys.path.append('../intcode')

import intcode
import itertools

signal = 0
read_signal = False
phase_setting = 0

def read_input():
    global read_signal
    global phase_setting
    value = 0
    if read_signal:
        value = signal
    else:
        value = phase_setting
    read_signal = not read_signal
    return value

def provide_output(value):
    global signal
    signal = value

with open("day7.input") as file:
    program = [int(val) for val in file.read().split(',')]

    
amplifier = intcode.IntCode()
amplifier.attach_io(read_input,
                    provide_output)

max_signal = 0
max_signal_settings = []
for phase_settings in itertools.permutations([0, 1, 2, 3, 4]):
    signal = 0
    read_signal = False
    for phase_setting in phase_settings:
        amplifier.load_program(program)
        amplifier.run_program()
    if signal > max_signal:
        max_signal = signal
        max_signal_settings = phase_settings

print(max_signal)
print(max_signal_settings)
