from operation import Operation, StopException

class Mult(Operation):
    def __init__(self):
        pass

    def execute(self, memory, arguments):
        raise StopException()

    def num_arguments(self):
        return 0

    def get_opcode(self):
        return 99
