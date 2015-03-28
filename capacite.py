#gere les capacites du joueur





def capacite(typecapacite,joueur,ennemis):
    if typecapacite == 'RLC':
        RLC(joueur,ennemis)
    if typecapacite == 'RDM':
        RDM(joueur,ennemis)


def RLC(joueur,ennemis):
    
    posJ = [ joueur.position[1],joueur.position[2] ]
    if joueur.capacite1Lvl >= 3:
        joueur.spriteCapacite = "eclairBHDG"
        joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-2.5]
        
    elif joueur.direction in [1,2]:
        if joueur.capacite1Lvl == 1:
            joueur.spriteCapacite = "eclairB"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]]
        elif joueur.capacite1Lvl == 2:
            joueur.spriteCapacite = "eclairBH"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]-2.5]
    elif joueur.direction in [3,4]:
        if joueur.capacite1Lvl == 1:
            joueur.positionCapacite = [posJ[0],posJ[1]-1]
            joueur.spriteCapacite = "eclairD"
        elif joueur.capacite1Lvl == 2:
            joueur.spriteCapacite = "eclairDG"
            joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-1]
    elif joueur.direction in [5,6]:
        if joueur.capacite1Lvl == 1:
            joueur.spriteCapacite = "eclairH"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]-2]
        elif joueur.capacite1Lvl == 2:
             joueur.spriteCapacite = "eclairBH"
             joueur.positionCapacite = [posJ[0]-1,posJ[1]-2.5]
    elif joueur.direction in [7,8]:
        if joueur.capacite1Lvl == 1:
            joueur.spriteCapacite = "eclairG"
            joueur.positionCapacite = [posJ[0]-2,posJ[1]-1]
        elif joueur.capacite1Lvl == 2:
            joueur.spriteCapacite = "eclairDG"
            joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-1]
            
    joueur.spriteCapaciteTimer = 0.25*60
    
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
    
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.capacite1Lvl == 1:
            if joueur.direction in [1,2]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
            elif joueur.direction in [3,4]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
            elif joueur.direction in [5,6]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
            elif joueur.direction in [7,8]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
        elif joueur.capacite1Lvl == 2:
            if joueur.direction in [1,2,5,6]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]) or d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
            elif joueur.direction in [3,4,7,8]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]) or d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                   degatRLC(ennemis[i],joueur.capacite1Lvl) 
        else:
            if d < 2**2:
                degatRLC(ennemis[i],joueur.capacite1Lvl)
                
                
def RDM(joueur,ennemi):
     if  ennemi.armure - joueur.lvl*5 > 0:
         ennemi.armure = ennemi.armure - joueur.capacite2Lvl*5
     else:
         ennemi.armure = 0

def degatRLC(ennemi,lvl):
    ennemi.hp = ennemi.hp - 50*lvl
    ennemi.aura = "Laplace"
    ennemi.auratimer = 2*30
    