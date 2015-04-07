"""

Fichier de gestion des attaques de joueur à ennemi
et d'ennemi à joueur

"""

import capacite

from math import exp

def attack(joueur,ennemis):
    #vers le bas
    posJ = [ joueur.position[1],joueur.position[2] ]
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
        damJ = (joueur.dammage + joueur.lvl + joueur.degatarme)*exp(-ennemis[i].armure/300)
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.direction in [1,2]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])                    
                ennemis[i].hp = ennemis[i].hp - damJ
                
        elif joueur.direction in [3,4]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ
        
        if joueur.direction in [5,6]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ
        
        if joueur.direction in [7,8]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                if joueur.capacite2 == "RDM":
                    capacite.capacite("RDM",joueur,ennemis[i])
                ennemis[i].hp = ennemis[i].hp - damJ