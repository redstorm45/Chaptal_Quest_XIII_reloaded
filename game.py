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
import son
import random
import inventaire
import boss



#defini un joueur
player = joueur.Joueur(4,4)

#liste des projectiles
projectileList = []

#liste des ennemis
ennemiList = []

#inventaire ouvert et affiché
inventaireOuvert = False

#dialogue
dialogueActif = [None,""]

#fin du jeu
gameOver = False

#initialisation du jeu
def init():
    global ennemiList
    global BossList
    
    #création des ennemis sur la map
    for k in map.theMap.regionList.keys():
        r = map.theMap.regionList[k]
        for e in r.ennemiBaseList:
            type,posX,posY = e
            r.ennemiList.append( ennemi.typesEnnemis[type].copyAt( (r.name,posX,posY) ) )
        for e in r.PNGbaseList:
            type,posX,posY = e
            r.PNGlist.append( PNG.PNG(type,(posX,posY)))
        for e in r.BossbaseList:
            type,posX,posY = e
            r.BossList.append(boss.boss(type,posX,posY))
    
    dessin.initInterface(quete.listeQuetesActives)
    
    #initialisation de la liste d'ennemi
    ennemiList = map.theMap.regionList[ player.position[0] ].ennemiList[:]
    BossList = map.theMap.regionList[ player.position[0] ].BossList[:]
    
    #musique de la région
    if player.position[0] == "cours/E":
        son.playMusique("maccarena")
    elif player.position[0] == "salle/E.1":
        son.playMusique("zen")
    
    #fin du jeu
    global gameOver
    gameOver = False

#décharge les ennemis des maps
def quit():
    global ennemiList
    
    ennemiList = []
    for k in map.theMap.regionList.keys():
        r = map.theMap.regionList[k]
        r.ennemiList = []
        r.PNGlist = []

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
        
    for b in BossList:
        dessin.drawPlayer(fenetre,b)
                
    if player.attackanim > 0:
        dessin.animAttack(fenetre,player)    
        player.attackanim -=1
        
    if player.spriteCapacite != '' and player.spriteCapaciteTimer >0:
        dessin.drawCapacite(player,fenetre)
    
    for s,l,o in dessin.interfaceDrops:
        posX = (fenetre.get_width()-s.get_width())//2
        posY = (fenetre.get_height()-s.get_height())//2-o
        fenetre.blit(s,(posX,posY))
    
    dessin.drawATH(fenetre,player)
    if dessin.interfaceQueteOn:
        dessin.drawInterface(fenetre)
    
    if dialogueActif[0]:
        dessin.drawDialogue(fenetre)
    
    #inventaire
    if inventaireOuvert:
        dessin.drawInventaire(player,fenetre)

#touches de mouvement
def actionKeys(listPressed):
    global player,ennemiList,projectileList,BossList
    
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
        if t[0].dest[0] == "cours/E":
            son.playMusique("maccarena")
        elif t[0].dest[0] == "salle/E.1":
            son.playMusique("zen")
        else:
            son.playMusique("pirate")
        player.position = t[0].dest[:]
        #récupère les ennemis de la nouvelle région
        ennemiList = map.theMap.regionList[ player.position[0] ].ennemiList[:]
        for e in ennemiList:
            if e.hp <= 0:
                ennemiList.remove(e)
        BossList = map.theMap.regionList[ player.position[0] ].BossList[:]
        for b in BossList:
            if b.hp <= 0:
                BossList.remove(b)
        projectileList = []
        if opt.debugMode:
            print("teleport2",player.position)
    
    #test de completion de quete de position
    modif = False
    
    for q in quete.listeQuetesActives:
        if q.trouvee and q.objType == 1 and not q.completed:
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
            attackJoueur.attack(player,map.theMap.regionList[player.position[0]].ennemiList,map.theMap.regionList[player.position[0]].BossList)
            player.attackTimer = 1
            player.attackanim  = 0.2*60
        else:
            player.attackTimer = max( 0, player.attackTimer - 1/16)
    
    #sort
    if keybinding.isKeyActive( "SORT1" , listPressed ) and player.capacite1timer == 0 and player.capacite1Lvl > 0:
        capacite.capacite('RLC',player,map.theMap.regionList[player.position[0]].ennemiList,map.theMap.regionList[player.position[0]].BossList)
        player.capacite1timer = player.capacite1timer + 60*3
    elif keybinding.isKeyActive( "SORT2" , listPressed ) and player.capacite2timer == 0 and player.capacite1Lvl > 0:
        capacite.capacite('PFS',player,map.theMap.regionList[player.position[0]].ennemiList,map.theMap.regionList[player.position[0]].BossList)
        player.capacite2timer = player.capacite2timer + 60*3
    elif keybinding.isKeyActive( "ULTI" , listPressed ) and player.ULTITimer == 0 and player.ULTILvl > 0:
        capacite.capacite('Laplace',player,map.theMap.regionList[player.position[0]].ennemiList,map.theMap.regionList[player.position[0]].BossList)
        player.ULTITimer = player.ULTITimer + 60*10
        
    if player.capacite1timer > 0:
        player.capacite1timer -= 1
    if player.capacite2timer > 0:
        player.capacite2timer -= 1
    if player.ULTITimer > 0:
        player.ULTITimer -= 1

