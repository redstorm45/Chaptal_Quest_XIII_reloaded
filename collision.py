"""

Fichier de gestion des collisions,
pour toute entitée sur la carte

"""

import map

#liste des sprites qui entrainent une collision
collideList = [ "m1","m2","m3","m4","m5","m6","m7","m8", #murs standards
                "a1","a2","a3","a4","a5","a6","a7","a8", #angles
                "b1","b2","b3","b4","b5","b6","b7","b8", #angles
                "p","v"]                        #planche , vide

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

def checkProjectile(projectile,joueur):
    if projectile.position[0] < joueur.position[1] + joueur.hitbox[0]:
        return False
    if projectile.position[0] > joueur.position[1] + joueur.hitbox[1]:
        return False
    if projectile.position[1] < joueur.position[2] + joueur.hitbox[2]:
        return False
    if projectile.position[1] > joueur.position[2] + joueur.hitbox[3]:
        return False
    return True

#retourne False si la position (x,y) contient une case non accessible
def checkCase(regionName,x,y):
    if map.theMap.regionList[regionName].at( int(x) , int(y) ) in collideList:
        return False
    return True