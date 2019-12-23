import pkgutil
import sys
import collections

class InvalidAddressingModeException(Exception):
    pass

class WaitInputException(Exception):
    pass

class OpCode:
    def __init__(self, num_input, store_result, func):
        self.num_input = num_input
        self.store_result = store_result
        self.func = func

class IOQueue:
    def __init__(self):
        self.deque = collections.deque()

    def empty(self):
        return not self.deque

    def put(self, value):
        self.deque.append(value)

    def get(self):
        return self.deque.popleft()

    def size(self):
        return len(self.deque)

class IntCode:

    def __init__(self):
        self.memory = {}
        self.pc = 0
        self.relative_base = 0
        self.input_func = None
        self.output_func = None
        self.input_queue = IOQueue()
        self.output_queue = IOQueue()
        self.stopped = False

        self.ops = { 1: OpCode(2, True, lambda args: args[0] + args[1]),
                     2: OpCode(2, True, lambda args: args[0] * args[1]),
                     3: OpCode(0, True, self.get_input),
                     4: OpCode(1, False, self.provide_output),
                     5: OpCode(2, False, self.jmp_if_true),
                     6: OpCode(2, False, self.jmp_if_false),
                     7: OpCode(2, True, self.is_less_than),
                     8: OpCode(2, True, self.is_equal),
                     9: OpCode(1, False, self.modify_relative_base),
                     99: OpCode(0, False, self.stop_program)
        }

    def stop_program(self, arguments):
        self.stopped = True

    def jmp_if_true(self, arguments):
        if arguments[0]:
            self.pc = arguments[1]

    def is_less_than(self, arguments):
        return 1 if arguments[0] < arguments[1] else 0

    def is_equal(self, arguments):
        return 1 if arguments[0] == arguments[1] else 0

    def jmp_if_false(self, arguments):
        if not arguments[0]:
            self.pc = arguments[1]

    def modify_relative_base(self, arguments):
        self.relative_base += arguments[0]

    def get_input(self, arguments):
        if self.input_func:
            return self.input_func()
        if self.input_queue.empty():
            raise WaitInputException()
        return self.input_queue.get()

    def provide_output(self, arguments):
        value = arguments[0]
        if self.output_func:
            self.output_func(value)
            return
        self.output_queue.put(value)

    def get_input_queue(self):
        return self.input_queue

    def set_input_queue(self, input_queue):
        self.input_queue = input_queue

    def get_output_queue(self):
        return self.output_queue

    def set_output_queue(self, output_queue):
        self.output_queue = output_queue

    def attach_io(self, input_func, output_func):
        self.input_func = input_func
        self.output_func = output_func

    def read_memory(self, address):
        return self.memory.get(address, 0)

    def get_input_arguments(self, address_modes, num_arguments):
        arguments = []
        for i in range(0, num_arguments):
            address_mode = address_modes % 10
            address_modes = int(address_modes / 10)
            value = self.read_memory(self.pc)
            self.pc += 1
            if address_mode == 0:
                arguments.append(self.read_memory(value))
            elif address_mode == 1:
                arguments.append(value)
            elif address_mode == 2:
                arguments.append(self.read_memory(self.relative_base + value))
            else:
                raise InvalidAddressingModeException()
        return arguments, address_modes

    def store_result(self, value, address_mode):
        if address_mode == 0:
            addr = self.read_memory(self.pc)
        elif address_mode == 2:
            addr = self.relative_base + self.read_memory(self.pc)
        else:
            raise InvalidAddressingModeException()
        self.memory[addr] = value
        self.pc += 1


    def load_program(self, program):
        for i in range(0, len(program)):
            self.memory[i] = program[i]
        self.pc = 0
        self.relative_base = 0
        self.stopped = False

    def run_program(self):
        try:
            while not self.stopped:
                instruction = self.read_memory(self.pc)
                opcode = (instruction % 100)
                address_modes = int(instruction / 100)
                self.pc += 1
                if not opcode in self.ops:
                    print("Invalid opcode %u" % opcode)
                    sys.exit(1)
                operation = self.ops[opcode]
                input_arguments, address_modes = self.get_input_arguments(address_modes,
                                                                          operation.num_input)
                ret = operation.func(input_arguments)
                if operation.store_result:
                    self.store_result(ret, address_modes % 10)
        except WaitInputException:
            self.pc -= 1
            pass

    def is_stopped(self):
        return self.stopped
