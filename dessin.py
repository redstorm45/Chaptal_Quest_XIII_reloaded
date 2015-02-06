import map
import ennemi
import os
import pygame

SPRITE_SIZE = 64
SCR_WIDTH   = 20
SCR_HEIGHT  = 10

xOffset = 0
yOffset = 0

sprites = {}

#charge les sprites animés d'un personnage
def loadAnimSprite(spriteName):
    sprite = []
    for i in range(8):
        sprite.append(pygame.image.load(spriteName+str(i+1)+".png"))
    sprites[spriteName] = sprite

def loadAllSprites():
    workDir = os.getcwd()
    os.chdir(workDir+"/sprites")
    sprites["mur"]={}
    sprites["mur"]["H"]   = pygame.image.load("mur_haut.bmp")
    sprites["mur"]["HG"]  = pygame.image.load("mur_angle_gauche_haut.bmp")
    sprites["mur"]["HG2"] = pygame.image.load("mur_angle2_gauche_haut.bmp")
    sprites["mur"]["G"]   = pygame.image.load("mur_gauche.bmp")
    sprites["mur"]["BG"]  = pygame.image.load("mur_angle_gauche_bas.bmp")
    sprites["mur"]["BG2"] = pygame.image.load("mur_angle2_gauche_bas.bmp")
    sprites["mur"]["B"]   = pygame.image.load("mur_bas.bmp")
    sprites["mur"]["BD"]  = pygame.image.load("mur_angle_droite_bas.bmp")
    sprites["mur"]["BD2"] = pygame.image.load("mur_angle2_droite_bas.bmp")
    sprites["mur"]["D"]   = pygame.image.load("mur_droite.bmp")
    sprites["mur"]["HD"]  = pygame.image.load("mur_angle_droite_haut.bmp")
    sprites["mur"]["HD2"] = pygame.image.load("mur_angle2_droite_haut.bmp")
    sprites["plancher"]   = pygame.image.load("plancher.bmp")
    sprites["joueur"]     = pygame.image.load("perso.png")
    
    loadAnimSprite( "gobelin" )
    
    sprites["ennemi"]    = pygame.image.load("ennemi.png")
    
def centerOffset(player):
    global xOffset
    global yOffset
    
    reg = map.theMap.regionList[ player.position[0] ]
    
    xOffset = ((SCR_WIDTH /2) - player.position[1] )*SPRITE_SIZE
    yOffset = ((SCR_HEIGHT/2) - player.position[2] )*SPRITE_SIZE
    
    if reg.width - player.position[1] < (SCR_WIDTH /2):
        xOffset = -(reg.width-SCR_WIDTH)*SPRITE_SIZE
    if player.position[1] < (SCR_WIDTH /2):
        xOffset = 0
    if reg.height - player.position[2] < (SCR_HEIGHT /2):
        yOffset = -(reg.height-SCR_HEIGHT)*SPRITE_SIZE
    if player.position[2] < (SCR_HEIGHT /2):
        yOffset = 0
    


def drawRegion(fenetre,regionName):
    #recupère le tableau
    region = map.theMap.regionList[regionName]
    #dessine les sols
    fenetre.fill( (0,0,0) )
    for x in range( region.width ):
        for y in range( region.height ):
            drawCase(fenetre,region,x,y)

def drawCase(fenetre,region,x,y):
    xEcran = x * SPRITE_SIZE  + xOffset
    yEcran = y * SPRITE_SIZE  + yOffset
    
    if region.at(x,y) == 1:
        fenetre.blit(sprites["plancher"]   , (xEcran,yEcran))
    elif region.at(x,y) == 2:
        fenetre.blit(sprites["mur"]["H"]   , (xEcran,yEcran))
    elif region.at(x,y) == 3:
        fenetre.blit(sprites["mur"]["HG"]  , (xEcran,yEcran))
    elif region.at(x,y) == 4:
        fenetre.blit(sprites["mur"]["G"]   , (xEcran,yEcran))
    elif region.at(x,y) == 5:
        fenetre.blit(sprites["mur"]["BG"]  , (xEcran,yEcran))
    elif region.at(x,y) == 6:
        fenetre.blit(sprites["mur"]["B"]   , (xEcran,yEcran))
    elif region.at(x,y) == 7:
        fenetre.blit(sprites["mur"]["BD"]  , (xEcran,yEcran))
    elif region.at(x,y) == 8:
        fenetre.blit(sprites["mur"]["D"]   , (xEcran,yEcran))
    elif region.at(x,y) == 9:
        fenetre.blit(sprites["mur"]["HD"]  , (xEcran,yEcran))
    elif region.at(x,y) == 10:
        fenetre.blit(sprites["mur"]["HG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 11:
        fenetre.blit(sprites["mur"]["BG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 12:
        fenetre.blit(sprites["mur"]["BD2"] , (xEcran,yEcran))
    elif region.at(x,y) == 13:
        fenetre.blit(sprites["mur"]["HD2"] , (xEcran,yEcran))

def drawPlayer(fenetre,player):
    x,y = player.position[1] , player.position[2]
    xEcran = (x-0.5) * SPRITE_SIZE  + xOffset
    yEcran = (y-0.5) * SPRITE_SIZE  + yOffset
    
    fenetre.blit(sprites[player.spriteName][player.direction-1], (xEcran,yEcran))
    