#gere les capacites du joueur





def capacite(typecapacite,joueur,ennemis):
    if typecapacite == 'RLC':
        RLC(joueur,ennemis)


def RLC(joueur,ennemis):
    
    posJ = [ joueur.position[1],joueur.position[2] ]
    for i in range(len(ennemis)):
        posE = [ ennemis[i].position[1],ennemis[i].position[2] ]
    
        d = (posE[0]-posJ[0])**2 + (posE[1]-posJ[1])**2
        if joueur.direction in [1,2]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= (posE[1]-posJ[1]):
                ennemis[i].hp = ennemis[i].hp - 1
                ennemis[i].aura = "eclair"
        elif joueur.direction in [3,4]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= (posE[0]-posJ[0]):
                ennemis[i].hp = ennemis[i].hp - 1
                ennemis[i].aura = "eclair"
        if joueur.direction in [5,6]:
            if d < 2**2 and abs(posE[0]-posJ[0]) <= -(posE[1]-posJ[1]):
                ennemis[i].hp = ennemis[i].hp - 1
                ennemis[i].aura = "eclair"
        if joueur.direction in [7,8]:
            if d < 2**2 and abs(posE[1]-posJ[1]) <= -(posE[0]-posJ[0]):
                ennemis[i].hp = ennemis[i].hp - 1
                ennemis[i].aura = "eclair"
            
        
        