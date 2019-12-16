from operation import Operation

class Equal(Operation):
    def __init__(self):
        pass

    def execute(self, memory, arguments):
        arg1 = arguments[0].get_read_value(memory)
        arg2 = arguments[1].get_read_value(memory)
        dest = arguments[2].get_write_value(memory)
        memory[dest] = (1 if arg1 == arg2 else 0)

    def num_arguments(self):
        return 3

    def get_opcode(self):
        return 8
