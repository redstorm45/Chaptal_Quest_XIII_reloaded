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
        #variables de compétences
        self.regen          = 0.5
        self.capacite1      = "RLC"
        #timers
        self.capacite1timer = 0
    
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
            