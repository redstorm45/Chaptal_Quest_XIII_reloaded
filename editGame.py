"""

Fichier de gestion de l'édition des maps

"""
import dessin
import map
import ennemi
import keybinding
import option as opt

#liste des ennemis
ennemiList = []
reg = map.theMap.regionList[option.editRegion]

#initialisation du jeu
def init():
    global ennemiList
    
    #création des ennemis sur la map
    for e in reg.ennemiBaseList:
        type,posX,posY = e
        reg.ennemiList.append( ennemi.typesEnnemis[type].copyAt( (reg.name,posX,posY) ) )
    
    #initialisation de la liste d'ennemi
    ennemiList = map.theMap.regionList[ player.position[0] ].ennemiList[:]

#dessin de la scène
def draw(fenetre):
    global player
    
    regionAffichee = player.position[0]
    dessin.drawRegion(fenetre,regionAffichee)
    
    for e in ennemiList:
        dessin.drawPlayer(fenetre,e)
        
#touches de mouvement
def actionKeys(listPressed):
    global player,ennemiList
    
    #mouvement du joueur
    elif keybinding.isKeyActive( "LEFT" , listPressed ):
        dessin.xOffset += 1
    elif keybinding.isKeyActive( "DOWN" , listPressed ):
        dessin.yOffset += 1
    elif keybinding.isKeyActive( "RIGHT" , listPressed ):
        dessin.xOffset -= 1
    elif keybinding.isKeyActive( "UP" , listPressed ):
        dessin.yOffset -= 1

    
    
    
    
    
    
    
    
    
    