Writeup: Intro to x86 Part I

Category: RE-50 points

CTF: CSAW 2018

Prompt:
	Newbs only!

	nc rev.chal.csaw.io 9003

	-Elyk

We are also given the files stage-1.asm, stage-2.bin, and Makefile, although this part will only involve stage-1.asm.

Stage-1.asm is a .asm file for compilation with nasm that walks through with notes on how to set up an os with assembly.

Connecting to the port reveals that it is asking a series of questions based on the assembly code.

Question 1 asks for the value in dx after the following command:  xor dh, dh
The answer is 0x00

Question 2 asks for the value of gs after the following command: mov gs, dx 
Looking back in the assembly we see that dx is set the following way:
	mov dx, 0xffff
     not dx
Since the not command will change the value of dx to 0x0000, the value in gs will be 0x00

Question 3 asks for the value of si as a 2 byte hex after the following line:
mov si, sp 
sp is set from the command
mov sp, cx
Previously in the code it is mentioned cx is already 0, so are answer is 0x0000

Question 4 asks for the value of ax after the following commands:
 mov al, 't'
 mov ah, 0x0e
Since the upper 8 bits of ax is ah and the lower 8 bits al, the value of ax will be 0x0e74

Question 5 asks for the value of ax after the following commands execute the first time:
cmp byte [si], 0
je .end
mov al, [si]
mov ah, 0x0e 
The upper 8 bits of ax will be ah, so 0x0e, and the lower 8 bits will be al which is equal to si.
Looking back we the following line:
mov si, ax
And back a couple more lines:
mov ax, .string_to_print
.string_to_print: db "acOS", 0x0a, 0x0d, "  by Elyk", 0x00
Therefore, al will be equal to the last byte in .string_to_print, which is "a" 0r 0x61
Are answer then is 0x0e61

flag{rev_up_y0ur_3ng1nes_reeeeeeeeeeeeecruit5!}

