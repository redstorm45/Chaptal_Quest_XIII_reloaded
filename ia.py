"""

Fichier de gestion de l'ia,
commun à tous les ennemis

"""

import collision
import projectile
from math import exp

speed = 1/32
dmin = 0.5
dmax = 3

#test si une IA doit aller vers le joueur
def agro(positionJoueur,ennemi):
    positionIA = ennemi.position
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if  d < ennemi.dMaxAgro**2 and d> ennemi.dMinAgro**2: #on regarde si l'ennemi est dans la zone d'agro
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
def attackIA(joueur,ennemi,projectileList):
    positionIA = ennemi.position
    positionJoueur = joueur.position
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if d < ennemi.portee **2 and ennemi.attackTimer == 0:
        if ennemi.typeAttaque == 2:
            joueur.hp = joueur.hp - (ennemi.dammage*exp(-joueur.armure/300))
        elif ennemi.typeAttaque == 1:
            projectileList.append( projectile.Projectile(ennemi,joueur) )
        ennemi.attackTimer = 1
    
        
    
    
    