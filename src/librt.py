class VMM:
    def __init__(self, size):
        self.memory = [0] * size
        self.sz = size

    def alloc(self, bytecode):
        for i in range(len(bytecode)):
            self.memory[i] = bytecode[i]
    
    def write(self, ptr, value):
        self.memory[ptr] = value
    
    def read(self, ptr):
        return self.memory[ptr]
    
    def read_bytes(self, start, end):
        return self.memory[start:end]
    
    def reset(self):
        self.memory = [0] * self.sz
    

class CPU:
    def __init__(self, memory: VMM, reg_sz: int = 4):
        self.memory = memory
        self.opcodes = {}
        self.ptr = 0
        self.registers = [b'\x00']*reg_sz
        self.reg_sz = reg_sz
        self.stack = []

    def opcode(self,value):
        def decorator(func):
            self.opcodes[value] = func
        return decorator
    
    def load(self, program):
        self.memory.alloc(program)
    
    def create(self):
        while self.ptr<len(self.memory.memory):
            opcode = self.memory.read(self.ptr)
            if opcode in self.opcodes:
                try:
                    self.opcodes[opcode](self)
                except Exception as e:
                    print(f"[LibRT] exception on {self.ptr} , {e}")
            self.ptr += 1
    
    def clean(self):
        self.registers = [b'\x00']*self.reg_sz
        self.stack = []
        self.ptr = 0
        self.memory.reset()

class Tools:
    def bytes_to_int(byte):
        return int.from_bytes(byte, byteorder='big')
    
    def int_to_bytes(number: int, size):
        return int(number).to_bytes(size, 'big')
        
    def read_bytes(cpu: CPU, index, size):
        return bytearray(cpu.memory.read_bytes(index, index+size))

objbuf = exec