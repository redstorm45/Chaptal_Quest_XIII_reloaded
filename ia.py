"""

Fichier de gestion de l'ia,
commun à tous les ennemis

"""

import collision
from math import exp

speed = 1/32
dmin = 0.5
dmax = 3
dattack = 0.75

#test si une IA doit aller vers le joueur
def agro(positionJoueur,positionIA):
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if  d < dmax**2 and d> dmin**2: #on regarde si l'ennemi est dans la zone d'agro
        return(True)
    else:
        return(False)
    
#effectue un mouvement en direction du joueur
def trajectoire(positionJoueur, ennemi):
    positionIA = ennemi.position
    mvtX , mvtY = 0,0
    
    #on teste a chaque fois les collisions
    if positionIA[1] - positionJoueur[1] < 0: #changer 0 par la hitbox du perso plus tard
        mvtX = speed
    elif positionIA[1] - positionJoueur[1] > 0:
        mvtX = -speed
    
    elif positionIA[1] - positionJoueur[1] == 0:
        pass
        
    if positionIA[2] - positionJoueur[2] < 0:
        mvtY = speed
    
    if positionIA[2] - positionJoueur[2] > 0:
        mvtY = -speed
    
    if positionIA[2] - positionJoueur[2] == 0:
        pass
        
    ennemi.mouvement(mvtX,mvtY)
    
    return(positionIA)

#effectue l'attaque d'une IA sur le joueur à distance suffisante
def attackIA(joueur,ennemi):
    positionIA = ennemi.position
    positionJoueur = joueur.position
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if d < dattack **2 and ennemi.attackTimer == 0:
        joueur.hp = joueur.hp - (ennemi.dammage*exp(-joueur.armure/300))
        ennemi.attackTimer = 1
        
    
    
    