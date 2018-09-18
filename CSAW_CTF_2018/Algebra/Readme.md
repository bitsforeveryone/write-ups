So for this challenge, we were given a server that feeds simple equations to us.
This becomes a rather easy challenge to solve with the Sympy module. However, I didn't know about it until someone else showed it to me. So first I tried to spin up my own parsing algorithm which actually worked fairly well until about the 25th equation.
At that point, the server feeds us much more complicated equations with several nested parentheses which my measly algorithm wasn't equipped to handle.
Queue the introduction to sympy which can convert strings of equations into sympy problems to be solved. See the attached script for my solution. It isn't perfect as there are a couple instances in which the equation from the server doesn't solve correctly.
