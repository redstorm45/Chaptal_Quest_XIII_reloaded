"""

Fichier de gestion de toutes les variables pendant la phase de jeu
(gère l'histoire entre autres)

"""

import dessin
import keybinding
import joueur
import ennemi
import option as opt

#defini un joueur et ennemi
player = joueur.Joueur(2,2)
listEnnemis = []

#dessin de la scène
def draw(fenetre):
    global player
    
    regionAffichee = player.position[0]
    dessin.centerOffset(player)
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    for e in listEnnemis:
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
    player.anim += 0.28
    #IA
    for e in listEnnemis:
        if e.hp < 0:
            listEnnemis.remove(e)
        if ia.agro(player.position,e.position):
            ia.trajectoire(player.position,e)
        
        ia.attackIA(player,e)
        
    
    
    
    
    
    
    
    
    
    
    
    
    