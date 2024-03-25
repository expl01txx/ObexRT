from librt import VMM, CPU, Tools, objbuf, print
import marshal

memory = VMM(8192)
cpu = CPU(memory, reg_sz=5)

#BITS - CPU DATA SIZE 
BITS = 16
CPU_SZ = int(BITS/8)

#regisers
#0 - base
#1 - base
#2 - base
#3 - result
#4 - flag

#base opcodes
@cpu.opcode(0x01)
def vm_print(cpu: CPU):
    print(Tools.bytes_to_int(cpu.stack.pop(0)))

@cpu.opcode(0x02)
def vm_prints(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    buf = b""
    i = 0
    while cpu.memory.memory[addr+i] != 0:
        buf += Tools.int_to_bytes(cpu.memory.memory[addr+i], CPU_SZ)
        i += 1
    print(buf.decode())

@cpu.opcode(0x03)
def vm_input(cpu: CPU):
    buf = int(input())
    cpu.registers[3] = Tools.int_to_bytes(buf, CPU_SZ) 
    
@cpu.opcode(0x04)
def vm_inputs(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    buf = input()
    n = 0
    for i in buf:
        cpu.memory.memory[addr+n] = Tools.bytes_to_int(i.encode())
        n += 1
    cpu.memory.memory[addr+n] = 0x00

#mov reg, int
#0xC0 0x01 - 0x01 - number to push
@cpu.opcode(0xC0)
def mov_0(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[0] = val
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xC1)
def mov_1(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[1] = val
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xC2)
def mov_2(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[2] = val
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xC3)
def mov_3(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[3] = val
    cpu.ptr += CPU_SZ-1

#move reg,reg
#0xD0 0x01 - reg addr
@cpu.opcode(0xD0)
def movr_0(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[0] = cpu.registers[Tools.bytes_to_int(val)]
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xD1)
def movr_1(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[1] = cpu.registers[Tools.bytes_to_int(val)]
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xD2)
def movr_2(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[2] = cpu.registers[Tools.bytes_to_int(val)]
    cpu.ptr += CPU_SZ-1

@cpu.opcode(0xD3)
def movr_3(cpu:CPU):
    cpu.ptr += 1
    val = Tools.read_bytes(cpu, cpu.ptr, CPU_SZ)
    cpu.registers[3] = cpu.registers[Tools.bytes_to_int(val)]
    cpu.ptr += CPU_SZ-1

#reg to stack
@cpu.opcode(0xD4)
def movs_0(cpu:CPU):
    cpu.stack.append(cpu.registers[0])

@cpu.opcode(0xD5)
def movs_1(cpu:CPU):
    cpu.stack.append(cpu.registers[1])

@cpu.opcode(0xD6)
def movs_2(cpu:CPU):
    cpu.stack.append(cpu.registers[2])

@cpu.opcode(0xD7)
def movs_3(cpu:CPU):
    cpu.stack.append(cpu.registers[3])

@cpu.opcode(0x6E)
def push_num(cpu: CPU):
    cpu.ptr += 1
    cpu.stack.append(Tools.read_bytes(cpu, cpu.ptr, CPU_SZ))
    cpu.ptr += CPU_SZ-1

#math
#inc
@cpu.opcode(0x30)
def inc_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[0]) + 1, CPU_SZ)

@cpu.opcode(0x31)
def inc_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[1]) + 1, CPU_SZ)
    
@cpu.opcode(0x32)
def inc_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) + 1, CPU_SZ)

@cpu.opcode(0x33)
def inc_3(cpu: CPU):
    cpu.registers[3] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[3]) + 1, CPU_SZ)

#dec
@cpu.opcode(0x34)
def dec_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[0]) - 1, CPU_SZ)

@cpu.opcode(0x35)
def dec_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[1]) - 1, CPU_SZ)

@cpu.opcode(0x36)
def dec_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) - 1, CPU_SZ)

@cpu.opcode(0x37)
def dec_3(cpu: CPU):
    cpu.registers[3] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[3]) - 1, CPU_SZ)

#add
@cpu.opcode(0xE0)
def add_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[0]) + Tools.bytes_to_int(cpu.registers[1]), CPU_SZ)
    
@cpu.opcode(0xE1)
def add_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[1]) + Tools.bytes_to_int(cpu.registers[2]), CPU_SZ)

@cpu.opcode(0xE2)
def add_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) + Tools.bytes_to_int(cpu.registers[3]), CPU_SZ)

@cpu.opcode(0xE3)
def add_3(cpu: CPU):
    cpu.registers[3] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[3]) + Tools.bytes_to_int(cpu.registers[4]), CPU_SZ)

#sub
@cpu.opcode(0xE4)
def sub_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[0]) - Tools.bytes_to_int(cpu.registers[1]), CPU_SZ)

@cpu.opcode(0xE5)
def sub_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[1]) - Tools.bytes_to_int(cpu.registers[2]), CPU_SZ)

@cpu.opcode(0xE6)
def sub_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) - Tools.bytes_to_int(cpu.registers[3]), CPU_SZ)

