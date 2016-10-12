#CSAW 2016

##Watchword (Forensics 250)

We downloaded the video file from the original challenge.

We are interested in seeing what metadata is in the file so we run `exiftool powpow.mp4`. Results are:

![exiftool powpow.mp4](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/exiftool.png)

That title field looks like Base64. Decoded it converts to: `http://steghide.sourceforge.net/`. This is probably a clue that we will have to use StegHide at some point.
Next we check to see if there is another file hidden inside of the MP4. 

![powpow.mp4 binwalk](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/binwalk_powpow.png)

Ok, so we can see that there is a png file inside of the video. So we extract that file using `foremost powpow.mp4`.
This is the image that comes out, some nice Neosporin flavored Oreos.

![oreos](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/oreo.png)

We run Stegsolve on the image and can see that there are signs of data being hidden in the blue0 plane (shown here) as well as red0 and green0. 

![stegsolve](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/stegsolve_oreo.PNG)

So we are pretty sure that there's data hidden in the image and that we need to use StegHide at some point. Unfortunately, StegHide does not work with PNG files so we cannot use it yet.
Instead we turn to the Python Stepic package. Using the script shown below and the command `python unhide.py > data` we are able to pull the data out of the PNG.

![unhide.py](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/unhide.png)

So we have pulled the data out of the Oreo picture. Running `file data` tells us that it is a JPEG and StegHide work with JPEGs.

![harambe](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/harambe.jpg)

Of course it's a Harambe meme, not exactly a rare reference in CSAW this year. By this point a hint had been released for the challenge that said `password = password`.
With this in mind we run `steghide extract -p password -sf harambe.jpg`.

StegHide informs us that if was able to extract the file `base64.txt`. When we open the file we see this:

`W^7?+dsk&3VRB_4W^-?2X=QYIEFgDfAYpQ4AZBT9VQg%9AZBu9Wh@|fWgua4Wgup0ZeeU}c_3kTVQXa}eE`

At first glance it looks like this could be Base64, but it also contains special characters. After some quick googling we stumble across Ascii85 encoding. Which Wikipedia tells us includes the character `0`-`9`, `A`-`Z`, `a`-`z`, and the characters ``!@#$%^&*()_+-;<=>?`{|}~``. This looks pretty promising. A little more research even tells us that we can decode this using Python3.

![base85decode](https://github.com/Fauer4Effect/write-ups/blob/master/screencaps/base85_decode.png)

And there's the flag `flag{We are fsociety, we are finally free, we are finally awake!}`
