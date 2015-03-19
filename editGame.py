"""

Fichier de gestion de l'édition des maps

"""
import dessin
import pygame
import map
import ennemi
import option
import keybinding
import option as opt

#changements sauvegardés
changesSaved = False

#liste des ennemis
ennemiList = []

#région en édition
regionEditee = None

#nom du curseur en utilisation
# sprite (vert) : edition du fond
# item (rouge)  : edition des items
# event (bleu)  : edition des différents évenements
cursor = "sprite"

#cases selectionnées
caseSel = []

#initialisation du jeu
def init():
    global ennemiList,regionEditee
    
    regionEditee = map.theMap.regionList[option.editRegion]
    
    #création des ennemis sur la map
    for e in regionEditee.ennemiBaseList:
        type,posX,posY = e
        regionEditee.ennemiList.append( ennemi.typesEnnemis[type].copyAt( (regionEditee.name,posX,posY) ) )
    
    #initialisation de la liste d'ennemi
    ennemiList = regionEditee.ennemiList[:]

#dessin de la scène
def draw(fenetre):
    global player
    
    #dessin de la région
    regionAffichee = regionEditee.name
    dessin.drawRegion(fenetre,regionAffichee)
    
    for e in ennemiList:
        dessin.drawPlayer(fenetre,e)
    
    #dessin de confirmation de sauvegarde
    if changesSaved:
        pygame.draw.rect( fenetre, (255,255,255),(0,0,64,64) )
    
    #dessin du cadre du niveau
    xEcran = regionEditee.readOffset[0] * opt.SPRITE_SIZE  + dessin.xOffset
    yEcran = regionEditee.readOffset[1] * opt.SPRITE_SIZE  + dessin.yOffset
    w,h = regionEditee.width * opt.SPRITE_SIZE,regionEditee.height * opt.SPRITE_SIZE
    pygame.draw.lines( fenetre , (255,255,255) , True, [(xEcran   ,yEcran   ),
                                                        (xEcran+w ,yEcran   ),
                                                        (xEcran+w ,yEcran+h ),
                                                        (xEcran   ,yEcran+h )] )
    #dessin du curseur
    xMouse,yMouse = pygame.mouse.get_pos()
    if cursor == "sprite":
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-10,yMouse-2,20,4) )
        
        for xsel,ysel in caseSel:
            xEcran = xsel * opt.SPRITE_SIZE  + dessin.xOffset
            yEcran = ysel * opt.SPRITE_SIZE  + dessin.yOffset
            pygame.draw.lines( fenetre , (255,255,255) , True, [(xEcran   ,yEcran   ),
                                                                (xEcran+64,yEcran   ),
                                                                (xEcran+64,yEcran+64),
                                                                (xEcran   ,yEcran+64)] )
    elif cursor == "item":
        pygame.draw.rect( fenetre , (255,0,0) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (255,0,0) ,(xMouse-10,yMouse-2,20,4) )
    elif cursor == "event":
        pygame.draw.rect( fenetre , (0,0,255) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (0,0,255) ,(xMouse-10,yMouse-2,20,4) )
        
#touches de mouvement
def actionKeys(listPressed):
    global player,ennemiList
    
    #mouvement du joueur
    if keybinding.isKeyActive( "LEFT" , listPressed ):
        dessin.xOffset += 16
    if keybinding.isKeyActive( "DOWN" , listPressed ):
        dessin.yOffset -= 16
    if keybinding.isKeyActive( "RIGHT" , listPressed ):
        dessin.xOffset -= 16
    if keybinding.isKeyActive( "UP" , listPressed ):
        dessin.yOffset += 16

#clique droite à un endroit: change le mode d'édition
def clickR(x,y):
    global cursor
    if cursor == "sprite":
        cursor = "item"
    elif cursor == "item":
        cursor = "event"
    elif cursor == "event":
        cursor = "sprite"
        
#clique gauche à un endroit: selectionne la case
def clickL(x,y):
    #coordonnées de la case
    xC,yC = x-dessin.xOffset , y-dessin.yOffset
    xC,yC = xC//opt.SPRITE_SIZE , yC//opt.SPRITE_SIZE
    
    if cursor == "sprite":
        if (xC,yC) in caseSel:
            caseSel.remove( (xC,yC) )
        else:
            currentS = regionEditee.at(xC,yC)
            canAdd = True
            for xsel,ysel in caseSel:
                if regionEditee.at(xsel,ysel) != currentS:
                    canAdd = False
            if canAdd:
                caseSel.append( (xC,yC) )

