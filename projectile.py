import math

class Projectile():
    def __init__(self,tireur,cible,cibleposition=None):
        self.tireur , self.cible = tireur,cible
        #permet de tirer un projectile qui na pas la cible pour cible
        if not cibleposition:
            cibleposition = cible.position
        self.vitesse = 1/16
        
        self.distance = ( (tireur.position[1]-cibleposition[1])**2 + (tireur.position[2]-cibleposition[2])**2 )**0.5
        if self.distance == 0:
            self.distance = 1/16
        self.unitX = (cibleposition[1]-tireur.position[1])/self.distance
        self.unitY = (cibleposition[2]-tireur.position[2])/self.distance
    
        self.position = tireur.position[1] , tireur.position[2]
        
        self.life = 100
        
        self.spriteName = tireur.projectileSpriteName
    
    def avancer(self):
        self.life -= 1
        posX, posY = self.position
        posX += self.unitX * self.vitesse
        posY += self.unitY * self.vitesse
        self.position = posX,posY
    
def tripleprojectile(tireur,cible,projectileList):
    projectileCentre = Projectile(tireur,cible)
    uab = [-projectileCentre.unitY,projectileCentre.unitX]
    d = projectileCentre.distance
    #vecteur perpendiculaire au premier projectile
    pos0 = cible.position[0]
    pos1 = cible.position[1]
    pos2 = cible.position[2]
    poscible2 = [pos0,pos1,pos2]
    poscible3 = [pos0,pos1,pos2]
    poscible2[1] += uab[0]*d
    poscible2[2] += uab[1]*d
    poscible3[1] -= uab[0]*d
    poscible3[2] -= uab[1]*d
    projectileList.append(projectileCentre)
    projectileList.append(Projectile(tireur,cible,poscible2))
    projectileList.append(Projectile(tireur,cible,poscible3))
    print("triple:")
    print(cible.position,poscible2,poscible3)
   
    