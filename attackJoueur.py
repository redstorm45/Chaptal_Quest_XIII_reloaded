"""

Fichier de gestion des attaques de joueur à ennemi
et d'ennemi à joueur

"""

import capacite
import collision

from math import exp

def attack(joueur,ennemis):
    #vers le bas
    posJ = [ joueur.position[1],joueur.position[2] ]
    for i in range(len(ennemis)):
        posH = collision.hitbox(ennemis[i])
        posE = [ennemis[i].position[1],ennemis[i].position[2]]
        damJ = (joueur.dammage + joueur.lvl + joueur.degatarme)*exp(-ennemis[i].armure/300)
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.direction in [1,2]:
            if (aportee(posJ,posH[0]) <4 or aportee(posJ,posH[1])<4) and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])                    
                ennemis[i].hp = ennemis[i].hp - damJ
                
        elif joueur.direction in [3,4]:
            if (aportee(posJ,posH[0]) <4 or aportee(posJ,posH[3])<4) and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ
        
        if joueur.direction in [5,6]:
            if (aportee(posJ,posH[3]) <4 or aportee(posJ,posH[2])<4) and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ
        
        if joueur.direction in [7,8]:
            if (aportee(posJ,posH[1]) <4 or aportee(posJ,posH[2])<4) and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ

def aportee(posJ,posE):
    d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
    return(d)
    