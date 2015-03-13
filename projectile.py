

class Projectile():
    def __init__(self,tireur,cible):
        self.tireur , self.cible = tireur,cible
        self.vitesse = 1/16
        
        distance = ( (tireur.position[1]-cible.position[1])**2 + (tireur.position[2]-cible.position[2])**2 )**0.5
        self.unitX = (cible.position[1]-tireur.position[1])/distance
        self.unitY = (cible.position[2]-tireur.position[2])/distance
    
        self.position = tireur.position[1] , tireur.position[2]
        
        self.life = 100
    
    def avancer(self):
        self.life -= 1
        posX, posY = self.position
        posX += self.unitX * self.vitesse
        posY += self.unitY * self.vitesse
        self.position = posX,posY
    