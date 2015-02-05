import collision

speed = 1/32
dmin = 0.5
dmax = 7


def agro(positionJoueur,positionIA):
    d = (positionIA[1] - positionJoueur[1])**2 +  (positionIA[2] - positionJoueur[2])**2
    if  d < dmax**2 and d> dmin**2: #on regarde si l'ennemi est dans la zone d'agro
        return(True)
    else:
        return(False)
    

def trajectoire(positionJoueur, ennemi):
    positionIA = ennemi.position
    
    if positionIA[1] - positionJoueur[1] < 0: #changer 0 par la hitbox du perso plus tard
        #test collision decord (positionIA(0)+1)
        if collision.checkJoueur( ennemi, speed , 0 ):
            positionIA[1] = positionIA[1] +speed
    elif positionIA[1] - positionJoueur[1] > 0:
        if collision.checkJoueur( ennemi, -speed , 0 ):
            positionIA[1] = positionIA[1] -speed
    
    elif positionIA[1] - positionJoueur[1] == 0:
        positionIA[1] = positionIA[1] 
        
    if positionIA[2] - positionJoueur[2] < 0:
        if collision.checkJoueur( ennemi, 0 , speed ):
            positionIA[2] = positionIA[2] +speed
    
    if positionIA[2] - positionJoueur[2] > 0:
        if collision.checkJoueur( ennemi, 0 , -speed ):
            positionIA[2] = positionIA[2] -speed
    
    if positionIA[2] - positionJoueur[2] == 0:
        positionIA[2] = positionIA[2] 
    #on teste a chaque fois les collisions
    return(positionIA)
    
    
    