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

#edition d'une case de teleport
teleportCaseReg = ""        #région d'origine du téléport
teleportCase    = [0,0]     #position de la destination
teleportEvent   = 0         #numéro de l'évent séléctionné dans la liste

#nom du curseur en utilisation
# sprite (vert) : edition du fond
# item (rouge)  : edition des items
# event (bleu)  : edition des différents évenements
cursor = "sprite"

#cases selectionnées (sprites)
caseSel = []
#item selectionnée (item)
itemSel = []
#event selectionné  (event)
eventSel = None

helpSurf = None

#initialisation du jeu
def init():
    global ennemiList,regionEditee,helpSurf,changesSaved
    
    regionEditee = map.theMap.regionList[option.editRegion]
    pygame.display.set_caption("Chaptal Quest XIII - reloaded - edit["+option.editRegion+"]")
    dessin.xOffset , dessin.yOffset = 64,64
    changesSaved = False
    
    #création des ennemis sur la map
    if regionEditee.ennemiList == []:
        for e in regionEditee.ennemiBaseList:
            type,posX,posY = e
            regionEditee.ennemiList.append( ennemi.typesEnnemis[type].copyAt( (regionEditee.name,posX,posY) ) )
    
    #création des surfaces de description des events
    for e in regionEditee.eventList:
        e.surf = dessin.buttonFontXXS.render( e.__repr__() , True , (60,60,255) )
    
    #initialisation de la liste d'ennemi
    ennemiList = regionEditee.ennemiList[:]
    
    texteAide = "Aide\nMouvement : Touches de direction"
    texteAide += "\nChanger de mode : clic droit"
    texteAide += "\nMode sprite (vert):"
    texteAide += "\n -séléction avec clic gauche"
    texteAide += "\n -changement avec molette"
    helpSurf = dessin.renderMultiLine(dessin.buttonFontXXS,texteAide,20,(0,0,0),(255,255,255),align="left")

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
    xEcran = (regionEditee.readOffset[0]-0.5) * 64  + dessin.xOffset
    yEcran = (regionEditee.readOffset[1]-0.5) * 64  + dessin.yOffset
    w,h = (regionEditee.width+1)* 64,(regionEditee.height+1)* 64
    pygame.draw.lines( fenetre , (255,255,255) , True, [(xEcran   ,yEcran   ),
                                                        (xEcran+w ,yEcran   ),
                                                        (xEcran+w ,yEcran+h ),
                                                        (xEcran   ,yEcran+h )],5)
    #dessin du curseur
    xMouse,yMouse = pygame.mouse.get_pos()
    if cursor == "sprite":
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-10,yMouse-2,20,4) )
        
        for xsel,ysel in caseSel:
            xEcran = xsel * 64  + dessin.xOffset
            yEcran = ysel * 64  + dessin.yOffset
            pygame.draw.lines( fenetre , (0,255,0) , True, [(xEcran   ,yEcran   ),
                                                            (xEcran+64,yEcran   ),
                                                            (xEcran+64,yEcran+64),
                                                            (xEcran   ,yEcran+64)],2 )
    elif cursor == "item":
        pygame.draw.rect( fenetre , (255,0,0) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (255,0,0) ,(xMouse-10,yMouse-2,20,4) )
        
        if itemSel:
            [xI,yI,type] = itemSel
            surf = dessin.listItemSprites[type]
            w,h = surf.get_width(),surf.get_height()
            
            xEcran = xI * 64  + dessin.xOffset
            yEcran = yI * 64  + dessin.yOffset
            
            pygame.draw.lines( fenetre , (255,0,0) , True, [(xEcran   ,yEcran   ),
                                                            (xEcran+w ,yEcran   ),
                                                            (xEcran+w ,yEcran+h ),
                                                            (xEcran   ,yEcran+h )],2 )
                                                            
            pygame.draw.line(fenetre,(255,0,0),(xEcran   ,yEcran), (xEcran+w,yEcran+h ) ,2 )
            pygame.draw.line(fenetre,(255,0,0),(xEcran+w ,yEcran), (xEcran  ,yEcran+h ) ,2 )
        
    elif cursor == "event":
        pygame.draw.rect( fenetre , (0,0,255) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (0,0,255) ,(xMouse-10,yMouse-2,20,4) )
        
        for e in regionEditee.eventList:
            xA,yA = e.pA[0],e.pA[1]
            w,h = e.pB[0]-xA +1 ,e.pB[1]-yA +1
            w,h = w*64 , h*64
            
            xEcran = xA * 64  + dessin.xOffset
            yEcran = yA * 64  + dessin.yOffset
            if e == eventSel:
                pygame.draw.line( fenetre , (0,0,255) , (xEcran   ,yEcran   ), (xEcran+w ,yEcran+h ) ,2 )
                pygame.draw.line( fenetre , (0,0,255) , (xEcran+w ,yEcran   ), (xEcran   ,yEcran+h ) ,2 )
            fenetre.blit( e.surf , (xEcran+20,yEcran+20) )
            pygame.draw.lines( fenetre , (0,0,255) , True, [(xEcran   ,yEcran   ),
                                                            (xEcran+w ,yEcran   ),
                                                            (xEcran+w ,yEcran+h ),
                                                            (xEcran   ,yEcran+h )],2 )
        if teleportCaseReg != "":
            xEcran = teleportCase[0] * 64  + dessin.xOffset
            yEcran = teleportCase[1] * 64  + dessin.yOffset
            if eventSel == "tel":
                pygame.draw.circle( fenetre , (100,50,255) , (xEcran+32,yEcran+32) , 24 )
            pygame.draw.circle( fenetre , (50,50,255) , (xEcran+32,yEcran+32) , 16 )
        
    #dessin du cadre d'aide
    fenetre.blit( helpSurf , (fenetre.get_width()-helpSurf.get_width(),0) )
        
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
    global eventSel,teleportCaseReg,teleportCase,teleportEvent,itemSel
    #coordonnées de la case
    xC,yC = x-dessin.xOffset , y-dessin.yOffset
    xC,yC = xC//64 , yC//64
    
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
    elif cursor == "item":
        underMouse = []
        for i in regionEditee.itemList:
            [x,y,name] = i
            sprite = dessin.listItemSprites[name]
            w,h = sprite.get_width()//64-1,sprite.get_height()//64-1
            if xC >= x and xC <= x+w and yC >= y and yC <= y+h:
                underMouse.append(i)
        
        if not itemSel and underMouse:
            itemSel = underMouse[0]
        elif underMouse:
            if itemSel in underMouse:
                i = underMouse.index(itemSel)
                if len(underMouse)> i+2:
                    itemSel = underMouse[i+1]
                else:
                    itemSel = []
            else:
                itemSel = []
        currentS = regionEditee.at(xC,yC)
        canAdd = True
        for xsel,ysel in caseSel:
            if regionEditee.at(xsel,ysel) != currentS:
                canAdd = False
        if canAdd:
            caseSel.append( (xC,yC) )
    elif cursor == "event":
        for e in regionEditee.eventList:
            if e.activate(xC,yC) and eventSel != e:
                eventSel = e
            elif e.activate(xC,yC) and eventSel == e:
                if e.type == "teleport":
                    #crée les items pour l'édition de la destination
                    teleportCaseReg = option.editRegion
                    teleportCase    = [ e.dest[1],e.dest[2] ]
                    teleportEvent   = regionEditee.eventList.index(e)
                    #change de région
                    writeEvent(option.editRegion)
                    option.editRegion = e.dest[0]
                    init()
                eventSel = None
        if teleportCaseReg != "":
            if [xC,yC] == teleportCase:
                eventSel = "tel"

