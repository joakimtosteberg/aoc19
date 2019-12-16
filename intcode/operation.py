from abc import ABC, abstractmethod

class StopException(Exception):
    pass

class Operation(ABC):
    operations = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.operations.append(cls)

    def register_io(self, input_func, output_func):
        self.input_func = input_func
        self.output_func = output_func

    @abstractmethod
    def num_arguments(self):
        pass
        
    @abstractmethod
    def execute(self, memory, arguments):
        pass

    @abstractmethod
    def get_opcode(self, args):
        pass
