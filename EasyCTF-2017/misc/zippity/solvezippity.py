#####################################
#  Zippity Write-up - EasyCTF 2017  #
#####################################

# Import pwntools cause why not
from pwn import *

# File found online after googling for 2010 census data. 
file = open('Gaz_zcta_national.txt','r')

# Initializing dictionaries for fast lookups. We are trying 
# to beat the program in under 30 seconds.
lat = {}
lon = {}
wat = {}
land = {}

# We loop through the file we open. The data is separated by tabs
# and has a lot of white space and special characters. We just .strip() 
# these away. We store them in their respective dictionaries with the 
# (key, value) pairs being (zipcode, data).
for x in file:
	l = x.split('\t')
	# print (l[0],l[7].strip(),l[8].strip())
	lat[int(l[0])] = l[7].strip()
	lon[int(l[0])] = l[8].strip()
	wat[int(l[0])] = l[4].strip()
	land[int(l[0])] = l[3].strip()

# Always remember to close your files kids.
file.close()

# Remote server we are attacking.
p = remote("c1.easyctf.com",12483)

# Bypass glitchy recv at the beggining due to new lines.
p.recvuntil("1 / 50")

# Instead of making some crazy specific for loop, it's easiest to just
# throw your recv/sendline scripting into an endless while loop and ctrl-C 
# out of it when you need to.
while True:
	prompt = p.recv()
	# parse the line for the zipcode we are working with for this part.
	i = int(prompt[-7:-2].strip())
	print prompt
	# return the data from the appropriate dictionary.
	if "water" in prompt:
		p.sendline(str(wat[i]))
	elif "lat" in prompt:
		p.sendline(str(lat[i]))
	elif "long" in prompt:
		p.sendline(str(lon[i]))
	elif "land" in prompt:
		p.sendline(str(land[i]))



