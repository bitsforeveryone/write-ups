## IRS (PWN 100)

by droofe

When running the binary, I started by noticing that Mr. Trumps tax return was already filed. Hm? Lets go ahead and try to open it!

Password protected... okay awesome. After messing around and filing a few tax returns on my own, the program complained after I had made four additional returns, saying "blah blah blah, if this problem persists call us at 0xf7d35678". 

WOW! A free leak already. So, I decided to drop the binary into IDA and see what I was dealing with.

After some analysis, I saw that the binary started off and malloc'ed a space for Donald Trumps tax return and put the flag as the password. Awesome, goal: find the password to his tax return.

### Vulnerability
The vulnerability comes into play if you try to edit your tax return. After editing the tax return, it asks you to confirm, prompting you for [y/n], which is read in by none other than `gets`.
