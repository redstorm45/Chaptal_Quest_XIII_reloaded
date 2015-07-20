"""

gestion des boss

"""
import math
import projectile
import random

class boss:
    def __init__(self,name,x,y):
        self.name = name
        self.position = ["salle/E.1",x,y]
        
        file = open("ennemi/Boss/" + name +".txt")                     #charge le fichier correspondant au boss
        self.spriteName  = file.readline().strip().split(";")
        self.projectileSpriteName = str(file.readline().strip().split(";")[0])
        self.portee      = float(file.readline().strip().split(";")[0])
        self.dMaxAgro    = float(file.readline().strip().split(";")[0])
        self.dMinAgro    = float(file.readline().strip().split(";")[0])
        self.spriteNb    = int(file.readline().strip().split(";")[0])
        self.lvl         = int(file.readline().strip().split(";")[0])
        self.hp          = self.lvl*100
        self.dammage     = 0
        self.armure      = int(file.readline().strip().split(";")[0])
        self.hitbox      = eval(file.readline().strip().split(";")[0])
        self.spriteName  = str(self.spriteName[0])
        self.exp         = int(file.readline().strip().split(";")[0])
        self.drops       = eval(file.readline().strip().split(";")[0])
        self.degatarme = 0
        self.direction   = 1
        self.projectileLife = 300
    
        #stats
        self.anim    = 0
        self.arme    = 0
        self.aura    = "ATT"
        #timers
        self.attackTimer = 0
        self.auratimer   = 180
        self.attackanim  = 0
        
        #offset
        self.auraoffset = [0,0]
        
        #patterne du boss
        self.pattern = file.readline().strip().split(";")             
        #mais les different patterne ds une liste, attaque de base compte comme un patterne il apparait plusieurs fois
        self.patternDamage = file.readline().strip().split(";")        
        #damage des differentes attaque du boss
        self.directionCharge = None
        
        


def patterne(boss,posJ):
    posJoueur =posJ
    i = random.randrange(0,len(boss.pattern))
    #on choisit un patterne aleatoire
    boss.damage = int(boss.patternDamage[i])
    #on regarde le type du patterne
    if boss.pattern[i] == "charge":                                    
        charge(posJoueur,boss)
    if boss.pattern[i] == "ATT":
        ATT(boss)
    if boss.pattern[i] == "triple":
        tripleprojectile(boss)
    if posJ[1]-boss.position[1] < 0:
        boss.direction = 7
    elif posJ[1]-boss.position[1] > 0:
        boss.direction = 3
    elif posJ[2]-boss.position[2] > 0:
        boss.direction = 5
    elif posJ[1]-boss.position[1] < 0:
        boss.direction = 1
        

def charge(posJ,boss): 
    
    """
    Le boss fonce ds la direction du joueur le boss devient invulnerable.
    s'il touche le joueur il s'arrete et le stun en lui infilgeant des degat
    s'il touche un mur le boss et stun
    
    posJ = position joueur
    """
    d = math.sqrt((posJ[1] - boss.position[1])**2 + (posJ[2] - boss.position[2])**2)
    boss.directionCharge = [(posJ[1]-0.5 - boss.position[1])/d*1/16,(posJ[2]-0.5 - boss.position[2])/d*1/16] 
    #definit la direction de la charge
    boss.aura = "charge"
    boss.auratimer = 0
    
def ATT(boss):
    boss.aura = "ATT"
    boss.auratimer = 180

def tripleprojectile(boss):
    
    boss.aura = "triple"
    boss.auratimer = 180
    
    