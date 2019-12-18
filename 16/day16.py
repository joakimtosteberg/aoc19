import numpy
import math

sequence = []
with open("day16.input") as file:
    str_seq = file.read()
    initial_sequence = [int(char) for char in str_seq]

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

def fft_second_half(half_sequence):
    for i in range(len(half_sequence)-2,-1,-1):
        half_sequence[i] = (half_sequence[i] + half_sequence[i+1])%10
    pass

passes = 100
sequence = numpy.matrix(initial_sequence)
for i in range(0, passes):
    sequence = fft(sequence, BASE_PATTERN)
list_seq = sequence.tolist()[0]
print(list_seq[0:8])


offset =  int(str_seq[0:7])
half_sequence = initial_sequence * 5000
offset -= len(half_sequence)
print(offset)
print(len(half_sequence))
passes = 100
for i in range(passes):
    fft_second_half(half_sequence)

print(half_sequence[offset:offset+8])
