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
import collision
import PNG

#defini un joueur
player = joueur.Joueur(4,4)

#liste des projectiles
projectileList = []

#liste des ennemis
ennemiList = []

#inventaire ouvert et affiché
inventaireOuvert = None

#initialisation du jeu
def init():
    global ennemiList
    
    #création des ennemis sur la map
    for k in map.theMap.regionList.keys():
        r = map.theMap.regionList[k]
        for e in r.ennemiBaseList:
            type,posX,posY = e
            r.ennemiList.append( ennemi.typesEnnemis[type].copyAt( (r.name,posX,posY) ) )
        for e in r.PNGbaseList:
            type,posX,posY = e
            r.PNGlist.append( PNG.PNG(type,(posX,posY)))
    #chargement des quêtes
    quete.loadQuetes()
    quete.refreshActive()
    
    dessin.initInterface(quete.listeQuetesActives)
    
    #initialisation de la liste d'ennemi
    ennemiList = map.theMap.regionList[ player.position[0] ].ennemiList[:]

#dessin de la scène
def draw(fenetre):
    global player
    
    regionAffichee = player.position[0]
    dessin.centerOffset(player)
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    dessin.drawXP(fenetre,player)
    for e in ennemiList:
        dessin.drawPlayer(fenetre,e)
        
    for p in projectileList:
        dessin.drawProjectile(fenetre,p)
        
    if player.attackanim > 0:
        dessin.animAttack(fenetre,player)    
        player.attackanim -=1
        
    if player.spriteCapacite != '' and player.spriteCapaciteTimer >0:
        dessin.drawCapacite(player,fenetre)
    
    if dessin.interfaceQueteOn:
        dessin.drawInterface(fenetre)
    dessin.drawATH(fenetre,player)
#touches de mouvement
def actionKeys(listPressed):
    global player,ennemiList,projectileList
    
    #mouvement du joueur
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
        
    #test de teleportation
    t = map.theMap.regionList[ player.position[0] ].eventAt( player.position[1],player.position[2],"teleport" )
    if t:
        #supprime les ennemis tués
        map.theMap.regionList[ player.position[0] ].ennemiList = ennemiList[:]
        if opt.debugMode:
            print("teleport",player.position)
        #change de region
        player.position = t[0].dest[:]
        #récupère les ennemis de la nouvelle région
        ennemiList = map.theMap.regionList[ player.position[0] ].ennemiList[:]
        for e in ennemiList:
            if e.hp <= 0:
                ennemiList.remove(e)
        projectileList = []
        if opt.debugMode:
            print("teleport2",player.position)
    
    #test de completion de quete de position
    modif = False
    
    for q in quete.listeQuetesActives:
        if q.trouvee and q.objType == 1:
            q.checkCompleted( player )
            if q.changed:
                modif = True
    if modif:
        quete.refreshActive()
        dessin.reloadInterface(quete.listeQuetesActives)
        for q in quete.listeQuetesActives:
            q.changed = False
    
    #attaque
    if keybinding.isKeyActive( "ATTACK" , listPressed ):
        if player.attackTimer == 0:
            attackJoueur.attack(player,map.theMap.regionList[player.position[0]].ennemiList)
            player.attackTimer = 1
            player.attackanim  = 0.2*60
        else:
            player.attackTimer = max( 0, player.attackTimer - 1/16)
    
    #sort
    if keybinding.isKeyActive( "SORT1" , listPressed ) and player.capacite1timer == 0 and player.capacite1Lvl > 0:
        capacite.capacite('RLC',player,map.theMap.regionList[player.position[0]].ennemiList)
        player.capacite1timer = player.capacite1timer + 60*3
    elif keybinding.isKeyActive( "SORT2" , listPressed ) and player.capacite2timer == 0 and player.capacite1Lvl > 0:
        capacite.capacite('PFS',player,map.theMap.regionList[player.position[0]].ennemiList)
        player.capacite2timer = player.capacite2timer + 60*3
    elif keybinding.isKeyActive( "ULTI" , listPressed ) and player.ULTITimer == 0 and player.ULTILvl > 0:
        capacite.capacite('Laplace',player,map.theMap.regionList[player.position[0]].ennemiList)
        player.ULTITimer = player.ULTITimer + 60*3
    
    if keybinding.isKeyActive( "UPSORT1" , listPressed ) and player.pointbonus > 0:
        player.capacite1Lvl += 1
        player.pointbonus -=1
    elif keybinding.isKeyActive( "UPSORT2" , listPressed ) and player.pointbonus > 0:
        player.capacite2Lvl += 1
        player.pointbonus -=1
    elif keybinding.isKeyActive( "UPSORT3" , listPressed ) and player.pointbonus > 0:
        player.capacite3Lvl += 1
        player.pointbonus -=1
    elif keybinding.isKeyActive( "ULTI" , listPressed ) and player.pointbonus > 0 and player.lvl/2 - player.ULTILvl-1 > 0:
        player.ULTILvl += 1
        player.pointbonus -=1
        
    if player.capacite1timer > 0:
        player.capacite1timer -= 1
    if player.capacite2timer > 0:
        player.capacite2timer -= 1
    if player.ULTITimer > 0:
        player.ULTITimer -= 1

def findPNG():
    region = map.theMap.regionList[player.position[0]]
    px , py = player.position[1] , player.position[2]
    
    for p in region.PNGlist:
        if (px-p.position[0])**2 + (py-p.position[1])**2 < 2 ** 2:
            print(p.name+":")
            print(p.texte)

#evenement de mise à jour (ia et animations)    
def tick():
    player.anim += 0.25
    if player.hp < player.lvl*100 and player.combat <= 0:
        player.hp += 0.1*player.lvl
    if player.combat > 0 and player.hp < player.lvl*100:
        player.hp += 0*player.lvl
    if player.combat > 0:
        player.combat -= 1
    if player.spriteCapaciteTimer > 0:
        player.spriteCapaciteTimer -= 1
    
    #avancement de projectiles
    for p in projectileList:
        p.avancer()
        
        if p.life < 0:
            projectileList.remove(p)
        elif isinstance(p.cible,joueur.Joueur):
                if collision.checkProjectile(p,player):
                    player.hp -= p.tireur.dammage
                    projectileList.remove(p)
                    player.combat = 3*60
    
    #IA
    modifQuete = False
    for e in ennemiList:
        #mort d'un ennemi
        if e.hp < 0:
            ennemiList.remove(e)
            player.levelup += e.exp
            for q in quete.listeQuetesActives:
                if q.trouvee and q.objType == 3:
                    if e.name in q.data["target"].keys():
                        q.data["current"][e.name] += 1
                        q.checkCompleted()
        
        
        
        if e.aura == 'Laplace':
            e.hp -= 0.1/60 * 100*2**e.lvl
            
        
        
        
        elif e.aura != "stun":
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
            e.auratimer -= 1
        if e.auratimer <= 0:
            e.aura = ""
        
        print(e.armure)
    if modifQuete:
        quete.refreshActive()
        dessin.reloadInterface(quete.listeQuetesActives)
        for q in quete.listeQuetesActives:
            q.changed = False
        
    #levelup du joueur
    if player.levelup - (100*2**player.lvl) >= 0:
        player.levelup -= (100*2**player.lvl)
        player.lvl += 1
        player.pointbonus += 1
        player.hp = player.lvl * 100
        player.surfLvl = dessin.buttonFontXXS.render( str(player.lvl) , True , (0,0,255) )
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    