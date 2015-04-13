"""

Fichier qui gère l'attribution des touches au différentes commandes

"""
from pygame.locals import *


keys = {"UP"         : [K_UP    , K_w],
        "DOWN"       : [K_DOWN  , K_s],
        "LEFT"       : [K_LEFT  , K_a],
        "RIGHT"      : [K_RIGHT , K_d],
        "DIALOGUE"   : [K_t],
        "INVENTAIRE" : [K_i],
        "ATTACK"     : [K_SPACE],
        "SORT1"      : [K_y],
        "SORT2"      : [K_u],
        "ULTI"       : [K_o],
        "UPSORT1"    : [K_h] ,
        "UPSORT2"    : [K_j] ,
        "UPSORT3"    : [K_k] ,
        "QUETES"     : [K_e] }

#vrai si toutes les touches demandées sont actives
def areKeysActive( actionList , listPressed ):
    for a in actionList:
        if not isKeyActive( a,listPressed):
            return False
    return True

#vrai si la touche demandée est active
def isKeyActive( action , listPressed ):
    for k in keys[action]:
        if listPressed[k]:
            return True
    return False
