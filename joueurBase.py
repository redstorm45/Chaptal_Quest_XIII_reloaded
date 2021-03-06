"""

Classe de de base d'une entitée

défini les propriétées communes aux joueurs et ennemis

"""

import collision

class JoueurBase:
    def __init__(self,x,y):
        #caractéristiques
        self.name       = ""
        self.position   = ["base",x,y]
        self.hitbox     = [ -0.25 , 0.25 , -0.2 , 0.3 ]  # xmin , xmax , ymin , ymax
        #dessin
        self.spriteName = "gobelin"
        self.direction  = 1
        #stats
        self.lvl     = 1
        self.hp      = 100 * self.lvl
        self.dammage = 5
        self.armure  = 100
        self.anim    = 0
        self.arme    = 0
        self.aura    = ""
        #timers
        self.attackTimer = 0
        self.auratimer   = 0
        self.attackanim  = 0
        
    #mouvement de x cases vers la droite
    # et de y cases vers le bas
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

