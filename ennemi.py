import collision
import os


class Ennemi:
    
    def __init__(self,name,position):
        
        self.name = name
   
        workDir = os.getcwd()
        os.chdir(workDir)
        file = open( "ennemi/" + name + ".txt")
        self.position   = position
        self.spriteName = file.readline().strip().split(";")
        self.direction  = int(file.readline().strip().split(";")[0])
        self.lvl        = int(file.readline().strip().split(";")[0])
        self.hp         =self.lvl*100
        self.dammage    = int(file.readline().strip().split(";")[0])
        self.armure      = int(file.readline().strip().split(";")[0])
        self.hitbox     = [ -1/4 , 1/4 , -1/4 , 1/4 ]
        self.position[1] = int(self.position[1])
        self.position[2] = int(self.position[2])
        self.spriteName = str(self.spriteName[0])
        self.anim       = 0 
        self.attackTimer = 0
    
     
     
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
