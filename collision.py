"""

Fichier de gestion des collisions,
pour toute entitée sur la carte

"""

import map

#liste des sprites qui entrainent une collision
collideList = [ 2,3,4,5,6,7,8,9,10,11,12,13, #murs standards
                14,15,16,17,                 #murs d'escaliers
                18]                          #planche

#retourne True si le mouvement est possible
def checkJoueur(joueur,dx,dy):
    newX = joueur.position[1] + dx
    newY = joueur.position[2] + dy
    
    if not checkCase(joueur.position[0],newX+joueur.hitbox[0],newY+joueur.hitbox[2]):
        return False
    if not checkCase(joueur.position[0],newX+joueur.hitbox[0],newY+joueur.hitbox[3]):
        return False
    if not checkCase(joueur.position[0],newX+joueur.hitbox[1],newY+joueur.hitbox[3]):
        return False
    if not checkCase(joueur.position[0],newX+joueur.hitbox[1],newY+joueur.hitbox[2]):
        return False
    return True

#retourne False si la position (x,y) contient une case non accessible
def checkCase(regionName,x,y):
    if map.theMap.regionList[regionName].at( int(x) , int(y) ) in collideList:
        return False
    return True