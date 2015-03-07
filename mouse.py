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
        self.surf2 = None
    
    def __repr__(self):
        return "bouton["+str(self.pX)+","+str(self.pY)+","+str(self.pX+self.width)+","+str(self.pY+self.height)
    
    #change la surface et met à jour la position pour se centrer
    def setSurfCenter(self,surf):
        self.surf = surf
        
        xCenter = self.pX + self.width//2
        yCenter = self.pY + self.height//2
        
        newX = xCenter - surf.get_width()//2
        newY = yCenter - surf.get_height()//2
        
        self.pX,self.pY = newX,newY
        self.pos = newX,newY
        self.width,self.height = surf.get_width(),surf.get_height()
        self.size = self.width,self.height
    
    #change la surface et met à jour la position pour se centrer sur l'axe horizontal
    def setSurfCenterTop(self,surf):
        self.surf = surf
        
        xCenter = self.pX + self.width//2
        
        newX = xCenter - surf.get_width()//2
        
        self.pX = newX
        self.pos = newX,self.pY
        self.width = surf.get_width()
        self.size = self.width,self.height
    
    #changement d'angle haut gauche
    def setTopLeft(self,t,l):
        self.setTop(t)
        self.setLeft(l)
    
    #changement d'angle haut droite
    def setTopRight(self,t,r):
        self.setTop(t)
        self.setRight(r)
        print("top right to",r,t)
        
    #changement du bord gauche
    def setLeft(self,l):
        self.pX = l
        self.pos = l,self.pY
        
    #changement du bord droit
    def setRight(self,r):
        self.pX = r - self.width
        self.pos = self.pX,self.pY
    
    #changement du bord haut
    def setTop(self,t):
        self.pY = t
        self.pos = self.pX,t
        
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
    addBoutCenter("menu"    ,"nouveau"     ,int(scrW*0.5) , int(scrH*0.3)  , 260,75 )
    addBoutCenter("menu"    ,"charger"     ,int(scrW*0.5) , int(scrH*0.45) , 260,75 )
    addBoutCenter("menu"    ,"option"      ,int(scrW*0.5) , int(scrH*0.60) , 260,75 )
    addBoutCenter("menu"    ,"quitter"     ,int(scrW*0.5) , int(scrH*0.75) , 230,75 )
    addBoutCenter("overlayV","oui"         ,int(scrW*0.4) , int(scrH*0.65) , 100,50 )
    addBoutCenter("overlayV","non"         ,int(scrW*0.6) , int(scrH*0.65) , 100,50 )
    addBoutCenter("nouveau" ,"PTSI"        ,int(scrW*0.3) , int(scrH*0.25) , 260,75 )
    addBoutCenter("nouveau" ,"MPSI"        ,int(scrW*0.5) , int(scrH*0.25) , 260,75 )
    addBoutCenter("nouveau" ,"PCSI"        ,int(scrW*0.7) , int(scrH*0.25) , 230,75 )
    addBoutCenter("nouveau" ,"commencer"   ,int(scrW*0.5) , int(scrH*0.9)  , 260,75 )
    #création des etideurs de textes
    tEdits["nouveau"] = {}

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