@cpu.opcode(0xE7)
def sub_3(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) - Tools.bytes_to_int(cpu.registers[3]), CPU_SZ)

#mult
@cpu.opcode(0xE8)
def mul_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[0]) * Tools.bytes_to_int(cpu.registers[1]), CPU_SZ)

@cpu.opcode(0xE9)
def mul_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[1]) * Tools.bytes_to_int(cpu.registers[2]), CPU_SZ)

@cpu.opcode(0xEA)
def mul_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) * Tools.bytes_to_int(cpu.registers[3]), CPU_SZ)

@cpu.opcode(0xEB)
def mul_3(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(Tools.bytes_to_int(cpu.registers[2]) * Tools.bytes_to_int(cpu.registers[3]), CPU_SZ)

#div
@cpu.opcode(0xEC)
def div_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[0]) / Tools.bytes_to_int(cpu.registers[1])), CPU_SZ)

@cpu.opcode(0xED)
def div_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[1]) / Tools.bytes_to_int(cpu.registers[2])), CPU_SZ)

@cpu.opcode(0xEE)
def div_2(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[2]) / Tools.bytes_to_int(cpu.registers[3])), CPU_SZ)

@cpu.opcode(0xEF)
def div_3(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[2]) / Tools.bytes_to_int(cpu.registers[3])), CPU_SZ)

#xor
@cpu.opcode(0x40)
def xor_0(cpu: CPU):
    cpu.registers[0] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[0]) ^ Tools.bytes_to_int(cpu.registers[1])), CPU_SZ)

@cpu.opcode(0x41)
def xor_1(cpu: CPU):
    cpu.registers[1] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[1]) ^ Tools.bytes_to_int(cpu.registers[2])), CPU_SZ)

@cpu.opcode(0x42)
def xor_3(cpu: CPU):
    cpu.registers[2] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[2]) ^ Tools.bytes_to_int(cpu.registers[3])), CPU_SZ)

@cpu.opcode(0x7C)
def xor_num(cpu: CPU):
    cpu.ptr += 1
    num = (Tools.read_bytes(cpu, cpu.ptr, CPU_SZ))
    cpu.registers[3] = Tools.int_to_bytes(int(Tools.bytes_to_int(cpu.registers[3]) ^ Tools.bytes_to_int(num)), 1)
    cpu.ptr += CPU_SZ-1


#cmp
@cpu.opcode(0xD8)
def cmp_0(cpu:CPU):
    cpu.registers[4] = Tools.int_to_bytes(int(cpu.registers[0] == cpu.registers[1]), CPU_SZ)

@cpu.opcode(0xD9)
def cmp_1(cpu:CPU):
    cpu.registers[4] = Tools.int_to_bytes(int(cpu.registers[1] == cpu.registers[2]), CPU_SZ)

@cpu.opcode(0xDA)
def cmp_2(cpu:CPU):
    cpu.registers[4] = Tools.int_to_bytes(int(cpu.registers[2] == cpu.registers[3]), CPU_SZ)

@cpu.opcode(0xDB)
def strcmp(cpu: CPU):
    addr1 = Tools.bytes_to_int(cpu.stack.pop(0))
    addr2 = Tools.bytes_to_int(cpu.stack.pop(0))
    n = 0
    while cpu.memory.memory[addr1+n] != 0:
        a = cpu.memory.memory[addr1+n]
        b = cpu.memory.memory[addr2+n]
        if a != b:
            cpu.registers[4] = Tools.int_to_bytes(0, CPU_SZ)
            return
        n += 1
    cpu.registers[4] = Tools.int_to_bytes(1, CPU_SZ)

@cpu.opcode(0xF0)
def jmp(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    cpu.ptr = addr - 1

@cpu.opcode(0xF1)
def je(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    flag = Tools.bytes_to_int(cpu.registers[4])
    if flag:
        cpu.ptr = addr - 1

@cpu.opcode(0xF2)
def jne(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    flag = Tools.bytes_to_int(cpu.registers[4])
    if not flag:
        cpu.ptr = addr - 1

#flag to result
@cpu.opcode(0xDC)
def ftr(cpu:CPU):
    cpu.registers[3] = cpu.registers[4]

#memory operations
@cpu.opcode(0x1E)
def read_memory(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    cpu.registers[3] = Tools.int_to_bytes(cpu.memory.memory[addr+255], 1)

@cpu.opcode(0x1F)
def write_memory(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    value = Tools.bytes_to_int(cpu.stack.pop(0))
    cpu.memory.memory[addr+255] = value
@cpu.opcode(0x7E)
def retn(cpu: CPU):
    addr = Tools.bytes_to_int(cpu.stack.pop(0))
    size = Tools.bytes_to_int(cpu.stack.pop(0))
    bytes = bytearray(cpu.memory.memory[addr:addr+size])
    obj = marshal.loads(bytes)
    objbuf(obj)
    del obj

#end reg
@cpu.opcode(0xFF)
def stop(cpu: CPU):
    cpu.ptr = len(cpu.memory.memory)
