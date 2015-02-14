"""

Fichier qui gère les différents évenements de souris
et les positions de boutons

"""



class Bouton:
    
    def __init__(self,position,size,name):
        self.name = name
        self.pos = position
        self.pX,self.pY = position
        self.size = size
        self.width,self.height = size
        self.surf = None
    
    def inBouton(self,x,y):
        if self.pY<x<self.pX+self.width and self.pY<y<self.pY+self.height:
            return True
        return False

boutons = {}

def init(scrW,scrH):
    #création des boutons
    addBoutCenter("overlay","menu"        ,int(scrW*0.5) , int(scrH*0.3) , 150,75 )
    addBoutCenter("overlay","sauvegarder" ,int(scrW*0.5) , int(scrH*0.5) , 320,75 )
    addBoutCenter("overlay","quitter"     ,int(scrW*0.5) , int(scrH*0.7) , 190,75 )

#ajoute un bouton, (x,y) en haut à gauche
def addBout(win,name,x,y,w,h):
    try:
        0 in boutons[win]
    except:
        boutons[win] = {}
    boutons[win][name] = Bouton( (x,y) , (w,h) ,name )
    return boutons[win][name]
    
#ajoute un bouton, (x,y) au centre du bouton
def addBoutCenter(win,name,x,y,w,h):
    return addBoutCenterTop(win,name, x,y-h//2 , w,h )
    
#ajoute un bouton, (x,y) au milieu en haut
def addBoutCenterTop(win,name,x,y,w,h):
    return addBout(win,name, x-w//2,y , w,h )

#donne le bouton d'un click
def getBoutonAt(win,x,y):
    for b in boutons[win].keys():
        if boutons[win][b].inBouton(x,y):
            return boutons[win][b]
    return None







