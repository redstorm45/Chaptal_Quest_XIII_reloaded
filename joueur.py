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
        super(Joueur,self).__init__(x,y)
        #caractéristiques
        self.classe = "PTSI"
        #variables d'affichage
        self.hitbox     = [ -0.25 , 0.25 , -0.1 , 0.4 ]  # xmin , xmax , ymin , ymax
        self.spriteName = "gobelin"
        self.spriteNb   = 8
        #variables de compétences
        self.regen          = 0.5
        self.capacite1      = "RLC"
        self.capacite1Lvl   = 1
        self.capacite2      = "RDM"
        self.capacite2Lvl   = 1
        self.pointbonus     = 0
        self.spritecapacite = ""
        self.positioncapacite = [0,0]
        #timers
        self.capacite1timer = 0
        self.levelup = 0
        
    
    def mouvement(self,x,y,):
        #mouvement normal
        super( Joueur , self ).mouvement(x,y)
        #test de quete
        qList = map.theMap.regionList[ self.position[0] ].eventAt( self.position[1],self.position[2],"quest" )
        for qNum in qList:
            q = quete.getQuete(qNum.q)
            if not q.trouvee:
                print("nouvelle quête:",q)
                q.trouvee = True
            