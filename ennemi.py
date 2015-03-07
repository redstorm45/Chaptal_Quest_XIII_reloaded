
import collision
import joueurBase


class Ennemi(joueurBase.JoueurBase):
    
    def __init__(self,name,position):
        super(Ennemi,self).__init__(int(position[1]),int(position[2]))
        self.name = name
   
        file = open( "ennemi/" + name + ".txt")
        self.position[0] = position[0]
        self.spriteName  = file.readline().strip().split(";")
        self.direction   = int(file.readline().strip().split(";")[0])
        self.lvl         = int(file.readline().strip().split(";")[0])
        self.hp          = self.lvl*100
        self.dammage     = int(file.readline().strip().split(";")[0])
        self.armure      = int(file.readline().strip().split(";")[0])
        self.hitbox      = [ -1/4 , 1/4 , -1/4 , 1/4 ]
        self.spriteName  = str(self.spriteName[0])
     
     
    def mouvement(self,x,y):
        if x> 0:
            self.direction = 4
        elif x< 0:
            self.direction = 8
        elif y> 0:
            self.direction = 2
        elif y< 0:
            self.direction = 6
        else:
            if self.direction % 2 == 0:
                self.direction -= 1
            
        if collision.checkJoueur(self,x,0):
            self.position[1] += x
        if collision.checkJoueur(self,0,y):
            self.position[2] += y
