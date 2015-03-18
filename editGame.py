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

#liste des ennemis
ennemiList = []

#région en édition
regionEditee = None

#nom du curseur en utilisation
# sprite (vert) : edition du fond
# item (rouge)  : edition des items
# event (bleu)  : edition des différents évenements
cursor = "sprite"

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
    
    regionAffichee = regionEditee.name
    dessin.drawRegion(fenetre,regionAffichee)
    
    for e in ennemiList:
        dessin.drawPlayer(fenetre,e)
    
    xMouse,yMouse = pygame.mouse.get_pos()
    if cursor == "sprite":
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-2,yMouse-10,4,20) )
        pygame.draw.rect( fenetre , (0,255,0) ,(xMouse-10,yMouse-2,20,4) )
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

#clique gauche à un endroit: change le mode d'édition
def click(x,y):
    global cursor
    if cursor == "sprite":
        cursor = "item"
    elif cursor == "item":
        cursor = "event"
    elif cursor == "event":
        cursor = "sprite"
        
#clique droite à un endroit: selectionne la case
def clickR(x,y):
    pass

#sauvagarde la région en cours d'édition
def saveChanges():
    pass
    
    
    
    
    
    
    
    
    