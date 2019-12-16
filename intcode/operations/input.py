from operation import Operation

class Input(Operation):
    def __init__(self):
        pass

    def execute(self, memory, arguments):
        dest = arguments[0].get_write_value(memory)
        memory[dest] = self.input_func()

    def num_arguments(self):
        return 1

    def get_opcode(self):
        return 3
