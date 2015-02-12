"""

Classe de de base d'un joueur

défini les propriétées de tout les joueurs

"""

import collision
import map
import math
import joueurBase

class Joueur(joueurBase.JoueurBase):
    def __init__(self,x,y):
        self.name       = ""
        self.position   = ["base",x,y]
        self.hitbox     = [ -0.25 , 0.25 , -0.1 , 0.4 ]  # xmin , xmax , ymin , ymax
        self.spriteName = "gobelin"
        self.direction  = 1
        self.lvl = 1
        self.hp = 100 * self.lvl
        self.dammage = 20
        self.armure = 100
        self.anim = 0
        self.attackTimer = 0
    
    def mouvement(self,x,y):
        #mouvement normal
        super( Joueur , self ).mouvement(x,y)
        #test de téléportation
        t = map.theMap.regionList[ self.position[0] ].teleportAt( self.position[1],self.position[2] )
        if t:
            self.position = [ t[0] , t[1] , t[2] ]
            