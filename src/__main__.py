from runtime import *
import zipfile as gtz
import sys
target = cpu
ptr = gtz.ZipFile
bin = ".bin"
with ptr(sys.argv[0]) as z:
    src = z.read(f"ppa"[::-1] + bin)
obj = b""
for i in src:
    obj += (int(i) ^ 147).to_bytes(1, 'big')
target.load(obj)
target.create()
target.clean()