def clickMid(x,y):
    global eventSel,itemSel
    #coordonnées de la case
    xC,yC = x-dessin.xOffset , y-dessin.yOffset
    xC,yC = xC//64 , yC//64
    
    if cursor == "event":
        if eventSel:
            if eventSel.activate(xC,yC):
                regionEditee.eventList.remove( eventSel )
                eventSel = None
        else:
            regionEditee.eventList.append( map.EventReg("1,1,1,1:t,couloir/1.V1,1,1") )
            eventSel = regionEditee.eventList[ len(regionEditee.eventList)-1 ]
            eventSel.surf = dessin.buttonFontXXS.render( eventSel.__repr__() , True , (60,60,255) )
    elif cursor == "item":#copie l'item
        if itemSel:
            newI = [itemSel[i] for i in range(3)]
            regionEditee.itemList.append(newI)

def keyPressed(key):
    global itemSel
    if cursor == "event":
        pass
        """
        if key == "t":
            name = input("region d'arrivée")
            if not name in map.theMap.regionList.keys():
                return
            """
    elif cursor == "item":
        if key == "4":
            itemSel[0] -= 1
        elif key == "6":
            itemSel[0] += 1
        elif key == "8":
            itemSel[1] += 1
        elif key == "2":
            itemSel[1] -= 1
        elif key == "n":
            name = input("nom de l'objet")
            x,y = [ int(x) for x in input("coordonnées").split(",") ]
            itemSel = [x,y,name]
            print("added : ",itemSel)
            regionEditee.itemList.append(itemSel)

