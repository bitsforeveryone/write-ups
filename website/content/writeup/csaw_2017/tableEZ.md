---
title: "tableEZ"
date: 2017-09-19T14:14:20-04:00
type: "writeup"
tags:
  - "csaw 2017"
  - "reverse engineering"
  - "crackme"
---

#### CSAW CTF 2017 - 100 points - Reverse Engineering 
<!--more-->
**Description - Bobby was talking about tables a bunch, so I made some table stuff. I think this is what he was talking about...**  
**Files: [tablez](https://github.com/r0d/Write_Ups/blob/master/CSAW%20CTF%202017/tablEZ/tablez)**

*Solved by r0d & stonepresto* 

---

tablEZ is a fairly straight-forward crackme style challenge.  

![tablez main()](https://github.com/r0d/Write_Ups/blob/master/CSAW%20CTF%202017/tablEZ/maincheckloop.png)


Booting up IDA, we see a prompt asking for the flag and an fgets whcih recieves the flag. The length of the input is then stored and we enter a loop that iterates through our input string byte by byte and calls get_tbl_entry on each byte. It then overwrites the byte it passed to get_tbl_entry with the return value. So it seems like this function is taking our input and translating it with this function. Looking a little farther, we see that our translated input is compared to a hex string that was passed earlier in the function ([rbp + s2]). So, the key here is to figure out how get_tbl_entry is modifying our input and work backwards from the hex string to recover our flag.   

get_tbl_entry turns out to be a fairly small function. We see a loop, and looking at the comparison we see it will execute at most 256 time while looking for a match to our input in the data section at trans_table. Once a match is found, it uses that index to pull out a new value and returns the new value.   

![tabelz get_tbl_entry()](https://github.com/r0d/Write_Ups/blob/master/CSAW%20CTF%202017/tablEZ/gettblentry.png)


Looking at trans_table, we see a large array starting with \x01 to and ending at \xFF and a corresponding (random) value associated with each entry. So I think it's safe to assume here that this function is simply taking our input, looking it up in this table, and translating it to a random hex value. Since we already have the hex values it is being compared too, we can simply look those up and find the corresponding plaintext that produces them, which will yield the flag.  
  
![tabelz Data:trans_table](https://github.com/r0d/Write_Ups/blob/master/CSAW%20CTF%202017/tablEZ/transtable.png)

In our case, we wrote an IDApython script to perform a reverse lookup, which resulted in the flag.   

Script:   
```python  
from struct import pack  
loc1 = 0x8BA  
loc2 = 0x8C4  
loc3 = 0x8DC  
loc4 = 0x8E6  
loc5 = 0x8FE  
loc6 = 0x908  
  
str1 = pack("<Q",GetOperandValue(loc1,1))  
str2 = pack("<Q",GetOperandValue(loc2,1))  
str3 = pack("<Q",GetOperandValue(loc3,1))  
str4 = pack("<Q",GetOperandValue(loc4,1))  
str5 = pack("<Q",GetOperandValue(loc5,1))  
str6 = pack("<Q",GetOperandValue(loc6,1))  
s = (str1 + str2 + str3 + str4 + str5 + str6)  
flag = ""  
for char in s:  
    for i in range(1,512,2):  
        b = Byte(LocByName("trans_tbl")+i)  
        if(ord(char) == b):  
            flag += ("%c" %(Byte(LocByName("trans_tbl")+i-1)))  
print(flag)  
```

Output: 

flag{t4ble_l00kups_ar3_b3tter_f0r_m3}
