
import collision
import joueurBase
import copy

class Ennemi(joueurBase.JoueurBase):
    
    def __init__(self,name):
        super(Ennemi,self)
        self.name = name
   
        file = open( "ennemi/" + name + ".txt")
        self.spriteName  = file.readline().strip().split(";")
        self.typeAttaque = int(file.readline().strip().split(";")[0])
        self.direction   = 1
        self.portee      = float(file.readline().strip().split(";")[0])
        self.dMaxAgro    = float(file.readline().strip().split(";")[0])
        self.dMinAgro    = float(file.readline().strip().split(";")[0])
        self.spriteNb    = int(file.readline().strip().split(";")[0])
        self.lvl         = int(file.readline().strip().split(";")[0])
        self.hp          = self.lvl*100
        self.dammage     = int(file.readline().strip().split(";")[0])
        self.armure      = int(file.readline().strip().split(";")[0])
        self.hitbox      = [ -1/4 , 1/4 , -1/4 , 1/4 ]
        self.spriteName  = str(self.spriteName[0])
        self.exp         = int(file.readline().strip().split(";")[0])
    
        #stats
        self.anim    = 0
        self.arme    = 0
        self.aura    = ""
        #timers
        self.attackTimer = 0
        self.auratimer   = 0
        self.attackanim  = 0
        
    def copyAt(self,position):
        newEnnemi = copy.deepcopy(self)
        newEnnemi.position = list(position)
        return newEnnemi
     
    def __repr__(self):
        return self.name+" at("+str(self.position[1])+","+str(self.position[2])+")"
     
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
        
    def translate(self,dx,dy):
        r,ox,oy = self.position
        self.position = r,ox+dx,oy+dy 

typesEnnemis = {"gobelin"  : Ennemi("gobelin") ,
                "orc"      : Ennemi("orc") }
