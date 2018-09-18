This challenge was awful if only for the fact that there was one line within a 185000 line log file that contained the key and that it was a random hex string.
So the way to go about this one was fairly straightforward.
We unpacked the .deb package using:</br>
`dpkg-deb -R com.* whyos` </br></br>
inside is a directory structure that allows us to look at some of the config files within the app.</br>
Root.plist shows us a lot of information and references the Preferences app.
lets try hunting through the log file looking for preferences:</br>
`cat console.log | grep Preferences`</br>
Well that still leaves us with over 1700 possible lines so we have to find out a way to narrow that down even more.
The hint for the challenge was that it was a hex string so we can refine even further:</br>
`cat console.log | grep -e "\([A-Fa-f0-9]\)\+\{15,32\}" | grep Preferences`</br>
And Boom! we are left with just three lines left over. Copy and paste the one with an actual hex string and claim your 300 points!

![Flag](https://github.com/bitsforeveryone/write-ups/blob/master/CSAW_CTF_2018/whyOS/whyos_flag.png)
