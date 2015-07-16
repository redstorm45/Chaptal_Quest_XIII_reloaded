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
import inventaire

class Joueur(joueurBase.JoueurBase):
    def __init__(self,x,y):
        super(Joueur,self).__init__(x,y)
        #caractéristiques
        self.classe = "PTSI"
        self.inventaire = None
        self.nomarme = 'epee_en_bois'
        self.arme = inventaire.objet(self.nomarme)
        self.nomcasque = "casque"
        self.casque = inventaire.objet(self.nomcasque)
        self.nomarmure = 'armure'
        self.armure = inventaire.objet(self.nomarmure)
        #variables d'affichage
        self.hitbox     = [ -0.25 , 0.25 , -0.1 , 0.4 ]  # xmin , xmax , ymin , ymax
        self.spriteName = "PTSI"
        self.spriteNb   = 4
        self.surfLvl    = None
        #variables de compétences
        self.regen          = 0.5
        self.capacite1      = "RLC"
        self.capacite1Lvl   = 0
        self.capacite2      = "PFS"
        self.capacite2Lvl   = 0
        self.capacite3      = "RDM"
        self.capacite3Lvl   = 0
        self.ULTI           = "Laplace"
        self.ULTILvl        = 0
        self.pointbonus     = 0
        self.spriteCapacite = ""
        self.positionCapacite = [0,0]
        self.degatarme = int(self.arme.degatarme)
        self.armure = int(self.casque.defense) + int(self.armure.defense)
        #timers
        self.capacite1timer = 0
        self.capacite2timer = 0
        self.capacite3timer = 0
        self.ULTITimer = 0
        self.levelup = 0
        self.spriteCapaciteTimer = 0
        self.combat = 0
        self.auraoffset = [0,0]
        
    
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
            