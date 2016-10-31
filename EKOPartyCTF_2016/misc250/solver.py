from PIL import Image
from string import digits, uppercase
alphabet = digits + uppercase

def convert(imgfile):
    image = Image.open(imgfile)
    im = image.load()
    xstart = 15
    ystart = 20
    xoff = 7
    yoff = 20
    allpunches = []
    for x in range(xstart,image.size[0],xoff):
        punches = []
        for y in range(ystart,image.size[1],yoff):
            if im[x,y] == (255,255,255,255):
                punches.append((y-ystart)/yoff)
        allpunches.append(punches)
    return allpunches

def readpunch(p):
    if len(p) > 2:
        if p == [2,5,10]: return ','
        if p == [0,5,10]: return '.'
        if p == [2,9,10]: return '?'
        if p == [0,7,10]: return '('
        if p == [1,7,10]: return ')'
    if len(p) == 0:
        return ' '
    if len(p) == 1:
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

