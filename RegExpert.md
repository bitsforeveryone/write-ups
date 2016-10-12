# Regexpert

This challenge presented us with 5 challenges to be solved using Ruby's [regular expressions](https://ruby-doc.org/core-2.2.0/Regexp.html "Ruby Regex Class"). The challenges were presented in the command line and we used `cat filename | nc IPADDR PORT` to quickly feed multiple regexes into the tester. The difficulty was primarily in using Ruby's limited regex class. While [PCRE](http://php.net/manual/en/book.pcre.php) has many features designed to make complex matching possible and has many well documented answers to complex problems, Ruby does not. Additionally, each regex had to be as short as possible, which required siginificant refactoring. Our general problem solving proces was to search for a PCRE regex that solved our problem and the port it to Ruby. We used extensive use of [Rubular](http://rubular.com/), an online Ruby regex testing platform, to test before we submitted our regexes to testing. 


### Problem 1
This challenge required us to match a SQL SELECT statement, case insensitively, with letters between each character of the statment. One sample match would be `SeXleCccdt`. To do this, we used this regex:
```ruby
(?i)s.*e.*l.*e.*c.*t
```
The `(?i)` denotes case insensitivity, so `s` represents both lower and upper case. In between each character are `.*` which means any character, repeated 0 or more times. These accounted for any text in between the characters of the command. 


### Problem 2
This challenge was to match any number of a's followed by the same number of b's. The flavor text noted that this is a classic case of context free grammer. Luckily, there are many PCRE regexex designed to solve this problem. In particular, [one answer on Stack Overflow](http://stackoverflow.com/questions/3644266/how-can-we-match-an-bn-with-java-regex) was very helpful. From this example, we were able to craft an equivalent Ruby regex:
```ruby
^(a\g<1>?b)$
```
This regex uses the `\g<>` function of Ruby's regex class, which allows for recursive matching of a group. The parenteses create a numbered group, group 1, which `\g<1>` references. The `?` makes the recursion match 0 or 1 times. The `^$` around the group limit the regex to match only if the whole line conforms to the patterm. To understand how this regex works, it is useful to think of the matching process as a loop. 
#### Loop 1
At this point, `\g<1>` is uninitialized and will not match. The regex will thus only match `ab`. Here, the `?` comes into play. Since `?` is greedy, it will try to match something and loop again.
#### Loop 2
In the second loop, `\g<1>` is initialized as the previous match of group 1. Since group 1 is effectively the whole regex, it will match `ab`. If we substitute this in, the regex now looks like: ```^(aa\g<1>?bb)$``` and will match `aabb`. This loop will continue until `/g<1>` can no longer be substituted into the regex and still match. At that point, the regex is evaluated
for a match. If the test string were 'aabbb', this final evaluation would come during the third loop.
#### Loop 3
Since the previous match for group 1 was `aabb`, the regex will substitute that in for `\g<1>`. Since `aaabbb` does not match, `aabbb`, the regex will go back to the previous confirmed match (`aabb`). Now, since the regex was surrounded by `^$`, the regex will not match since there is an extra character between `aabb` and the end of the line.


### Problem 3
We were asked to match prime length strings of x's, not including 0 or 1. Sample matches would be 3, 5, 9, 11:
```
xxx
xxxxx
xxxxxxxxx
xxxxxxxxxxx
```
The challenge is that prime numbers are prime; they have no factors and cannot be defined by a uniform set of rules. We once again searched for a PCRE regex that did this and implemented it in Ruby. We defined a negative matching group `(?! )` that matches any string that is the length of two prime numbers added together. More succinctly, `(?!(..+)\1+$|.?$)` matches and excludes any non-prime number. The `(..+)` group matches any two or greater character string. The `.` could be replaced by x's, but is not required. Then, `\1+` matches the first group, repeated any number of times. The result is a compound number. `|.?$` matches a 0 or 1 characters at the end of the string and since we included `^` at the beginning of the regex, matches an empty line or a line containing only one character. Finally, `xx` matches the first two x's in a string that is not matches by our non-prime-number-matching group. Thus, our final regex looks like this:
```ruby
^(?!(..+)\1+$|.?$)xx
```


### Problem 4
This problem asked us to match palindromes. 'QQ' and 'TAT' are defined as sample palindromes. Once again, `\g<>` is essentail to understanding and using this regex. We group the whole regex with `()`, defining it as group 1. We then create another group inside the main group with `(\w)`. `\w` matches any 'word' character, as defined by Ruby. Thus, `(\w)\2` matches the same character repeated twice. Between these groups we add the recursive group, `(\g<1>)`, matching group 1. Anything that group 1 matches will be subsituted into this group on the next loop. The last piece of regex is `|\w?` which matches 0 or 1 single characters, allowing for the regex to match the empty string and single characters. 
```ruby
((\w)(\g<1>)\2|\w?)$
```
If the OR group (`\w?`) is matched, it will be substituted into `\g<1>` on the second loop, allowing the regex to match a three letter palindrome. Recursively substituting into `\g<1>` allows the regex to match any length palindrome. If the OR group is not matched, the palindrome will be even-length. 


### Problem 5
Our final challenge was to match `a^nb^nc^n`. This is similar to the first challenge, but much more difficult. The core of this regex is `a+`, which matches any number of 'a' characters. We then define a positive lookahead before this core, `(?=(a\g<1>?b)c)`. This group uses `\g<1>?` to optionally recursively match `(a\g<1>?b)`. This is essentially the solution to problem 2, happily reused and recycled. The difference is that this only matches `a^nb^n`. The `c` at the end does not actually match, it is only there to confirm that there is a string of 'c's. To match the whole pattern, we define a second matching group, `(b\g<2>?c)`. Once again, this is essentially a copy of the solution to problem 2, but instead matches `b^nc^n`. Since the positive lookahead confirms that there are the same number of b's as there are a's, the second group matches the correct number of c's by the associative property. 
```ruby
^(?=(a\g<1>?b)c)a+(b\g<2>?c)$
```


