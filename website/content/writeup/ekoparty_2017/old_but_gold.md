---
title: "Old_but_gold"
date: 2016-10-30T17:11:41-04:00
type: "writeup"
tags: [misc, ekoparty, legacy]
---

#### EKOParty 2016 CTF - 250 points - Misc
<!--more-->
**Description - These QR codes look weird**  
**Files: [Zip Files](https://github.com/bitsforeveryone/write-ups/raw/master/EKOPartyCTF_2016/misc250/misc250_100ff979353dd452.zip)**


*Solved by madeye*

My teammates immediately pointed this challenge out to me since they knew I loved punch cards. A few months prior, I had written a challenge for our internal try-out CTF in which they were given a base64 encoced ascii art image of an IBM-29 punch card with a message encoded for them. It was a favorite for the students. It took me about 20 minutes to repurpose my code to solve this challenge. 

When extracted, the zip file contains 14 PNG files that are images of IBM-29 punch cards. The images are consistently the same size and with equally spaced punches. Iterating over each column then each row, you can read the punch if the pixel in the top left corner is white. The top row, left most column starts at pixel column 15 and pixel row 20. Each punch location is then spaced 20 pixel vertically and 7 pixels horizontally.

Using PIL, I was able to read each image to find the punches on each row. The following code returns a list of columns of punches, where each column is a list of the rows that are punched.

```python
def convert(imgfile):
    image = Image.open(imgfile)
    im = image.load()
    xstart = 15
    ystart = 20
    xoff = 7
    yoff = 20
    allpunches = []
    for x in range(xstart,image.size[0],xoff):
        punches = []
        for y in range(ystart,image.size[1],yoff):
            if im[x,y] == (255,255,255,255):
                punches.append((y-ystart)/yoff)
        allpunches.append(holes(punches))
    return allpunches

```
The list of punches now needs to be converted to a string of characters. Understanding the layout of the punches as shown [here](http://www.columbia.edu/cu/computinghistory/029-card.jpg), we can script this up as follows. *note: not all puncutations are converted, just the ones observed on this set of cards*.

```python
def readpunch(p):
    if len(p) > 2:
        if p == [2,5,10]: return ','
        if p == [0,5,10]: return '.'
        if p == [2,9,10]: return '?'
        if p == [0,7,10]: return '('
        if p == [1,7,10]: return ')'
    if len(p) == 0:
        return ' '
    if len(p) == 1:
        return alphabet[p[0]-2]
    elif p[0] == 0:
        return alphabet[7+p[1]]
    elif p[0] == 1:
        return alphabet[16+p[1]]
    elif p[0] == 2:
        return alphabet[24+p[1]]
```

Now we just need to iterate over all 14 cards provided in the zip file to get the text for each card.
```python
for f in files:
    print ''.join([readpunch(p) for p in convert(f)])
```

The cards in alphabetical order by file name produces the following text. Reading through each line to determine the follow of the story is needed. I did not see any logical way to automate this. I have indicated the final line number after each row of text

~~~
OF TIME PUNCHING THOSE NARDS, CAN YOU IMAGINE WHAT COULD      [8]
THE BUG, BUT THOSE WER3 THE OLD DAYS. CAN YOU FIND THE FLAG   [13]
USING THIS OLD TECHNOLOGY? GOOD LUCK, YOU WILL NEED IT)       [14]
IT WAS THE SIXTIES, HE WAS TRYKNG TO FIGURE OUT HOW TO        [2]
MANUALS TRY1NG TO LEARN HOW TO PROGRAM AND SPEND A LOT        [7]
HAPPEN IF YOU FAKE A SMALL MISTAKE IN ON OF THOSE PUNCHED     [9]
USE THOSE PONCHED CARDS, HE LIKES TO PROGRAM IN FORTRAN       [3]
ERROR DUE TO A SMALL AND ALMOST INSIGNIFICANT MIST4KE BUT     [11]
AND COBOL, B(T EVEN AFTER ALL THOSE YEARS HE DOESNT KNOW      [4]
CARDS? AFTER THOSE HOURS WAITING ROR A RESULT, THEN IT SAYS   [10]
IN THOSE DAYS YOUR ONLY OPTION W4S READ LARGE BOOKS AND       [6]
HOW TO PROPERLY MRITE SECURE CODE IN THOSE LANGUAGES          [5]
THAT WILL TAKE MORE TIME TO MEBUG AND FIGURE OUT WHERE WAS    [12]
ONCE UPON A TEME, THERE WAS A YOUNG HACKER CALLED MJ          [1]
~~~

Following along with the story, it talks about mistakes. There are also some mistakes in the story. After double checking that the solver was correct, I noticed the first three typos were E, K, O which matches the flag pattern. In order, the flag properly describes the system that used the punchcards. *note: some writeups show the flag using the parenthesis, but since there was no symbol for curly braces I submited the flag with the curlies and got the points*

```
EKO{M41NFR4M3}
```

Entire solve script can be found [here](https://raw.githubusercontent.com/bitsforeveryone/write-ups/master/EKOPartyCTF_2016/misc250/solver.py)

**Constant Vigilance!!**
