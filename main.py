import marshal
import zipfile
import os, py_compile, shutil

print("Obex v0.2")

PYTHON = "312"

def build_stub(key: int = 33):
    src = open("src.py", 'r').read()
    src = compile(src, "obex", "exec")
    src = marshal.dumps(src)

    sz = len(src).to_bytes(length=2, byteorder='big')

    #generate stub
    loader = bytearray([
        0xC0, #mov a, len(src)
    ])

    for i in sz:
        loader.append(i)

    #decrypt
    loader += bytearray([
        0xC1, 0x00, 0x00, #mov b, 0
        0xD5, #push b
        0x1E, #read memory on b
        0x7C, 0x00, key, #xor d, 33
        0xD5, #push b
        0xD7, #push d
        0x1F, #write memory +255 (read vm code)
        0xD3, 0x00, 0x00, #mov d, a
        0xD2, 0x00, 0x01, #mov c, b
        0x31, #inc b
        0xDA, #cmp c,d
        0x6E, 0x00, 6, #push ?
        0xF2, #jne 
        0x6E, 0x00, 0xFF, #push 255
        0xD4, #push a
        0x7E, 0xFF #pycall
    ])

    #loader.append(0x7E)
    loader += bytearray([0x7E, 0xFF])

    for i in range(len(src)*2):
        loader.append(0x00)

    for i in range(len(src)):
        loader[i+255] = (src[i]^key)
    return loader

print("Building sources...")

#build sources
for i in os.listdir("src"):
    if os.path.isfile(f"src/{i}"):
        target = i.removesuffix(".py")
        py_compile.compile("src/" + i)
        shutil.copy(f"src/__pycache__/{target}.cpython-{PYTHON}.pyc", f"stub/{target}.pyc")

print("Packing files...")
with zipfile.ZipFile("output/app_obex.pyz", 'w') as z:
    print("Virtualize sources...")
    z.writestr("app.bin", build_stub())
    print("Packing runtime...")
    for file in os.listdir("stub"):
        tmp = open("stub/" + file, 'rb').read()
        z.writestr(file, tmp)
    
print("Done!")