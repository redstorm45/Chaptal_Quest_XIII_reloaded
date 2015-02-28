"""

Stockage d'informations de débogguage

"""

import dessin
import option as opt

caseSel = [-1,-1]

#donne la position sur le niveau d'un click
def getCellAt(x,y):
    x,y = x-dessin.xOffset , y-dessin.yOffset
    x,y = x//opt.SPRITE_SIZE , y//opt.SPRITE_SIZE
    return x,y





