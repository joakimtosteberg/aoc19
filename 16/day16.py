import numpy
import math

sequence = []
with open("day16.input") as file:
    str_seq = file.read()
    initial_sequence = numpy.matrix([int(char) for char in str_seq])

def get_pattern(base_pattern, position):
    pattern = []
    for num in base_pattern:
        pattern.extend([num] * (position + 1))

    return pattern

def extend_pattern(pattern, length):
    start_pos = 1
    extended_pattern = pattern * math.ceil((length + start_pos) / len(pattern))
    return extended_pattern[start_pos:length+start_pos]
BASE_PATTERN = [0,1,0,-1]


def fft(sequence, pattern):
    row = []
    for i in range(0,sequence.size):
        multiplier = numpy.matrix(extend_pattern(get_pattern(pattern, i), sequence.size)).transpose()
        row.append(abs(sequence*multiplier).item(0) % 10)
    return numpy.matrix(row)

passes = 100
sequence = initial_sequence
for i in range(0, passes):
    sequence = fft(sequence, BASE_PATTERN)
list_seq = sequence.tolist()[0]
print(list_seq[0:8])


offset =  int(str_seq[0:7])
passes = 10000
sequence = initial_sequence
for i in range(0, passes):
    sequence = fft(sequence, BASE_PATTERN)

list_seq = sequence.tolist()[0]
print(list_seq[offset:offset+8])