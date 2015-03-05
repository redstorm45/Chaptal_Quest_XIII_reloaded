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
import mouse
import option
import debug
import save

#definition des différents états du jeu
ETAT_MENU     =  1  #menu
ETAT_GAME     =  2  #en jeu
ETAT_OVERLAY  =  3  #en jeu, avec overlay pour quitter,sauvegarder
ETAT_OVERLAY_Q = 4  #validation avant de quitter le jeu
ETAT_OVERLAY_M = 5  #validation avant de revenir au menu
ETAT_OPT      =  6  #ecran d'options
ETAT_NOUVEAU  =  7  #lancement de partie (selection de filière)

#crée la fenetre
pygame.init()
if option.debugMode:
    fenetre = pygame.display.set_mode( (0,0) )
else:
    fenetre = pygame.display.set_mode( (0,0),FULLSCREEN )
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

while not pygame.display.get_init():
    pass

#charge la map
map.theMap = map.Map()

#charge les ennemis sur la map
game.init()

#initialise les boutons
mouse.init(fenetre.get_width(),fenetre.get_height())

#initialise l'affichage avec la taille de l'écran
dessin.loadAllSprites()
dessin.initDraw(fenetre)

#initialisation de l'horloge
clock = pygame.time.Clock()

#initialisation de l'état avant entrée dans la boucle
state = ETAT_MENU

#main loop
running = True
while running:
    #  ***  dessin  ***
    fenetre.fill( (0,0,0) )
    if state == ETAT_GAME:
        game.draw(fenetre)
    elif state == ETAT_MENU:
        dessin.drawMenu(fenetre)
    elif state == ETAT_NOUVEAU:
        dessin.drawNewGame(fenetre)
    elif state == ETAT_OVERLAY:
        game.draw(fenetre)
        dessin.drawOverlay(fenetre)
    elif state == ETAT_OVERLAY_Q:
        game.draw(fenetre)
        dessin.drawOverlay(fenetre)
        dessin.drawOverlayQuit(fenetre)
    elif state == ETAT_OVERLAY_M:
        game.draw(fenetre)
        dessin.drawOverlay(fenetre)
        dessin.drawOverlayMenu(fenetre)
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
                elif state == ETAT_OVERLAY:
                    state = ETAT_GAME
                else:
                    running = False
            if event.key == K_RETURN:
                if state == ETAT_OVERLAY:
                    state = ETAT_OVERLAY_M
            if event.key == K_a:
                pass
            """
            different deplacement
            """
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:#bouton gauche
                x,y = event.pos
                if state == ETAT_MENU:
                    b = mouse.getBoutonAt("menu",x,y)
                    if b:
                        if b.name == "quitter":
                            running = False
                        elif b.name == "nouveau":
                            state = ETAT_NOUVEAU
                elif state == ETAT_NOUVEAU:
                    save.create("test")
                    save.load("test",game.player)
                    state = ETAT_GAME
                elif state == ETAT_OVERLAY:
                    b = mouse.getBoutonAt("overlay",x,y)
                    if b:
                        if b.name == "quitter":
                            state = ETAT_OVERLAY_Q
                        elif b.name == "menu":
                            state = ETAT_OVERLAY_M
                        elif b.name == "sauvegarder":
                            save.save( game.player )
                elif state == ETAT_OVERLAY_Q:
                    b = mouse.getBoutonAt("overlayQ",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            running = False
                elif state == ETAT_OVERLAY_M:
                    b = mouse.getBoutonAt("overlayM",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            state = ETAT_MENU
                elif state == ETAT_GAME and option.debugMode:
                    debug.caseSel = list( debug.getCellAt(x,y) )
                    print("click en",debug.caseSel)
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