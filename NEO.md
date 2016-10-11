# Neo Challenge 
	
The Neo challenge presented us with a webpage with a search box and two buttons. Inside the search box was a string of base-64 encoded 
text. The red button submitted the text in the search box and the blue button opened a pop up that displayed a quote. When text was 
submitted, one of two errors could be raised: an error that indicated the input string was not base-64 and an error indicating a problem
with the AES decryption. From context, we determined that the "Oracle" was a reference to a Padding Oracle Attack. 

The Padding Oracle Attack takes advantage of the knowledge of the PKCS7 padding scheme used in the AES implementation and of the XOR 
operation within AES. Since AES is most often implemented in Cipher Block Chaining (CBC) mode, a padding scheme must be implemented in 
order to round out the block size of the last block. PKCS7 [requires] that the block be padded with the hex digit of the bytes needed to
pad the block to the correct length. For example, if the block needs three bytes of padding, the appropriate padding according to PKCS7 
would be \0x03\0x03\0x03. Once the block is properly padded, it can be input into the AES algorithm. 

In AES CBC, blocks are XORed with the previous block in order to improve the encryption of the block. This step is performed after the 
actual AES encryption and is performed in order to change the encryption of the block and the other blocks in the chain. This operation 
does provide an opportunity to decipher the plaintext from the ciphertext blocks, provided we have a few conditions:

1. Knowledge of the padding scheme
2. A Padding Oracle, which returns TRUE if the padding is correct and FALSE if the padding is incorrect

For this challenge, we could assume the AES implementation as 16-byte CBC and the padding scheme as PKCS7, as both are the most common 
implementations of the AES cipher. The webpage itself was the Padding Oracle, providing an AES decryption error if the padding was 
incorrect and no error if it was correct. We now had the two requirements for the Padding Oracle Attack. 

This took a long time to figure out. I personally thought the POA targeted the base-64 encryption of the string. It took a lot of 
googling to figure this assumption out as false. @tratda figured this out before I did after I asked him for help with implementing the 
attack. In that time, I found several implementations of the POA made by other people, however I overlooked them since they targetted 
the PKCS7 padding. Additionally, I was unfamilliar with how HTTP requests functions and originally attempted to use the Selenium or 
Mechanize module of Python to automate the browser inputting strings into the webpage. @unif0rm and @squidward showed me how to 
implement HTTP GET requests to solve this problem, making the whole process much faster and more efficient.

The following Python code was our implemenation of the Padding Oracle Attack. One major improvement would be automation of the GET 
requests. This was scripted quickly and, due to limited time, was implemented before testing and refactoring. If we had taken the 
time to automate the main loop, the program could have been much faster and required less user input. Due to this high level of user 
integration, mistakes were common. Specifically, we lost track of what iteration of the algorithm we were on and had to repeat loops.