def mouseWheel(dir):
    global changesSaved
    if cursor == "sprite":
        for xC,yC in caseSel:
            if dir > 0:
                curr = regionEditee.at(xC,yC)
                next = curr
                if curr == max( list( dessin.listSprites.keys() ) ):
                    next = min( list( dessin.listSprites.keys() ) )
                else:
                    next = curr+1
                    while not next in dessin.listSprites.keys():
                        next += 1
                regionEditee.setAt(xC,yC,next)
                changesSaved = False
            else:
                curr = regionEditee.at(xC,yC)
                next = curr
                if curr == min( list( dessin.listSprites.keys() ) ):
                    next = max( list( dessin.listSprites.keys() ) )
                else:
                    next = curr-1
                    while not next in dessin.listSprites.keys():
                        next -= 1
                regionEditee.setAt(xC,yC,next)
                changesSaved = False

#réduit la taille de la région en enlevant les bords vides inutiles
def optimiseStep():
    #sur -x
    iter = regionEditee.readOffset[0]
    opti = True
    for i in range( regionEditee.readOffset[1] , regionEditee.height+regionEditee.readOffset[1] ):
        if regionEditee.at(iter,i) != 0:
            opti = False
    if opti:
        regionEditee.readOffset[0] += 1
        regionEditee.width -= 1
        regionEditee.data.pop(0)
        return True
    #sur +x
    iter = regionEditee.readOffset[0]+regionEditee.width-1
    opti = True
    for i in range( regionEditee.readOffset[1] , regionEditee.height+regionEditee.readOffset[1] ):
        if regionEditee.at(iter,i) != 0:
            opti = False
    if opti:
        regionEditee.width -= 1
        regionEditee.data.pop(regionEditee.width)
        return True
    #sur -y
    iter = regionEditee.readOffset[1]
    opti = True
    for i in range( regionEditee.readOffset[0] , regionEditee.width+regionEditee.readOffset[0] ):
        if regionEditee.at(i,iter) != 0:
            opti = False
    if opti:
        regionEditee.readOffset[1] += 1
        regionEditee.height -= 1
        for i in range(regionEditee.width):
            regionEditee.data[i].pop(0)
        return True
    #sur +y
    iter = regionEditee.readOffset[1]+regionEditee.height-1
    opti = True
    for i in range( regionEditee.readOffset[0] , regionEditee.width+regionEditee.readOffset[0] ):
        if regionEditee.at(i,iter) != 0:
            opti = False
    if opti:
        regionEditee.height -= 1
        for i in range(regionEditee.width):
            regionEditee.data[i].pop(regionEditee.height)
        return True
    return False

def optimiseRegion():
    while( optimiseStep() ):
        pass
    #bouge toutes les cases selectionnees
    for i in range(len(caseSel)):
        x,y = caseSel[i]
        caseSel[i] = ( x - regionEditee.readOffset[0] , y - regionEditee.readOffset[1] )
    #remet l'offset de lecture à 0
    dessin.xOffset += opt.SPRITE_SIZE * regionEditee.readOffset[0]
    dessin.yOffset += opt.SPRITE_SIZE * regionEditee.readOffset[1]
    regionEditee.resetReadOffset()

#sauvegarde la région en cours d'édition
def saveChanges():
    optimiseRegion()
    
    global changesSaved
    changesSaved = True
    
    #sprites
    try:
        f = open("map/"+option.editRegion+".txt","w")
        width = len(regionEditee.data)
        height = len(regionEditee.data[0])
        f.write( str(width)+"\t"+str(height)+"\n" )
        for y in range(height):
            line = "".join( [ str(regionEditee.data[x][y])+"\t" for x in range(width) ] ).strip("\t")+"\n"
            f.write(line)
    except Exception as e:
        print("except :",e)
    else:
        f.close()
    
    #ennemis
    try:
        f = open("map/"+option.editRegion+"_ennemi.txt","w")
        for e in ennemiList:
            line = str(e.position[1])+","+str(e.position[2])+","+e.name+"\n"
            f.write(line)
    except Exception as e:
        print("except :",e)
    else:
        f.close()
        
    #event
    try:
        f = open("map/"+option.editRegion+"_event.txt","w")
        for e in regionEditee.eventList:
            line = str(e)+"\n"
            f.write(line)
    except Exception as e:
        print("except :",e)
    else:
        f.close()
    
    
    
    
    
    
    
    
    