def mouseWheel(dir):
    global changesSaved
    global eventSel,teleportCaseReg,teleportCase,teleportEvent,itemSel
    if cursor == "sprite":
        for xC,yC in caseSel:
            if dir > 0:
                curr = regionEditee.at(xC,yC)
                next = curr
                if dessin.listStyleSprites.index(curr) == len( dessin.listStyleSprites )-1:
                    next = dessin.listStyleSprites[0]
                else:
                    next = dessin.listStyleSprites[ dessin.listStyleSprites.index(curr) +1 ]
                regionEditee.setAt(xC,yC,next)
                changesSaved = False
            else:
                curr = regionEditee.at(xC,yC)
                next = curr
                if dessin.listStyleSprites.index(curr) == 0:
                    next = dessin.listStyleSprites[len( dessin.listStyleSprites )-1]
                else:
                    next = dessin.listStyleSprites[ dessin.listStyleSprites.index(curr) -1 ]
                regionEditee.setAt(xC,yC,next)
                changesSaved = False
        regionEditee.preRender =  pygame.Surface( ( 64*regionEditee.width , 64*regionEditee.height ) )
        dessin.drawPreRender(regionEditee,regionEditee.preRender)
    elif cursor == "event":
        if eventSel:
            if eventSel == "tel":
                if pygame.key.get_mods() & pygame.locals.KMOD_CTRL:
                    teleportCase[0] += dir
                else:
                    teleportCase[1] += dir
                changesSaved = False
            else:
                if pygame.key.get_mods() & pygame.locals.KMOD_CTRL:
                    if pygame.key.get_mods() & pygame.locals.KMOD_SHIFT:
                        eventSel.changeSize( dir ,0 )
                    else:
                        eventSel.pA[0] += dir
                        eventSel.pB[0] += dir
                else:
                    if pygame.key.get_mods() & pygame.locals.KMOD_SHIFT:
                        eventSel.changeSize( 0,-dir )
                    else:
                        eventSel.pA[1] -= dir
                        eventSel.pB[1] -= dir
                changesSaved = False
    elif cursor == "item":
        if itemSel:
            if pygame.key.get_mods() & pygame.locals.KMOD_CTRL:
                itemSel[0] += dir
            else:
                itemSel[1] += dir
            changesSaved = False

#réduit la taille de la région en enlevant les bords vides inutiles
def optimiseStep():
    #sur -x
    iter = regionEditee.readOffset[0]
    opti = True
    for i in range( regionEditee.readOffset[1] , regionEditee.height+regionEditee.readOffset[1] ):
        if regionEditee.at(iter,i) != "v":
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
        if regionEditee.at(iter,i) != "v":
            opti = False
    if opti:
        regionEditee.width -= 1
        regionEditee.data.pop(regionEditee.width)
        return True
    #sur -y
    iter = regionEditee.readOffset[1]
    opti = True
    for i in range( regionEditee.readOffset[0] , regionEditee.width+regionEditee.readOffset[0] ):
        if regionEditee.at(i,iter) != "v":
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
        if regionEditee.at(i,iter) != "v":
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
    dessin.xOffset += 64 * regionEditee.readOffset[0]
    dessin.yOffset += 64 * regionEditee.readOffset[1]
    regionEditee.resetReadOffset()

def writeEvent(regName):
    #event
    if map.theMap.regionList[regName].eventList != []:
        try:
            f = open("map/"+regName+"_event.txt","w")
            for e in map.theMap.regionList[regName].eventList:
                line = str(e)+"\n"
                f.write(line)
        except Exception as e:
            print("except :",e)
        else:
            f.close()

#sauvegarde la région en cours d'édition
def saveChanges():
    global changesSaved,teleportCaseReg
    
    optimiseRegion()
    
    changesSaved = True
    
    #sprites
    try:
        f = open("map/"+option.editRegion+".txt","w")
        width = len(regionEditee.data)
        height = len(regionEditee.data[0])
        f.write( str(width)+"\t"+str(height)+"\t"+regionEditee.style+"\n" )
        for y in range(height):
            line = "".join( [ str(regionEditee.data[x][y])+"\t" for x in range(width) ] ).strip("\t")+"\n"
            f.write(line)
    except Exception as e:
        print("except :",e)
    else:
        f.close()
    
    #items
    if regionEditee.itemList != []:
        try:
            f = open("map/"+option.editRegion+"_item.txt","w")
            for item in regionEditee.itemList:
                line = str(item[0])+","+str(item[1])+","+item[2]+"\n"
                f.write(line)
        except Exception as e:
            print("except :",e)
        else:
            f.close()
        
    #ennemis
    if ennemiList != []:
        try:
            f = open("map/"+option.editRegion+"_ennemi.txt","w")
            for e in ennemiList:
                line = str(e.position[1])+","+str(e.position[2])+","+e.name+"\n"
                f.write(line)
        except Exception as e:
            print("except :",e)
        else:
            f.close()
    
    writeEvent(option.editRegion)
    
    if teleportCaseReg != "":#édition d'une case de téléportation
        e = map.theMap.regionList[teleportCaseReg].eventList[teleportEvent]
        e.dest = [regionEditee.name,teleportCase[0],teleportCase[1]]
        writeEvent(teleportCaseReg)
        teleportCaseReg = ""
    
    
    
    
    
    
    
    
    