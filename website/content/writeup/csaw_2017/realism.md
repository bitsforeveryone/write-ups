---
title: "Realism"
date: 2017-09-27T18:03:59-04:00
type: "writeup"
tags:
  - "aw 2017"
  - "reverse engineering"
---

#### CSAW CTF 2017 - 300 points - Reverse Engineering 

<!--more-->

**Description - Did you know that x86 is really old? I found a really old Master Boot Record that I thought was quite interesting! At least, I think it's really old...**

**qemu-system-i386 -drive format=raw,file=main.bin**

**Files: [main.bin](https://github.com/bitsforeveryone/write-ups/raw/master/CSAW_CTF_2017/realism/main.bin)**

*Solved by Rebeca, r0d, l0ckbox, vimgod*

---

Result of file command in main.bin file:
main.bin: DOS/MBR boot sector

We used IDA to disassemble the program.

The most important part of assembly code is:

![main_loop()](https://github.com/bitsforeveryone/write-ups/raw/master/CSAW_CTF_2017/realism/mainloop.png)

On this part of the code the flag is analyzed.

The input is storage in the memory 1234h.
In the first part of the code, the number in position 1234h is compared with 67616c66h (the word "galf").
Note that numbers are stored in little endian and strings are stored in correct order. Therefore, the characters will appear in the opposite order when used as a number.

After removing the first string, the remaining part of the input is moved to the register xmm0, the string in the position 7C00h is moved to the register xmm5 and the input is shuffled.

Next, in 8 iterations we have the input recursively execute each operation:

------------------

1.	and with memory in address (si + 7D90h)

		is ff ff ff ff ff ff ff ff 00 ff ff ff ff ff ff ff 00 ff ff ff ff ff ff ff 

		si start in 8 and is decreased in each operation, so, in the first operation the and will be with the string: 00 ff ff ff ff ff ff ff ff 00 ff ff ff ff ff ff ff ff 
		and the last one will be with the string ff ff ff ff ff ff ff ff 00 ff ff ff ff ff ff ff ff 00

		The operation just erase the flag in one of the positions


[see memory](https://github.com/bitsforeveryone/write-ups/raw/master/CSAW_CTF_2017/realism/hexdump.png)

2. psadw with the string in xmm5 (see that the result of operation is storage at xmm5, so, that register is changed all operation)

[see psadbw function](http://x86.renejeschke.de/html/file_module_x86_id_253.html)

------------------

The result of the operation will moved to edx and compared with:

				8f 02 df 02
				5d 02 90 02
				21 02 09 02
				78 02 7b 02
				33 02 f9 02
				91 02 5e 02
				55 02 29 02
				70 02 11 02


We can better understand what happens in the shuffle operation using GDB:

	Passing the input flag{abcdefghijklm}, after shuffle, we have: ghijklm}defg{abc

We can calculate separately the first 8 characters and the last 8.

First, lets calculate the first part. We will call the characters a, b, c, d, e, f, g, h.

Each iteration gives us one equation with these variables:

------------------

	abs(6fh) + abs(b - 6eh) + abs(c - 74h) + abs(d - 65h) + abs(e - 78h) + abs(f - 74h) + abs(g - 2eh) + abs(h - 28h) = 2dfh
	abs(a - dfh) + abs(2) + c + d + e + f + g + h = 290h
	abs(a - 90h) + abs(b - 2)  d + e + f + g + h = 209h
	abs(a - 09h) + abs(b - 2) + c + e + f + g  + h = 27bh
	abs(a - 7bh) + abs(b - 2) + c + d + f + g  + h = 2f9h
	abs(a - f9h) + abs(b - 2) + c + d + e + g  + h = 25eh
	abs(a - 5eh) + abs(b - 1) + c + d + e + f + h = 229h
	abs(a - 29h) + abs(b - 2) + c + d + e + f + g = 211h

------------------

We know b is a legible character, so, it is greater than 2

We know that the last character is '}', so, we can substitute in the equation and eliminate the first equation (we will just need 6 equations)

After that, we have:

------------------

![mathematica()](https://github.com/bitsforeveryone/write-ups/raw/master/CSAW_CTF_2017/realism/mathematica.png)

------------------

The result obtained in Mathematica is:

109, 48, 100, 51, 95, 121, 48 = m0d3_y0}

Doing the same thing in the second part we obtain: 

alz_{4re

So, the flag is: {4realz_m0d3_y0}
