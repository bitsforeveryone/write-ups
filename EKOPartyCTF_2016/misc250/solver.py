
        return alphabet[p[0]-2]
    elif p[0] == 0:
        return alphabet[7+p[1]]
    elif p[0] == 1:
        return alphabet[16+p[1]]
    elif p[0] == 2:
        return alphabet[24+p[1]]


files = [
    "07d561df3da01f31590066f014652e995f7b76f1.png",
    "19756efa72339faa9c9b5fe1743c3abedbc5079d.png",
    "24c1e220c056210e6507c4c57079ffb99ffeb96c.png",
    "2d77fbd5eda9ed661a7834d8273815722fb97ccc.png",
    "4a95fea0f5e9af0af550b94fb960222e934ad09b.png",
    "85a749d44bcba42869f21fb58f9725a443066a4f.png",
    "89596be1f6463cb83abaecac7a375546069ecf0f.png",
    "93ec404ba9266f5d059a727a6460b2693fc4c440.png",
    "a034586b253b057c96da0b6707364853886b22b6.png",
    "a8a103961eccf8a991edfed1aaa39a8f9a3fe622.png",
    "a9aba85ebcb160a7b18ea22abfb9589bd3ce1914.png",
    "cdeea42d7f7216f93a9f1eb93b2723c70e693bea.png",
    "d3860afefe98f2408e24218a882aaf227d9287b9.png",
    "f7191b128c49ecfef0b27cd049550ae75249f86b.png"
]

for f in files:
    print ''.join([readpunch(p) for p in convert(f)])


