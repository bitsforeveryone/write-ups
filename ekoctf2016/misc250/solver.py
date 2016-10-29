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
        allpunches.append(holes(punches))
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


