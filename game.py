"""

Fichier de gestion de toutes les variables pendant la phase de jeu
(gère l'histoire entre autres)

"""

import dessin
import keybinding
import joueur
import ennemi
import map
import ia
import option as opt

#defini un joueur
player = joueur.Joueur(2,2)

#initialisation du jeu (création des ennemis)
def init():
    for k in map.theMap.regionList.keys():
        r = map.theMap.regionList[k]
        for e in r.ennemiBaseList:
            r.ennemiList.append( ennemi.Ennemi( e[0] , [ k , e[1] , e[2] ] ) )

#dessin de la scène
def draw(fenetre):
    global player
    
    regionAffichee = player.position[0]
    dessin.centerOffset(player)
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    for e in map.theMap.regionList[ player.position[0] ].ennemiList:
        dessin.drawPlayer(fenetre,e)

#touches de mouvement
def actionKeys(listPressed):
    global player
    
    if keybinding.areKeysActive(["LEFT","UP"],listPressed):
        player.mouvement( -opt.speedDiag , -opt.speedDiag )
    elif keybinding.areKeysActive(["LEFT","DOWN"],listPressed):
        player.mouvement( -opt.speedDiag ,  opt.speedDiag )
    elif keybinding.areKeysActive(["RIGHT","DOWN"],listPressed):
        player.mouvement(  opt.speedDiag ,  opt.speedDiag )
    elif keybinding.areKeysActive(["RIGHT","UP"],listPressed):
        player.mouvement(  opt.speedDiag , -opt.speedDiag )
    elif keybinding.isKeyActive( "LEFT" , listPressed ):
        player.mouvement( -opt.speed , 0 )
    elif keybinding.isKeyActive( "DOWN" , listPressed ):
        player.mouvement( 0 ,  opt.speed )
    elif keybinding.isKeyActive( "RIGHT" , listPressed ):
        player.mouvement( opt.speed ,  0 )
    elif keybinding.isKeyActive( "UP" , listPressed ):
        player.mouvement( 0 , -opt.speed )
    else:
        player.mouvement( 0 , 0 )
    
    if keybinding.isKeyActive( "ATTACK" , listPressed ):
        attackJoueur.attack(player,listEnnemis)

#evenement de mise à jour (ia et animations)    
def tick():
    player.anim += 0.2
    #IA
    for e in map.theMap.regionList[ player.position[0] ].ennemiList:
        if e.hp < 0:
            listEnnemis.remove(e)
        if ia.agro(player.position,e.position):
            ia.trajectoire(player.position,e)
        
        ia.attackIA(player,e)
        
    
    
    
    
    
    
    
    
    
    
    
    
    