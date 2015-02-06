import collision
import math
import joueurBase

class Joueur(joueurBase.JoueurBase):
    
    def __init__(self,x,y):
        self.name       = ""
        self.position   = ["base",x,y]
        self.hitbox     = [ -1/4 , 1/4 , -1/4 , 1/4 ]  # xmin , xmax , ymin , ymax
        self.spriteName = "gobelin"
        self.direction  = 1
        self.lvl = 1
        self.hp = 100 * self.lvl
        self.dammage = 5
        self.armure = 100
    
            