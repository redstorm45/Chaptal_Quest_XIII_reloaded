#gere les capacites du joueur





def capacite(typecapacite,joueur,ennemis):
    if typecapacite == 'RLC':
        RLC(joueur,ennemis)
    if typecapacite == 'RDM':
        RDM(joueur,ennemis)


def RLC(joueur,ennemis):
    
    posJ = [ joueur.position[1],joueur.position[2] ]
    
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
    
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.direction in [1,2]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                ennemis[i].hp = ennemis[i].hp - 50*joueur.capacite1Lvl
                ennemis[i].aura = "eclair"
                ennemis[i].auratimer = 0.5*30
        elif joueur.direction in [3,4]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                ennemis[i].hp = ennemis[i].hp - 50*joueur.capacite1Lvl
                ennemis[i].aura = "eclair"
                ennemis[i].auratimer = 0.5*30
        if joueur.direction in [5,6]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                ennemis[i].hp = ennemis[i].hp - 50*joueur.capacite1Lvl
                ennemis[i].aura = "eclair"
                ennemis[i].auratimer = 0.5*30
        if joueur.direction in [7,8]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                ennemis[i].hp = ennemis[i].hp - 50*joueur.capacite1Lvl
                ennemis[i].aura = "eclair"
                ennemis[i].auratimer = 0.5*30
            
        
def RDM(joueur,ennemi):
     if  ennemi.armure - joueur.lvl*5 > 0:
         ennemi.armure = ennemi.armure - joueur.capacite2Lvl*5
     else:
         ennemi.armure = 0