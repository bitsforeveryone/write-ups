# Neo Challenge 
	
The Neo challenge presented us with a webpage with a search box and two buttons. Inside the search box was a string of base-64 encoded text. The red button submitted the text in the search box and the blue button opened a pop up that displayed a quote. When text was submitted, one of two errors could be raised: an error that indicated the input string was not base-64 and an error indicating a problem with the AES decryption. From context, we determined that the "Oracle" was a reference to a Padding Oracle Attack. 

The Padding Oracle Attack takes advantage of the knowledge of the PKCS7 padding scheme used in the AES implementation and of the XOR operation within AES. Since AES is most often implemented in Cipher Block Chaining (CBC) mode, a padding scheme must be implemented in order to round out the block size of the last block. PKCS7 [requires] that the block be padded with the hex digit of the bytes needed to pad the block to the correct length. For example, if the block needs three bytes of padding, the appropriate padding according to PKCS7 would be \0x03\0x03\0x03. Once the block is properly padded, it can be input into the AES algorithm. 

In AES CBC, blocks are XORed with the previous block in order to improve the encryption of the block. This step is performed after the actual AES encryption and is performed in order to change the encryption of the block and the other blocks in the chain. This operation does provide an opportunity to decipher the plaintext from the ciphertext blocks, provided we have a few conditions:

1. Knowledge of the padding scheme
2. A Padding Oracle, which returns TRUE if the padding is correct and FALSE if the padding is incorrect

For this challenge, we could assume the AES implementation as 16-byte CBC and the padding scheme as PKCS7, as both are the most common implementations of the AES cipher. The webpage itself was the Padding Oracle, providing an AES decryption error if the padding was incorrect and no error if it was correct. We now had the two requirements for the Padding Oracle Attack. 

Our code used HTTP requests to GET new ciphertext, send back our ciphertext, and check what errors were being returned. Given enough time to run, eventually our code would have returned the flag.
