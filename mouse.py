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
    
    def __repr__(self):
        return "bouton["+str(self.pX)+","+str(self.pY)+","+str(self.pX+self.width)+","+str(self.pY+self.height)
    
    def inBouton(self,x,y):
        if self.pX<x and x<self.pX+self.width and self.pY<y and y<self.pY+self.height:
            return True
        return False

class TextEdit(Bouton):
    
    def __init__(self,position,size,name,text):
        super(TextEdit,self).__init__(position,size,name)
        self.text = text

boutons = {}
tEdits  = {}

def init(scrW,scrH):
    #création des boutons
    addBoutCenter("overlay" ,"menu"        ,int(scrW*0.5) , int(scrH*0.3)  , 150,75 )
    addBoutCenter("overlay" ,"sauvegarder" ,int(scrW*0.5) , int(scrH*0.5)  , 320,75 )
    addBoutCenter("overlay" ,"quitter"     ,int(scrW*0.5) , int(scrH*0.7)  , 190,75 )
    addBoutCenter("menu"    ,"nouveau"     ,int(scrW*0.5) , int(scrH*0.3)  , 200,75 )
    addBoutCenter("menu"    ,"charger"     ,int(scrW*0.5) , int(scrH*0.5)  , 200,75 )
    addBoutCenter("menu"    ,"quitter"     ,int(scrW*0.5) , int(scrH*0.7)  , 190,75 )
    addBoutCenter("overlayQ","oui"         ,int(scrW*0.4) , int(scrH*0.65) , 100,50 )
    addBoutCenter("overlayQ","non"         ,int(scrW*0.6) , int(scrH*0.65) , 100,50 )
    #création des etideurs de textes
    tEdits["nouveau"] = {}
    tEdits["

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







