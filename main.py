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
import texte

#definition des différents états du jeu
ETAT_MENU      = 1  #menu
ETAT_GAME      = 2  #en jeu
ETAT_OVERLAY   = 3  #en jeu, avec overlay pour quitter,sauvegarder
ETAT_OVERLAY_Q = 4  #validation avant de quitter le jeu
ETAT_OVERLAY_M = 5  #validation avant de revenir au menu
ETAT_OPTION    = 6  #ecran d'options
ETAT_NOUVEAU   = 7  #lancement de partie (selection de filière)
ETAT_QUIT      = 8  #fin du programme

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

#charge les textes
texte.loadTextes()

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
    elif state == ETAT_QUIT:
        dessin.drawQuit(fenetre)
    pygame.display.flip()
    
    #  ***  evenements  ***
    for event in pygame.event.get():
        #appui sur la croix
        if event.type == QUIT:
            if state == ETAT_QUIT:
                running = False
            else:
                state = ETAT_QUIT
        #appui sur une touche
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if state in [ETAT_GAME,ETAT_OVERLAY_M,ETAT_OVERLAY_Q]:
                    state = ETAT_OVERLAY
                elif state == ETAT_OVERLAY:
                    dessin.overlaySaved = False
                    state = ETAT_GAME
                elif state == ETAT_MENU:
                    state = ETAT_QUIT
                elif state in [ETAT_NOUVEAU,ETAT_OPTION]:
                    state = ETAT_MENU
                elif state == ETAT_QUIT:
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
                            state = ETAT_QUIT
                        elif b.name == "nouveau":
                            state = ETAT_NOUVEAU
                        elif b.name == "option":
                            state = ETAT_OPTION
                elif state == ETAT_NOUVEAU:
                    b = mouse.getBoutonAt("nouveau",x,y)
                    if b:
                        if b.name == "PTSI":
                            dessin.newGameSelectedInfo = "PTSI"
                        elif b.name == "PCSI":
                            dessin.newGameSelectedInfo = "PCSI"
                        elif b.name == "MPSI":
                            dessin.newGameSelectedInfo = "MPSI"
                        elif b.name == "commencer":
                            game.player.classe = dessin.newGameSelectedInfo
                            save.create("test")
                            save.load("test",game.player)
                            dessin.overlaySaved = False
                            state = ETAT_GAME
                elif state == ETAT_OVERLAY:
                    b = mouse.getBoutonAt("overlay",x,y)
                    if b:
                        if b.name == "quitter":
                            if dessin.overlaySaved:
                                state = ETAT_QUIT
                            else:
                                state = ETAT_OVERLAY_Q
                        elif b.name == "menu":
                            if dessin.overlaySaved:
                                state = ETAT_MENU
                            else:
                                state = ETAT_OVERLAY_M
                        elif b.name == "sauvegarder" and not dessin.overlaySaved:
                            save.save( game.player )
                            dessin.overlaySaved = True
                elif state == ETAT_OVERLAY_Q:
                    b = mouse.getBoutonAt("overlayQ",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            state = ETAT_QUIT
                elif state == ETAT_OVERLAY_M:
                    b = mouse.getBoutonAt("overlayM",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            state = ETAT_MENU
                elif state == ETAT_QUIT:
                    running = False
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