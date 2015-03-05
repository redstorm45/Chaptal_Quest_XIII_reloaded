"""

Fichier de gestion du dessin et des sprites

à faire:
  - augmenter le nombre de sprites
  - ajouter le scrolling de map, pour ne dessiner les sprites que de
    quelques cases plus loins que la taille de l'écran
    
"""

import map
import ennemi
import os
import pygame
import mouse
import option
import debug
import option as opt

SCR_WIDTH   = 20   #largeur de l'écran (en termes de nombre de cases)
SCR_HEIGHT  = 10   #hauteur de l'écran

xOffset = 0
yOffset = 0

sprites = {}

#polices
menuFont = None
buttonFontS = None
buttonFontM = None
buttonFontL = None

#surfaces du menu
menuBack = None
menuTitle = None
menuButtons = {}

#surfaces de l'overlay en jeu
overlayBack = None
overlayTitle = None
overlayButtons = {}

#surface de validation de quitter
overlayQuit = None

#surface de validation de retour au menu
overlayMenu = None

#surfaces de l'écran de nouvelle partie
newGameBack = None

def initDraw(fenetre):
    #taille de l'écran
    global SCR_WIDTH , SCR_HEIGHT
    
    SCR_WIDTH  = fenetre.get_width()  / opt.SPRITE_SIZE
    SCR_HEIGHT = fenetre.get_height() / opt.SPRITE_SIZE
    
    #polices
    global menuFont,buttonFontS,buttonFontM,buttonFontL
    menuFont = pygame.font.SysFont("vinerhanditc",120)
    buttonFontS = pygame.font.SysFont("chillernormal",72)
    buttonFontM = pygame.font.SysFont("chillernormal",92)
    buttonFontL = pygame.font.SysFont("chillernormal",120)
    
    #écran overlay
    global overlayBack , overlayTitle , overlayButtons
    
    overlayBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    overlayBack.fill( (128,128,128) )
    overlayBack.set_alpha(150)
    
    overlayTitle = menuFont.render("PAUSE",True,(250,20,20))
    
    overlayButtons = mouse.boutons["overlay"]
    overlayButtons["quitter"].surf     = buttonFontM.render("Quitter"     ,True,(20,20,20))
    overlayButtons["menu"].surf        = buttonFontM.render("Menu"        ,True,(20,20,20))
    overlayButtons["sauvegarder"].surf = buttonFontM.render("Sauvegarder" ,True,(20,20,20))
    
    #validation de quittage de l'overlay et du jeu
    global overlayQuit
    overlayQuit = pygame.Surface( ( max( fenetre.get_width()//1.5 , 900 ), max( fenetre.get_height()//2, 300) ) )
    overlayQuit.fill( (230,230,230) )
    textOverlayQuit = renderMultiLine(buttonFontS,"Êtes-vous sûr de vouloir quitter?\nLes changements non sauvegardés\nseront perdus\nOUI            NON",30,(10,10,10),(230,230,230))
    xPos = (overlayQuit.get_width()-textOverlayQuit.get_width())//2
    yPos = (overlayQuit.get_height()-textOverlayQuit.get_height())//2
    overlayQuit.blit( textOverlayQuit, (xPos,yPos) )
    
    #validation de quittage de l'overlay vers le menu
    global overlayMenu
    overlayMenu = pygame.Surface( ( max( fenetre.get_width()//1.5 , 900 ), max( fenetre.get_height()//2, 300) ) )
    overlayMenu.fill( (230,230,230) )
    textOverlayMenu = renderMultiLine(buttonFontS,"Êtes-vous sûr de vouloir retourner au menu?\nLes changements non sauvegardés\nseront perdus\nOUI            NON",30,(10,10,10),(230,230,230))
    xPos = (overlayMenu.get_width()-textOverlayMenu.get_width())//2
    yPos = (overlayMenu.get_height()-textOverlayMenu.get_height())//2
    overlayMenu.blit( textOverlayMenu, (xPos,yPos) )
    
    #écran de menu
    global menuBack , menuTitle , menuButtons
    menuBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    menuBack.fill( (0,0,0) )
    
    menuTitle = menuFont.render("MENU",True,(250,20,20))
    
    menuButtons = mouse.boutons["menu"]
    menuButtons["quitter"].surf = buttonFontM.render("Quitter" ,True,(240,240,240))
    menuButtons["nouveau"].surf = buttonFontM.render("Nouveau" ,True,(240,240,240))
    menuButtons["charger"].surf = buttonFontM.render("Charger" ,True,(240,240,240))
    
    #écran de nouveau jeu
    global newGameBack
    newGameBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    newGameBack.fill( (0,0,0) )

#dessine un texte sur plusieurs lignes
def renderMultiLine(font,text,spacing,color,backColor):
    #crée les différentes surfaces
    lines = text.split("\n")
    surfaces = []
    totHeight,maxWidth = 0,0
    for t in lines:
        s = font.render(t,True,color)
        totHeight += s.get_height()
        maxWidth = max( maxWidth,s.get_width() )
        surfaces.append(s)
    #blitte les surfaces sur une seule surface commune
    totSurf = pygame.Surface( (maxWidth,totHeight+(len(lines)-1)*spacing) )
    totSurf.fill(backColor)
    h = 0
    for s in surfaces:
        totSurf.blit( s , ( (maxWidth-s.get_width())//2 , h ) )
        h += s.get_height()+spacing
    return totSurf

#charge un sprite seul
def getLoaded(name):
    s = pygame.image.load("sprites/"+name).convert()
    s.set_colorkey((255,255,255))
    return s

#charge les sprites animés d'un personnage
def loadAnimSprite(spriteName):
    sprite = []
    sprited , spriteg = [] , []
    for i in range(8):
        sprited.append(getLoaded(spriteName + "D" + str(i)+".png"))
        spriteg.append(getLoaded(spriteName + "G" + str(i)+".png"))
        sprite.append(getLoaded(spriteName + str(i+1)+".png"))
    sprites[spriteName] = sprite
    sprites[spriteName + "D"] = sprited
    sprites[spriteName + "G"] = spriteg

#charge tous les sprites utilisés dans le jeu en mémoire
def loadAllSprites():
    sprites["mur"]={}
    sprites["mur"]["H"]   = getLoaded("mur_haut.bmp")
    sprites["mur"]["HG"]  = getLoaded("mur_angle_gauche_haut.bmp")
    sprites["mur"]["HG2"] = getLoaded("mur_angle2_gauche_haut.bmp")
    sprites["mur"]["G"]   = getLoaded("mur_gauche.bmp")
    sprites["mur"]["BG"]  = getLoaded("mur_angle_gauche_bas.bmp")
    sprites["mur"]["BG2"] = getLoaded("mur_angle2_gauche_bas.bmp")
    sprites["mur"]["B"]   = getLoaded("mur_bas.bmp")
    sprites["mur"]["BD"]  = getLoaded("mur_angle_droite_bas.bmp")
    sprites["mur"]["BD2"] = getLoaded("mur_angle2_droite_bas.bmp")
    sprites["mur"]["D"]   = getLoaded("mur_droite.bmp")
    sprites["mur"]["HD"]  = getLoaded("mur_angle_droite_haut.bmp")
    sprites["mur"]["HD2"] = getLoaded("mur_angle2_droite_haut.bmp")
    sprites["escalier"]={}
    #haut
    sprites["escalier"]["HG"]  = getLoaded("escalier_hautGauche.bmp")
    sprites["escalier"]["HM"]  = getLoaded("escalier_hautMilieu.bmp")
    sprites["escalier"]["HD"]  = getLoaded("escalier_hautDroite.bmp")
    sprites["escalier"]["H_D"] = getLoaded("escalier_fin_hautDroite.bmp")
    sprites["escalier"]["H_G"] = getLoaded("escalier_fin_hautGauche.bmp")
    sprites["escalier"]["H_M"] = getLoaded("escalier_fin_hautMilieu.bmp")
    #gauche
    sprites["escalier"]["GG"]  = getLoaded("escalier_gaucheGauche.bmp")
    sprites["escalier"]["GM"]  = getLoaded("escalier_gaucheMilieu.bmp")
    sprites["escalier"]["GD"]  = getLoaded("escalier_gaucheDroite.bmp")
    sprites["escalier"]["G_D"] = getLoaded("escalier_fin_gaucheDroite.bmp")
    sprites["escalier"]["G_G"] = getLoaded("escalier_fin_gaucheGauche.bmp")
    sprites["escalier"]["G_M"] = getLoaded("escalier_fin_gaucheMilieu.bmp")
    #bas
    sprites["escalier"]["BG"]  = getLoaded("escalier_basGauche.bmp")
    sprites["escalier"]["BM"]  = getLoaded("escalier_basMilieu.bmp")
    sprites["escalier"]["BD"]  = getLoaded("escalier_basDroite.bmp")
    sprites["escalier"]["B_D"] = getLoaded("escalier_fin_basDroite.bmp")
    sprites["escalier"]["B_G"] = getLoaded("escalier_fin_basGauche.bmp")
    sprites["escalier"]["B_M"] = getLoaded("escalier_fin_basMilieu.bmp")
    #droite
    sprites["escalier"]["DG"]  = getLoaded("escalier_droiteGauche.bmp")
    sprites["escalier"]["DM"]  = getLoaded("escalier_droiteMilieu.bmp")
    sprites["escalier"]["DD"]  = getLoaded("escalier_droiteDroite.bmp")
    sprites["escalier"]["D_D"] = getLoaded("escalier_fin_droiteDroite.bmp")
    sprites["escalier"]["D_G"] = getLoaded("escalier_fin_droiteGauche.bmp")
    sprites["escalier"]["D_M"] = getLoaded("escalier_fin_droiteMilieu.bmp")
    #tapis
    sprites["escalier"]["TH"]  = getLoaded("tapis_haut.bmp")
    sprites["escalier"]["TG"]  = getLoaded("tapis_gauche.bmp")
    sprites["escalier"]["TB"]  = getLoaded("tapis_bas.bmp")
    sprites["escalier"]["TD"]  = getLoaded("tapis_droite.bmp")
    sprites["escalier"]["TM"]  = getLoaded("tapis_milieu.bmp")
    
    sprites["escalier"]["mH"] = getLoaded("mur_escalier_haut.bmp")
    sprites["escalier"]["mG"] = getLoaded("mur_escalier_gauche.bmp")
    sprites["escalier"]["mB"] = getLoaded("mur_escalier_bas.bmp")
    sprites["escalier"]["mD"] = getLoaded("mur_escalier_droite.bmp")
    sprites["beton"]          = getLoaded("beton.png")
    sprites["plancher"]       = getLoaded("plancher.bmp")
    sprites["planche"]        = getLoaded("planche.bmp")
    
    loadAnimSprite( "gobelin" )
    
#gère le décalage de l'écran à partir de la position du joueur
def centerOffset(player):
    global xOffset
    global yOffset
    
    reg = map.theMap.regionList[ player.position[0] ]
    
    #centrage si taille supèrieure à celle de l'écran
    #selon x
    if SCR_WIDTH > reg.width:
        xOffset = (SCR_WIDTH - reg.width)*opt.SPRITE_SIZE/2
    else:
        xOffset = ((SCR_WIDTH /2) - player.position[1] )*opt.SPRITE_SIZE
        if reg.width - player.position[1] < (SCR_WIDTH /2):
            xOffset = -(reg.width-SCR_WIDTH)*opt.SPRITE_SIZE
        if player.position[1] < (SCR_WIDTH /2):
            xOffset = 0
            
    #selon y
    if SCR_HEIGHT > reg.height:
        yOffset = (SCR_HEIGHT - reg.height)*opt.SPRITE_SIZE/2
    else:
        yOffset = ((SCR_HEIGHT/2) - player.position[2] )*opt.SPRITE_SIZE
        if reg.height - player.position[2] < (SCR_HEIGHT /2):
            yOffset = -(reg.height-SCR_HEIGHT)*opt.SPRITE_SIZE
        if player.position[2] < (SCR_HEIGHT /2):
            yOffset = 0

def drawMenu(fenetre):
    fenetre.blit( menuBack , (0,0) )
    fenetre.blit( menuTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-menuTitle.get_width()/2),0) )
    for k in menuButtons.keys():
        fenetre.blit( menuButtons[k].surf , (menuButtons[k].pX , menuButtons[k].pY) )

def drawOverlay(fenetre):
    fenetre.blit( overlayBack , (0,0) )
    fenetre.blit( overlayTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-overlayTitle.get_width()/2),0) )
    for k in overlayButtons.keys():
        fenetre.blit( overlayButtons[k].surf , (overlayButtons[k].pX , overlayButtons[k].pY) )

def drawOverlayQuit(fenetre):
    xPos = (fenetre.get_width()-overlayQuit.get_width())//2
    yPos = (fenetre.get_height()-overlayQuit.get_height())//2
    fenetre.blit( overlayQuit , (xPos,yPos) )

def drawOverlayMenu(fenetre):
    xPos = (fenetre.get_width()-overlayMenu.get_width())//2
    yPos = (fenetre.get_height()-overlayMenu.get_height())//2
    fenetre.blit( overlayMenu , (xPos,yPos) )
    
def drawNewGame(fenetre):
    fenetre.blit( newGameBack, (0,0) )

#dessine une région entière
def drawRegion(fenetre,regionName):
    #recupère le tableau
    region = map.theMap.regionList[regionName]
    #dessine les sols
    for x in range( region.width ):
        for y in range( region.height ):
            drawCase(fenetre,region,x,y)
    #dessine la case selectionnée
    if option.debugMode and debug.caseSel != [-1,-1]:
        xEcran = debug.caseSel[0] * opt.SPRITE_SIZE  + xOffset
        yEcran = debug.caseSel[1] * opt.SPRITE_SIZE  + yOffset
        pygame.draw.rect( fenetre , (250,250,250) , (xEcran,yEcran,64,64) )

#dessine un sprite seul d'une case
def drawCase(fenetre,region,x,y):
    xEcran = x * opt.SPRITE_SIZE  + xOffset
    yEcran = y * opt.SPRITE_SIZE  + yOffset
    
    #sols
    if region.at(x,y) == 1:
        fenetre.blit(sprites["beton"] , (xEcran,yEcran))
    elif region.at(x,y) == 100:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
    #murs
    elif region.at(x,y) == 2:
        fenetre.blit(sprites["mur"]["H"] , (xEcran,yEcran))
    elif region.at(x,y) == 3:
        fenetre.blit(sprites["mur"]["HG"], (xEcran,yEcran))
    elif region.at(x,y) == 4:
        fenetre.blit(sprites["mur"]["G"] , (xEcran,yEcran))
    elif region.at(x,y) == 5:
        fenetre.blit(sprites["mur"]["BG"], (xEcran,yEcran))
    elif region.at(x,y) == 6:
        fenetre.blit(sprites["mur"]["B"] , (xEcran,yEcran))
    elif region.at(x,y) == 7:
        fenetre.blit(sprites["mur"]["BD"], (xEcran,yEcran))
    elif region.at(x,y) == 8:
        fenetre.blit(sprites["mur"]["D"] , (xEcran,yEcran))
    elif region.at(x,y) == 9:
        fenetre.blit(sprites["mur"]["HD"], (xEcran,yEcran))
    elif region.at(x,y) == 10:
        fenetre.blit(sprites["mur"]["HG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 11:
        fenetre.blit(sprites["mur"]["BG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 12:
        fenetre.blit(sprites["mur"]["BD2"] , (xEcran,yEcran))
    elif region.at(x,y) == 13:
        fenetre.blit(sprites["mur"]["HD2"] , (xEcran,yEcran))
    #murs d'escaliers
    elif region.at(x,y) == 14:
        fenetre.blit(sprites["escalier"]["mH"] , (xEcran,yEcran))
    elif region.at(x,y) == 15:
        fenetre.blit(sprites["escalier"]["mG"] , (xEcran,yEcran))
    elif region.at(x,y) == 16:
        fenetre.blit(sprites["escalier"]["mB"] , (xEcran,yEcran))
    elif region.at(x,y) == 17:
        fenetre.blit(sprites["escalier"]["mD"] , (xEcran,yEcran))
    #planche
    elif region.at(x,y) == 18:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["planche"] , (xEcran,yEcran))
    #tapis
    elif region.at(x,y) == 19:
        fenetre.blit(sprites["escalier"]["TM"] , (xEcran,yEcran))
    #escaliers haut
    elif region.at(x,y) == 20:
        fenetre.blit(sprites["escalier"]["HD"] , (xEcran,yEcran))
    elif region.at(x,y) == 21:
        fenetre.blit(sprites["escalier"]["HG"] , (xEcran,yEcran))
    elif region.at(x,y) == 22:
        fenetre.blit(sprites["escalier"]["HM"] , (xEcran,yEcran))
    elif region.at(x,y) == 23:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 24:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 25:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 26:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TH"] , (xEcran,yEcran))
    #escaliers gauche
    elif region.at(x,y) == 30:
        fenetre.blit(sprites["escalier"]["GD"] , (xEcran,yEcran))
    elif region.at(x,y) == 31:
        fenetre.blit(sprites["escalier"]["GG"] , (xEcran,yEcran))
    elif region.at(x,y) == 32:
        fenetre.blit(sprites["escalier"]["GM"] , (xEcran,yEcran))
    elif region.at(x,y) == 33:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 34:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 35:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 36:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TG"] , (xEcran,yEcran))
    #escaliers bas
    elif region.at(x,y) == 40:
        fenetre.blit(sprites["escalier"]["BD"] , (xEcran,yEcran))
    elif region.at(x,y) == 41:
        fenetre.blit(sprites["escalier"]["BG"] , (xEcran,yEcran))
    elif region.at(x,y) == 42:
        fenetre.blit(sprites["escalier"]["BM"] , (xEcran,yEcran))
    elif region.at(x,y) == 43:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 44:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 45:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 46:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TB"] , (xEcran,yEcran))
    #escaliers droite
    elif region.at(x,y) == 50:
        fenetre.blit(sprites["escalier"]["DD"] , (xEcran,yEcran))
    elif region.at(x,y) == 51:
        fenetre.blit(sprites["escalier"]["DG"] , (xEcran,yEcran))
    elif region.at(x,y) == 52:
        fenetre.blit(sprites["escalier"]["DM"] , (xEcran,yEcran))
    elif region.at(x,y) == 53:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 54:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 55:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 56:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TD"] , (xEcran,yEcran))

#dessine le sprite d'un object JoueurBase
def drawPlayer(fenetre,player):
    x,y = player.position[1] , player.position[2]
    xEcran = (x-0.5) * opt.SPRITE_SIZE  + xOffset
    yEcran = (y-0.5) * opt.SPRITE_SIZE  + yOffset
    
    if player.direction == 4:
        fenetre.blit(sprites[player.spriteName + "D"][int(player.anim)%8], (xEcran,yEcran))
    elif player.direction == 8:
        fenetre.blit(sprites[player.spriteName + "G"][int(player.anim)%8], (xEcran,yEcran))
    else:
        fenetre.blit(sprites[player.spriteName][player.direction-1], (xEcran,yEcran))
    
    #affiche la vie au dessus du sprite
    pygame.draw.rect( fenetre , (255,0,0) , (xEcran,yEcran-10,64,10) )
    pygame.draw.rect( fenetre , (0,255,0) , (xEcran,yEcran-10,64*player.hp/(100*player.lvl),10) )