#gere les capacites du joueur





def capacite(typecapacite,joueur,ennemis):
    if typecapacite == 'RLC':
        RLC(joueur,ennemis)
    elif typecapacite == 'RDM':
        RDM(joueur,ennemis)
    elif typecapacite == 'PFS':
        PFS(joueur,ennemis)
    elif typecapacite == 'Laplace':
        Laplace(joueur,ennemis)
    

def RLC(joueur,ennemis):
    
    posJ = [ joueur.position[1],joueur.position[2] ]
    if joueur.capacite1Lvl >= 5:
        joueur.spriteCapacite = "eclairBHDG"
        joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-2.5]
        
    elif joueur.direction in [1,2]:
        if joueur.capacite1Lvl in [1,2]:
            joueur.spriteCapacite = "eclairB"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]]
        elif joueur.capacite1Lvl in [3,4]:
            joueur.spriteCapacite = "eclairBH"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]-2.5]
    elif joueur.direction in [3,4]:
        if joueur.capacite1Lvl in [1,2]:
            joueur.positionCapacite = [posJ[0],posJ[1]-1]
            joueur.spriteCapacite = "eclairD"
        elif joueur.capacite1Lvl in [3,4]:
            joueur.spriteCapacite = "eclairDG"
            joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-1]
    elif joueur.direction in [5,6]:
        if joueur.capacite1Lvl in [1,2]:
            joueur.spriteCapacite = "eclairH"
            joueur.positionCapacite = [posJ[0]-1,posJ[1]-2]
        elif joueur.capacite1Lvl in [3,4]:
             joueur.spriteCapacite = "eclairBH"
             joueur.positionCapacite = [posJ[0]-1,posJ[1]-2.5]
    elif joueur.direction in [7,8]:
        if joueur.capacite1Lvl in [1,2]:
            joueur.spriteCapacite = "eclairG"
            joueur.positionCapacite = [posJ[0]-2,posJ[1]-1]
        elif joueur.capacite1Lvl in [3,4]:
            joueur.spriteCapacite = "eclairDG"
            joueur.positionCapacite = [posJ[0]-2.5,posJ[1]-1]
            
    joueur.spriteCapaciteTimer = 0.25*60
    
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
    
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.capacite1Lvl >= 2:
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
        elif joueur.capacite1Lvl >= 4:
            if joueur.direction in [1,2,5,6]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]) or d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                    degatRLC(ennemis[i],joueur.capacite1Lvl)
            elif joueur.direction in [3,4,7,8]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]) or d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                   degatRLC(ennemis[i],joueur.capacite1Lvl) 
        else:
            if d < 2**2:
                degatRLC(ennemis[i],joueur.capacite1Lvl)


def degatRLC(ennemi,lvl):
    ennemi.hp = ennemi.hp -50 - 25*(lvl-1)
    ennemi.aura = ""
    ennemi.auratimer = 2*30
                
                
def RDM(joueur,ennemi):
    if  ennemi.armure - joueur.lvl*5 > 0:
        ennemi.armure = ennemi.armure - joueur.capacite2Lvl*10
    else:
        ennemi.armure = 0

def PFS(joueur,ennemis):
    joueur.spriteCapacite = ''
    posJ = [ joueur.position[1],joueur.position[2] ]
    if joueur.direction in [1,2]:
        joueur.positionCapacite = [posJ[0]-1,posJ[1]]
    elif joueur.direction in [3,4]:
        joueur.positionCapacite = [posJ[0],posJ[1]-1]
    elif joueur.direction in [5,6]:
        joueur.positionCapacite = [posJ[0]-1,posJ[1]-2]
    elif joueur.direction in [7,8]:
        joueur.positionCapacite = [posJ[0]-2,posJ[1]-1]
    
    joueur.spriteCapaciteTimer = 0.25*60
    
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        e = ennemis[i]
        if joueur.capacite1Lvl == 1:
            if joueur.direction in [1,2]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                    e.aura = 'stun'  
                    e.auratimer = 60*3    
                    e.auraoffset = [0,0]  
        elif joueur.direction in [3,4]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                    e.aura = 'stun'
                    e.auratimer = 60*3  
                    e.auraoffset = [0,0]                  
        elif joueur.direction in [5,6]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                    e.aura = 'stun'  
                    e.auratimer = 60*3  
                    e.auraoffset = [0,0]                 
        elif joueur.direction in [7,8]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                    e.aura = 'stun'
                    e.auratimer = 60*3 
                    e.auraoffset = [0,0]
                    
                    
def Laplace(joueur,ennemis):
    posJ = [ joueur.position[1],joueur.position[2] ]
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        e = ennemis[i]
        if joueur.capacite1Lvl == 1:
            if joueur.direction in [1,2]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                    e.aura = 'Laplace'  
                    e.auratimer = 60*3*joueur.ULTILvl                          
                    e.auraoffset = [-150,0]
        elif joueur.direction in [3,4]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                    e.aura = 'Laplace'
                    e.auratimer = 60*3*joueur.ULTILvl                
                    e.auraoffset = [-150,0]                
        elif joueur.direction in [5,6]:
                if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                    e.aura = 'Laplace'  
                    e.auratimer = 60*3*joueur.ULTILvl                         
                    e.auraoffset = [-150,0]          
        elif joueur.direction in [7,8]:
                if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                    e.aura = 'Laplace'
                    e.auratimer = 60*3*joueur.ULTILvl
                    e.auraoffset = [-150,0]
    
    