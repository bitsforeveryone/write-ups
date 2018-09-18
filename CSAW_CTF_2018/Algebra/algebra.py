#!/bin/python2.7a
from sympy import *
from pwn import *

r = remote("misc.chal.csaw.io",9002)
r.recvuntil('**********************************************************************************\n')
i = 1
while(True):
    equation = r.recvline()
    if "flag" in equation:
        print(equation)
        break
    eq = equation.split("=")
    qu = sympify(eq[0])
    if(str(eq[1])<0):
        d = str(qu)+"+"+str(eq[1]).replace('-','')
    else:
        d = str(qu) + '-'+eq[1]
    c = solve(d,'X')
    print("{}: {}".format(i, c))
    try:
        ans = str(c[0])
    except Exception as e:
	print("Caught error on equation: " + equation)
	break
    if '/' in str(c):
        f = str(c).split('/')
	f[0] = f[0][1:]
	f[1] = f[1][:-1]
        ans = float(f[0])/float(f[1])
        ans = str(ans)
    r.send(str(ans)+"\n")
    r.recvuntil("YAAAAAY keep going\n")
    i += 1
#print("")
print("Done!")
