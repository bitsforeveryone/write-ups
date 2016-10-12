def hashPPC(seedVal, inputVal):
    horribilized = horrible(seedVal)
    res = horribilized ^ ord(inputVal)
    return res

def horrible(num):
    binum = str(bin(num))[2:]
    res = '00000000000000000000'+pad(binum)[20:]
    return int(res,2)

def pad(strNum):
    res = strNum
    while(len(res) < 32):
        res = '0'+res
    return res

def getAnswer(index):
    alphanum = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'
    rando = [205757590,998377520,1430092073,2047191058,1959523426,1763442792,1345239717,793358328,658433361,1016199565,1294268491,1322964720,2137247737,1405325116,642114049,1392987601,988381069,740379636,1285459211,1904974096,943865137,605738913,1559909246,926847391,1442292648,425531748,1307965978,1673880289,860617914,1317232,831869049,1066375504,999694753,114477475,966082914]
    check = [3326,2137,2397,2161,1037,6,2782,4008,1377,2522,2168,1666,4009,3935,606,3504,4031,3014,3384,2397,3337,2029,775,448,921,2390,2629,658,3210,2351,74,2404,404,2522,287]
    for i in alphanum:
        test = hashPPC(rando[index],i)
        print("Test character: "+i+"          ")
        print("HashPPC Result: "+str(test)+"\n")
        if(test == check[index]):
            print("Hit: "+i)
            return i
    print("You lose!... Good day, sir!")
    return 'nope'

def getAnswers():
    res = ''
    for i in range(0,35):
        retChar = getAnswer(i)
        if(retChar == 'nope'):
            print("Game over...")
            exit(0)
        else:
            res += retChar
    print(res)
    return

getAnswers()

