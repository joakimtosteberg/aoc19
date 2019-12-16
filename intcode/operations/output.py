from operation import Operation

class Output(Operation):
    def __init__(self):
        pass

    def execute(self, memory, arguments):
        self.output_func(arguments[0].get_read_value(memory))

    def num_arguments(self):
        return 1

    def get_opcode(self):
        return 4