#appui sur une touche
def keyPress(key):
    global inventaireOuvert
    if key in keybinding.keys["QUETES"]:
        dessin.interfaceQueteOn = not dessin.interfaceQueteOn
    elif key in keybinding.keys["DIALOGUE"]:
        findPNG()
    elif key in keybinding.keys["INVENTAIRE"]:
        inventaireOuvert = not inventaireOuvert
    if key in keybinding.keys["UPSORT1"] and player.pointbonus > 0:
        player.capacite1Lvl += 1
        player.pointbonus -=1
    elif key in keybinding.keys["UPSORT2"] and player.pointbonus > 0:
        player.capacite2Lvl += 1
        player.pointbonus -=1
    elif key in keybinding.keys["UPSORT3"] and player.pointbonus > 0:
        player.capacite3Lvl += 1
        player.pointbonus -=1
    elif key in keybinding.keys["ULTIUP"] and player.pointbonus > 0 and (player.lvl-1)%5 == 0 and player.lvl > 5:
        player.ULTILvl += 1
        player.pointbonus -=1
    
#trouve un pnj à proximité et le fait parler
def findPNG():
    global dialogueActif
    region = map.theMap.regionList[player.position[0]]
    px , py = player.position[1] , player.position[2]
    
    trouve = False
    for p in region.PNGlist:
        if (px-p.position[0])**2 + (py-p.position[1])**2 < 2 ** 2:
            if p == dialogueActif[0]:
                dialogueActif = [p,p.getNextId(dialogueActif[1])]
            else:
                dialogueActif = [p,p.getNextId()]
            txt = p.name+": "+p.getText(dialogueActif[1])
            dessin.interfaceDialoguePNJ.updateTexte(txt)
            trouve = True
    if not trouve:
        dialogueActif = [None,""]

#supprime un ennemi, et gère le reste
def mortEnnemi(ennemi):
    #tue l'ennemi
    son.play("mort")
    ennemiList.remove(ennemi)
    player.levelup += ennemi.exp
    #check quêtes
    for q in quete.listeQuetesActives:
        if q.trouvee and q.objType == 3 and not q.completed:
            if ennemi.name in q.data["target"].keys():
                q.data["current"][ennemi.name] += 1
                q.checkCompleted()
    #génère des drops
    drops = []
    for k in ennemi.drops.keys():
        obj = inventaire.objet(k)
        #nombre d'objets:
        nbObj = 0
        if ennemi.drops[k] <= 1:
            if random.random() < ennemi.drops[k]:
                nbObj = 1
        else:
            nbObj = random.randint(0,ennemi.drops[k])
        
        if nbObj >= 1:
            if nbObj > 1:
                obj.stackSize = nbObj
            drops.append(obj)
    for d in drops:
        player.inventaire.add(d)
    dessin.addTooltipDrop(drops)
    
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
    
    #mort joueur
    if player.hp < 0:
        global gameOver
        gameOver = True
    
    #pnj
    for p in map.theMap.regionList[player.position[0]].PNGlist:
        p.spriteTimer += 0.1
    
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
            mortEnnemi(e)
        
        if e.aura == 'Laplace':
            e.hp -= 0.1/60 * 100*e.lvl
        
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
        
        
    if modifQuete:
        quete.refreshActive()
        dessin.reloadInterface(quete.listeQuetesActives)
        for q in quete.listeQuetesActives:
            q.changed = False
    
    
    #boss
    for b in BossList:
        
        if ia.agro(player.position,b):
            if b.aura == "": 
                #si le boss ne fait rien on declenche un patterne
                boss.patterne(b,player.position)
            if b.aura == "charge":
                if collision.checkJoueur(b,b.directionCharge[0],b.directionCharge[1]):  
                #on regarde si le boss peut avanver
                    b.position[1] += b.directionCharge[0]
                    b.position[2] += b.directionCharge[1]
                    b.anim += 0.25
                    
                else:                                                                   
                #s'il ne peut pas il est stun
                    b.aura = "stun"
                    b.auratimer = 60*3
                    
                    
                if collision.checkCharge(b,player):                      
                 #on regarde si le boss rencontre le joueur
                    player.hp -= b.damage
                    player.aura= "stun"
                    player.auratimer = 60
                    b.aura = ""    
                    #on arrete la charge du boss
                
            elif b.aura == "stun":
                if b.auratimer > 0:
                    b.auratimer -= 1
                else:
                    b.aura = ""
                    b.auratimer = 0 
            elif b.aura == "ATT":
                if b.auratimer == 180:
                    projectileList.append(projectile.Projectile(b,player,player.position))
                elif b.auratimer > 0:
                    b.auratimer -= 1
                else:
                    b.aura = ""
            elif b.aura == "triple":
                if b.auratimer == 180:
                    projectile.tripleprojectile(b,player,projectileList)
                elif b.auratimer > 0:
                    b.auratimer -= 1
                else:
                    b.aura = ""
            
        
    #levelup du joueur
    if player.levelup - (100*2**player.lvl) >= 0:
        player.levelup -= (100*2**player.lvl)
        player.lvl += 1
        player.pointbonus += 1
        player.hp = player.lvl * 100
        player.surfLvl = dessin.buttonFontXXS.render( str(player.lvl) , True , (0,0,255) )
        
    #tooltip interface
    for i in range(len(dessin.interfaceDrops)):
        t = dessin.interfaceDrops[i]
        [surf,life,offset] = t
        dessin.interfaceDrops[i][1] -= 1
        if life> 0:
            dessin.interfaceDrops[i][2]+=1
    
    for t in dessin.interfaceDrops:
        if t[1]<=0:
            dessin.interfaceDrops.remove(t)
    
    
    
    
    
    
    
    
    
    
    
    
    