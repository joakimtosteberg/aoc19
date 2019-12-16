from operation import Operation

class JumpIfTrue(Operation):
    def __init__(self):
        pass

    def execute(self, memory, arguments):
        arg1 = arguments[0].get_read_value(memory)
        arg2 = arguments[1].get_read_value(memory)
        if arg1 != 0:
            return arg2

        return None

    def num_arguments(self):
        return 2

    def get_opcode(self):
        return 5
