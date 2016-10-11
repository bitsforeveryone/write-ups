# Regexpert

This challenge presented us with 5 challenges to be solved using Ruby's [regular expressions](https://ruby-doc.org/core-2.2.0/Regexp.html "Ruby Regex Class"). 
The challenges were presented in the command line and we used `cat filename | nc IPADDR PORT` to quickly feed multiple regexes into the 
tester. The difficulty was primarily in using Ruby's limited regex class. While PCRE []() has many features designed to make complex 
matching possible, Ruby does not. Additionally, each regex had to be as short as possible, which required siginificant refactoring.

### Problem 1
This challenge required us to match a SQL SELECT statement, case insensitively, with letters between each character of the statment. To
do this, we used this regex:
```ruby
(?i)s.*e.*l.*e.*c.*t
```
The `(?i)` denotes case insensitivity, so `s` represents both lower and upper case. In between each character are `.*` which means any 
character, repeated 0 or more times. These accounted for any text in between the characters of the command. 

### Problem 2
This challenge was to match any number of 'a's followed by the same number of 'b's. The flavor text noted that this is a classic case of 
[context free grammer](). Luckily, there are many PCRE regexex designed to solve this problem. In particular, [one answer on Stack 
Overflow]() was very helpful. From this example, we were able to craft an equivalent Ruby regex:
```ruby
^(a\g<1>?b)$
```
This regex uses the `\g<>` function of Ruby's regex class, which allows for recursive matching of a group. The parenteses create a 
numbered group, group 1, which `\g<1>` references. The `?` makes the recursion match 0 or 1 times. The `^$` around the group limit the 
regex to match only if the whole line conforms to the patterm. To understand how this regex works, it is useful to think of the matching 
process as a loop. 
#### Loop 1
At this point, `\g<1>` is uninitialized and will not match. The regex will thus only match `ab`. Here, the `?` comes into play. Since `?` 
is greedy, it will try to match something and loop again.
#### Loop 2
In the second loop, `\g<1>` is initialized as the previous match of group 1. Since group 1 is effectively the whole regex, it will match 
`ab`. If we substitute this in, the regex now looks like: ```^(aa\g<1>?bb)$``` and will match `aabb`. This loop will continue until `/g<1>` can no longer be substituted into the regex and still match. At that point, the regex is evaluated
for a match. If the test string were 'aabbb', this final evaluation would come during the third loop.
#### Loop 3
Since the previous match for group 1 was `aabb`, the regex will substitute that in for `\g<1>`. Since `aaabbb` does not match `aabbb`, 
the regex will go back to the previous confirmed match (`aabb'). Now, since the regex was surrounded by `^$`, the regex will not match
since there is an extra character between `aabb` and the end of the line.

### Problem 3
We were asked to match `x^n^2`, where `n` is a positive integer. So sample matches would be 1, 4, 9, 16:
```
x
xxxx
xxxxxxxxx
xxxxxxxxxxxxxxxx
```

```ruby
^(?!(..+)\1+$|.?$)xx
```

### Problem 4
```ruby
((\w)(\g<1>)\2|\w?)$
```

### Problem 5
```ruby
^(?=(a\g<1>?b)c)a+(b\g<2>?c)$
```


