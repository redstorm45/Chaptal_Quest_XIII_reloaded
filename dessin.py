import map
from os import chdir
import pygame

SPRITE_SIZE = 64

sprites = {}

def loadAllSprites():
    chdir("C:/Users/Pierre/Dropbox/Informatique/Projet/Chaptal_Quest_XIII_reloaded/sprites")
    sprites["mur"]={}
    sprites["mur"]["H"]  = pygame.image.load("mur_haut.bmp")
    sprites["mur"]["HG"] = pygame.image.load("mur_angle_gauche_haut.bmp")
    sprites["mur"]["G"]  = pygame.image.load("mur_gauche.bmp")
    sprites["mur"]["BG"] = pygame.image.load("mur_angle_gauche_bas.bmp")
    sprites["mur"]["B"]  = pygame.image.load("mur_bas.bmp")
    sprites["mur"]["BD"] = pygame.image.load("mur_angle_droite_bas.bmp")
    sprites["mur"]["D"]  = pygame.image.load("mur_droite.bmp")
    sprites["mur"]["HD"] = pygame.image.load("mur_angle_droite_haut.bmp")
    sprites["plancher"]  = pygame.image.load("plancher.bmp")
    sprites["joueur"]    = pygame.image.load("perso.png")
    

def drawRegion(fenetre,regionName):
    #recupère le tableau
    region = map.theMap.regionList[regionName]
    #dessine les sols
    for x in range( region.width ):
        for y in range( region.height ):
            drawCase(fenetre,region,x,y)

def drawCase(fenetre,region,x,y):
    xEcran = x * SPRITE_SIZE  + 200
    yEcran = y * SPRITE_SIZE  + 100
    
    if region.at(x,y) == 1:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
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

def drawPlayer(fenetre,player):
    x,y = player.position[1] , player.position[2]
    xEcran = (x-0.5) * SPRITE_SIZE  + 200
    yEcran = (y-0.5) * SPRITE_SIZE  + 100
    
    fenetre.blit(sprites["joueur"], (xEcran,yEcran))
    