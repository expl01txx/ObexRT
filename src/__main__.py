from runtime import *
import zipfile as gtz
import sys

target = cpu
ptr = gtz.ZipFile
bin = ".bin"

with ptr(sys.argv[0]) as z:
    src = z.read(f"ppa"[::-1] + bin)

target.load(src)
target.create()
target.clean()