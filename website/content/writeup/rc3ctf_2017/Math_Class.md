---
title: "Math Class"
date: 2017-11-24T08:17:37-05:00
type: "writeup"
tags: [crypto, braille, rc3ctf]
---

#### RC3 CTF 2017 - 400 points - Crypto
<!--more-->
**Description - Part 4 of 5 in Classroom Crypto Series**

**Files: [Math_class.pdf](https://github.com/bitsforeveryone/write-ups/raw/master/rc3ctf_2017/crypto400/Math_class.pdf)**

*Solved by madeye*

---

#### Cross-posted at http://wclaymoody.com

Though we did not get the 400 points for this problem since I finally solved it 20 minutes after the end of the competition, I want to post a writeup since it was very cool.

This problem was worth 400 points and was the 4th in a series of classroom or school themed problems in the crypto category. English class, Science Class, History Class, Math Class and finally Report Card were the series of five challenges, worth 100,200,300,400 and 500 points. We did successfully solve Science and History for those 500 points.

![math_problems](http://wclaymoody.com/assets/images/rc3ctf2017/math_class.png)

## The realization

So when I first looked at this I noticed that the second math problem was incorrect. But I did not think much of it. Around mid day on Saturday of the CTF, the admin's posted some hints to many of the problems. The hint to this problems said _you must be BLIND not to see the pattern_. When I saw they hint, I went back to the problem and told my teammate "It's Braille!, I got this!"

Each summation problem is two digits wide and three digits tall. Just like a Braille character. The only question was which numbers were raised dots and which were flat dots. The numbers can be partioned many different ways, and my first instinct was even and odds. The text at the top of the PDF confirmed this. _you can't see the errors even though they are right in front of you._ My first hypothesis was even was a raised dot. Time to repurpose my braille library for this challenge.

Since my Braille Library uses lowercase `o` for raised and `.` for flat, I needed to convert the math expressions to this. Luckily the PDF was highlightable and I just copy and pasted the numbers into a text file and cleaned it up by removing the `+` and spacing them evenly. Below is those digits.

```
42 54 66 24 29 32 21
29 21 15 53 13 46 24
71 57 84 69 51 85 37

22 36 24 64 29 41 05
52 27 29 27 36 02 17
53 77 71 77 43 25 37

29 10 45 22 02 34 42
43 21 38 27 50 25 41
59 27 61 57 57 73 99

42 45 41 38 49 62 25
29 27 33 27 34 18 32
89 81 62 61 69 63 53

22 65 27 22 41 26 52
23 16 44 14 18 48 43
59 85 63 23 79 97 81
```

## The implementation

Saving those numbers above as `numbers.txt`, I was able to use the following python snippet to build my Braille representation of the math problems.

```python
# coding: utf-8
with open('numbers.txt') as f:
    data = f.read()

for c in "02468":
    data = data.replace(c, "o")

for c in "13579":
    data = data.replace(c, ".")
```
Which gave me the following:

```

oo .o oo oo o. .o o.
o. o. .. .. .. oo oo
.. .. oo o. .. o. ..

oo .o oo oo o. o. o.
.o o. o. o. .o oo ..
.. .. .. .. o. o. ..

o. .o o. oo oo .o oo
o. o. .o o. .o o. o.
.. o. o. .. .. .. ..

oo o. o. .o o. oo o.
o. o. .. o. .o .o .o
o. o. oo o. o. o. ..

oo o. o. oo o. oo .o
o. .o oo .o .o oo o.
.. o. o. o. .. .. o.
```
Now to see what is the Braille message. Using the `solve()` function from my Stevie N Ray code (below), I got what I thought was a flag in: `fixmathdifforabsofdifplusonefornegs`. Little did I know, that this was only the first of three messages I would need to solve to get the final answer.

```python

from string import lowercase

letterdots = [[1,],[1,2], [1,4], [1,4,5], [1,5], [1,2,4], [1,2,4,5], [1,2,5],
        [2,4], [2,4,5], [1,3], [1,2,3], [1,3,4], [1,3,4,5], [1,3,5],[1,2,3,4],
        [1,2,3,4,5], [1,2,3,5], [2,3,4], [2,3,4,5], [1,3,6], [1,2,3,6],
        [2,4,5,6], [1,3,4,6], [1,3,4,5,6], [1,3,5,6]]

def d2l(dotlist):
    if dotlist in letterdots:
        return lowercase[letterdots.index(dotlist)]
    else: return "&"

def d2i(dotlist):
    ind = (lowercase.index(d2l(dotlist)) + 1) % 10
    return digits[ind]

def solve(data):
    for linecount, line in enumerate(data.split('\n')):
        print linecount, line
        if len(line)==0: continue
        line = line.strip()
        if linecount == 0:
            letters = []
            for pairs in line.strip().split(' '):
                letters.append([])

        lettercount = len(letters)
        for i, pairs in enumerate(line.split(' ')):
            if len(pairs) == 0: continue
            for j, column in enumerate(pairs):
                if len(column) == 0: continue
                if j==0 and column == 'o':
                    letters[i].append(linecount+1 )
                if j==1 and column == 'o':
                    letters[i].append(linecount + 4)

        if linecount == 2:
            message = ''
            i = 0
            while i < len(letters):
                letter = sorted(letters[i])
                if letter == shift:
                    nextletter = sorted(letters[i+1])
                    message += d2l(nextletter).upper()
                    i += 2
                elif letter == numbersign:
                    nextletter = sorted(letters[i+1])
                    message += d2i(nextletter)
                    i += 2
                else:
                    message += d2l(letter)
                    i += 1
            return message
```
Like I said, I intially thought this was the flag. I tried submitting it as is, with spaces, with underscores, and finally with dashes. After confirming with a mod on IRC, I knew the phrase was a hint to going forward. Breaking down the message into individual words and thinking about the flow, I had this.

```
Fix math. Diff or abs of dif plus one for negs
```
## The correction

So most of the math problems looked to be incorrect. So this instruction was telling me to fix the math. Then to look the difference between the given answer and the correct result. If the difference was negative, take the absolute value of the difference and add one. This seems easy, but what to do with the result. My first guess was more Braille, replace the answer with the difference or absolute value plus one. This seemed like a stretch that such a message could have been created from only changing the last line. I was stuck on this for a while, adjusting my code to redo the Braille. But finally, I just stopped and looked at these new values. I had two difference sets of values depending if I subtracted the correction from the given values or the other way around. Here is the code I used to compute this two different sets of numbers.

```python
from string import lowercase
import re

patt_str = (("(\d{2}).?" * 7) + "\n") * 3

print patt_str

patt = re.compile(patt_str)

with open('numbers.txt') as f:
    data = f.read()

match = patt.findall(data)

option1 = []
option2 = []

for m in match:
    for i in range(7):
        a, b, c = [int(x) for x in (m[i], m[i+7], m[i+14])]
        d = c - (a+b)
        if d <= 0: d = abs(d) + 1
        option1.append(d)
        e = (a+b) - c
        if e <= 0: e = abs(e) + 1
        option2.append(e)
```

Those sets of numbers all are from the range of 1 to 26. 
```
[1, 19, 3, 9, 9, 7, 9, 22, 14, 18, 15, 23, 19, 15, 14, 5, 23, 8, 5, 14, 
    16, 18, 9, 13, 5, 15, 18, 5, 14, 4, 9, 14, 20, 23, 15]

[1, 18, 4, 8, 10, 8, 8, 21, 15, 19, 14, 22, 18, 16, 13, 4, 22, 9, 6, 15, 
    17, 19, 10, 12, 4, 14, 17, 4, 15, 5, 8, 13, 21, 24, 14]
```

I was stuck on this for a while cause like a computer scientist I was stuck on zero-indexed
arrays. Realizing that the value 0 was not possibly (thep problem says 0 is negative), I moved on.
Finally, using them as an index in to the alphabet with this code:

```python
print "".join(lowercase[o-1] for o in option1)
print "".join(lowercase[o-1] for o in option2)
```

results in the following two messages:

`asciigivnrowsonewhenprimeorendintwo`

`ardhjhhuosnvrpmdvifoqsjldnqdoehmuxn`

## One last step

The first message is obviously the next step. It tells us to create ASCII characters from the given rows. Using a 1 when the number is prime or ends in 2. Going back to the original data with the following code we can recover the flag.

```python
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
            37, 41, 43, 47, 53, 59, 61, 67,
            71, 73, 79, 83, 89, 97]

def bitstream(letter):
    bs = ""
    for b in letter:
        bs += "1" if (int(b) in primes or int(b)%10==2) else "0"
    return bs

flag = ""

for m in match:
    letters = [m[i:i+7] for i in range(0, len(m), 7)]
    for letter in letters:
        flag += chr(int("".join(bitstream(letter)),2))
print flag
```

That gives the message of:
`FLAGSUMARRAYMAN`

I never got to submit the flag, so don't know the exact flag, but that is definately the end.

## Full solve

The full code can be found here:

[Math Class(400)](http://wclaymoody.com/assets/ctffiles/rc3ctf2017/math_class_400_solve.py.txt)

#### Thanks to RC3 for a great challenge and fun CTF. Also, thanks to my teammates tr0gd0r, archang3l, phlint and goshawk

*Constant Vigilance*




