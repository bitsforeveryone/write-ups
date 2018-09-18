So for this challenge, we were given a server that feeds simple equations to us.</br>
This becomes a rather easy challenge to solve with the Sympy module. </br>
However, I didn't know about it until someone else showed it to me. </br>
So first, I tried to spin up my own parsing algorithm which actually worked fairly well until about the 25th equation.</br></br>
At that point, the server feeds us much more complicated equations with several nested parentheses which my measly algorithm wasn't equipped to handle.</br>
Queue the introduction to sympy which can convert strings of equations into sympy problems to be solved. </br></br>
See the attached script for my solution.
It isn't perfect as there are a couple instances in which the equation from the server doesn't solve correctly.

![Image of Flag](https://github.com/bitsforeveryone/write-ups/blob/master/CSAW_CTF_2018/Algebra/algebra_flag.JPG)
