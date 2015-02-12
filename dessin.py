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
import option as opt

SCR_WIDTH   = 20
SCR_HEIGHT  = 10

xOffset = 0
yOffset = 0

sprites = {}

menuFont = None

overlayBack = None
overlayFront = None

def initDraw(fenetre):
    #taille de l'écran
    global SCR_WIDTH , SCR_HEIGHT
    
    SCR_WIDTH  = fenetre.get_width()  / opt.SPRITE_SIZE
    SCR_HEIGHT = fenetre.get_height() / opt.SPRITE_SIZE
    
    #polices
    menuFont = pygame.font.Font(None,32)
    
    #écran overlay
    global overlayBack , overlayFront
    
    overlayBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    overlayBack.fill( (128,128,128) )
    overlayBack.set_alpha(128)

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
    sprites["plancher"]   = getLoaded("beton.png")
    sprites["joueur"]     = getLoaded("perso.png")
    #sprites["pause"]      = getLoaded("pause.png")
    
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

def drawOverlay(fenetre):
    fenetre.blit( overlayBack , (0,0) )
    
    #fenetre.blit( sprites["pause"] , (int(SCR_WIDTH*opt.SPRITE_SIZE/2)- 100 , 100 ) )

#dessine une région entière
def drawRegion(fenetre,regionName):
    #recupère le tableau
    region = map.theMap.regionList[regionName]
    #dessine les sols
    for x in range( region.width ):
        for y in range( region.height ):
            drawCase(fenetre,region,x,y)

#dessine un sprite seul d'une case
def drawCase(fenetre,region,x,y):
    xEcran = x * opt.SPRITE_SIZE  + xOffset
    yEcran = y * opt.SPRITE_SIZE  + yOffset
    
    #sols
    if region.at(x,y) == 1:
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