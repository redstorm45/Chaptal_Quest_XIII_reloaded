import collision

speed = 1/32
dmin = 0.5
dmax = 3


def agro(positionJoueur,positionIA):
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if  d < dmax**2 and d> dmin**2: #on regarde si l'ennemi est dans la zone d'agro
        return(True)
    else:
        return(False)
    

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

def attackIA(joueur,ennemi):
    positionIA = ennemi.position
    positionJoueur = joueur.position
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if d < dmin **2:
        joueur.hp = joueur.hp - ennemi.dammage
    
    
    