"""

Fichier principal du programme
Il gère les évènements, et la fenêtre

"""

import pygame
from pygame.locals import *

import map
import dessin
import game
import math
import keybinding

#definition des différents états du jeu
ETAT_MENU    =  1  #menu
ETAT_GAME    =  2  #en jeu
ETAT_OVERLAY =  3  #en jeu, avec overlay pour quitter,sauvegarder
ETAT_OPT     =  4  #ecran d'options

#crée la fenetre
pygame.init()
fenetre = pygame.display.set_mode( (0,0) ) #add ", FULLSCREEN" argument for fullscreen mode
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

while not pygame.display.get_init():
    pass

#charge la map
map.theMap = map.map()

#charge les ennemis sur la map
game.init()

#initialise l'affichage avec la taille de l'écran
dessin.loadAllSprites()
dessin.initDraw(fenetre)

#initialisation de l'horloge
clock = pygame.time.Clock()

#initialisation de l'état avant entrée dans la boucle
state = ETAT_GAME

#main loop
running = True
while running:
    #  ***  dessin  ***
    fenetre.fill( (0,0,0) )
    if state == ETAT_GAME:
        game.draw(fenetre)
    elif state == ETAT_OVERLAY:
        game.draw(fenetre)
        dessin.drawOverlay(fenetre)
    pygame.display.flip()
    
    #  ***  evenements  ***
    for event in pygame.event.get():
        #quitte le programme
        if event.type == QUIT:
            running = False
        #appui sur une touche
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if state == ETAT_GAME:
                    state = ETAT_OVERLAY
                else:
                    running = False
            if event.key == K_RETURN:
                if state == ETAT_OVERLAY:
                    state = ETAT_GAME
            if event.key == K_a:
                pass
            """
            different deplacement et capacité
            """
    #gestion des déplacements
    if state == ETAT_GAME:
        listPressed = pygame.key.get_pressed()
        game.actionKeys(listPressed)
    
    #  ***  update général  ***
    if state == ETAT_GAME:
        game.tick()
    #clock
    clock.tick(60)

pygame.quit()