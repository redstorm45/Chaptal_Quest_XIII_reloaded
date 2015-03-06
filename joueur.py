"""

Classe de de base d'un joueur

défini les propriétées de tout les joueurs

"""

import collision
import map
import math
import joueurBase
import quete
import option as opt

class Joueur(joueurBase.JoueurBase):
    def __init__(self,x,y):
        #variables misc
        self.name   = ""
        self.classe = "PTSI"
        #variables d'affichage
        self.position   = ["salle/1.V1.1",x,y]
        self.hitbox     = [ -0.25 , 0.25 , -0.1 , 0.4 ]  # xmin , xmax , ymin , ymax
        self.spriteName = "gobelin"
        self.direction  = 1
        self.anim = 0
        #variables de compétences
        self.lvl = 1
        self.hp = 100 * self.lvl
        self.dammage = 20
        self.armure = 100
        self.attackTimer = 0
    
    def mouvement(self,x,y):
        #mouvement normal
        super( Joueur , self ).mouvement(x,y)
        #test de téléportation
        t = map.theMap.regionList[ self.position[0] ].eventAt( self.position[1],self.position[2],"teleport" )
        if t:
            if opt.debugMode:
                print("teleport",self.position)
            self.position = t[0].dest.copy()
            if opt.debugMode:
                print("teleport2",self.position)
        #test de quete
        qList = map.theMap.regionList[ self.position[0] ].eventAt( self.position[1],self.position[2],"quest" )
        for qNum in qList:
            q = quete.getQuete(qNum.q)
            if not q.trouvee:
                print("nouvelle quête:",q)
                q.trouvee = True
            