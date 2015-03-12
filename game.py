"""

Fichier de gestion de toutes les variables pendant la phase de jeu
(gère l'histoire entre autres)

"""
import projectile
import dessin
import keybinding
import joueur
import ennemi
import map
import ia
import quete
import option as opt
import attackJoueur
import capacite

#defini un joueur
player = joueur.Joueur(2,2)
projectileList = []

#initialisation du jeu
def init():
    #création des ennemis sur la map
    for k in map.theMap.regionList.keys():
        r = map.theMap.regionList[k]
        for e in r.ennemiBaseList:
            r.ennemiList.append( ennemi.Ennemi( e[0] , [ k , e[1] , e[2] ] ) )
        
    #chargement des quêtes
    quete.loadQuetes()
    quete.refreshActive()

#dessin de la scène
def draw(fenetre):
    global player
    
    regionAffichee = player.position[0]
    dessin.centerOffset(player)
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    
    for e in map.theMap.regionList[ player.position[0] ].ennemiList:
        dessin.drawPlayer(fenetre,e)
        
    for p in projectileList:
        dessin.drawProjectile(fenetre,p)
        
    if player.attackanim > 0:
        dessin.animAttack(fenetre,player)    
        player.attackanim -=1

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
        if player.attackTimer == 0:
            attackJoueur.attack(player,map.theMap.regionList[player.position[0]].ennemiList)
            player.attackTimer = 1
            player.attackanim  = 0.2*60
        else:
            player.attackTimer = max( 0, player.attackTimer - 1/16)
    if keybinding.isKeyActive( "SORT1" , listPressed ) and player.capacite1timer == 0:
        capacite.capacite('RLC',player,map.theMap.regionList[player.position[0]].ennemiList)
        player.capacite1timer = player.capacite1timer + 60*3
        
    if keybinding.isKeyActive( "UPSORT1" , listPressed ) and player.pointbonus > 0:
        player.capacite1Lvl += 1
        player.pointbonus -=1
        
    if player.capacite1timer > 0:
        player.capacite1timer -= 1
    #print(player.capacite1timer)
    

#evenement de mise à jour (ia et animations)    
def tick():
    player.anim += 0.25
    #avancement de projectiles
    for p in projectileList:
        p.avancer()
        
        if p.life < 0:
            projectileList.remove(p)
    
    #IA
    for e in map.theMap.regionList[ player.position[0] ].ennemiList:
        if map.theMap.regionList[ player.position[0] ].ennemiList(e).aura != "stun":
            #mort d'un ennemi
            if e.hp < 0:
                map.theMap.regionList[ player.position[0] ].ennemiList.remove(e)
                player.levelup += e.exp
        
            #deplacement d'ennemi
            if ia.agro(player.position,e):
                ia.trajectoire(player.position,e)
                e.anim += 0.25
            elif e.anim != 0:
                e.anim = 0
                e.mouvement(0,0)
        
            #attaque d'ennemi
            if e.attackTimer == 0:
                ia.attackIA(player,e,projectileList)
            else:
                e.attackTimer = max( 0, e.attackTimer - 1/16)
         else:
                map.theMap.regionList[ player.position[0] ].ennemiList(e).auratimer -= 1
        if map.theMap.regionList[ player.position[0] ].ennemiList(e).auratimer <= 0:
            map.theMap.regionList[ player.position[0] ].ennemiList(e).aura = ""
    #levelup de l'ennemi
    if player.levelup - (100*2**player.lvl) >= 0:
        player.levelup -= (100*2**player.lvl)
        player.lvl += 1
        player.pointbonus += 1
        player.hp = player.lvl * 100
    
    
    
    
    
    
    
    
    
    
    
    
    
    