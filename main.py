"""

Fichier principal du programme
Il gère les évènements, et la fenêtre


objectifs:

 avoir une séquence complète de jeu jouable
 (intro, + début de 1ère quête)

>ajouter des objets (sprites)
 utilisables, avec capacitées etc..(armes/obj spé...)

>ajouter la map nécéssaire

>faire un affichage de l'histoire

>optimiser les collisions et les ennemis (pour la jouabilitée)

>ajuster les dégats

ce qui n'est pas à faire:

 changer les sprites pour les rendres plus beau (trop de temps)

"""

import pygame
from pygame.locals import *

#modules systèmes
import math,string,ctypes

#modules du programme
#E/S
import dessin
import keybinding
import mouse
#données sous forme de variables
import map
import game
import quete
import option
#données à charger
import save
import texte
import son
import inventaire
#édition
import editGame


classe = "PTSI"


#definition des différents états du jeu
ETAT_MENU         = 1  #menu
ETAT_GAME         = 2  #en jeu
ETAT_OVERLAY      = 3  #en jeu, avec overlay pour quitter,sauvegarder
ETAT_OVERLAY_Q    = 4  #validation avant de quitter le jeu
ETAT_OVERLAY_M    = 5  #validation avant de revenir au menu
ETAT_OPTION       = 6  #ecran d'options
ETAT_NOUVEAU      = 7  #lancement de partie (selection de filière)
ETAT_NOUVEAU_FAIL = 8  #selection invalide (nom de sauvagarde déjà utilisé)
ETAT_CHARGE       = 9  #selection invalide (nom de sauvagarde déjà utilisé)
ETAT_QUIT         = 10 #fin du programme
ETAT_EDIT         = 11 #edition des niveaux

#trouve la vraie taille de l'écran
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
theScrWidth,theScrHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#crée la fenetre
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

if option.debugMode:
    fenetre = pygame.display.set_mode( (theScrWidth,theScrHeight) )
else:
    fenetre = pygame.display.set_mode( (theScrWidth,theScrHeight),FULLSCREEN )
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

#attend l'initialisation de pygame
while not pygame.display.get_init():
    pass

#charge la map
map.theMap = map.Map()

#charge les textes
texte.loadTextes()

#charge les musiques
son.init()

#initialise les boutons
mouse.init(fenetre.get_width(),fenetre.get_height())

#initialise l'affichage avec la taille de l'écran
dessin.loadAllSprites()     #charge tous les sprites
dessin.initDraw(fenetre)    #prédessine toutes les entitées
dessin.initMaps(map.theMap) #prédessine chaque région

#initialisation de l'horloge
clock = pygame.time.Clock()
fps = 60

#initialisation de l'état avant entrée dans la boucle
state = ETAT_MENU
if option.editMode:
    editGame.init()
    state = ETAT_EDIT

#démarre la musique!
son.playMusique("pirate")

#main loop
running = True
while running:
    #  ***  dessin  ***
    fenetre.fill( (0,0,0) )
    if state == ETAT_GAME:
        game.draw(fenetre)
    elif state == ETAT_EDIT:
        editGame.draw(fenetre)
    elif state == ETAT_MENU:
        dessin.drawMenu(fenetre)
    elif state == ETAT_OPTION:
        dessin.drawOption(fenetre)
    elif state == ETAT_NOUVEAU:
        dessin.drawNewGame(fenetre)
    elif state == ETAT_NOUVEAU_FAIL:
        dessin.drawNewGame(fenetre)
        dessin.drawOverlayFail(fenetre)
    elif state == ETAT_CHARGE:
        dessin.drawCharge(fenetre)
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
            elif option.debugMode:
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
                elif state == ETAT_NOUVEAU:
                    state = ETAT_MENU
                    dessin.newGameName.updateTexte("")
                elif state == ETAT_CHARGE:
                    state = ETAT_MENU
                elif state == ETAT_OPTION:
                    state = ETAT_MENU
                elif state == ETAT_EDIT:
                    editGame.saveChanges()
                elif state == ETAT_QUIT:
                    running = False
            elif event.key == K_RETURN:
                if state == ETAT_OVERLAY:
                    state = ETAT_OVERLAY_M
            elif event.key == pygame.K_BACKSPACE:
                if state == ETAT_NOUVEAU:
                    dessin.newGameName.appendTexte( "\b" )
                elif state == ETAT_CHARGE:
                    dessin.chargeName.appendTexte( "\b" )
            elif ( (event.unicode in string.ascii_lowercase) or (event.unicode in string.ascii_uppercase) ) and state in [ETAT_NOUVEAU,ETAT_CHARGE]:
                if state == ETAT_NOUVEAU:
                    dessin.newGameName.appendTexte( event.unicode )
                elif state == ETAT_CHARGE:
                    dessin.chargeName.appendTexte( event.unicode )
            elif state == ETAT_GAME:
                if event.key in keybinding.keys["QUETES"]:
                    dessin.interfaceQueteOn = not dessin.interfaceQueteOn
                elif event.key in keybinding.keys["DIALOGUE"]:
                    game.findPNG()
                elif event.key in keybinding.keys["INVENTAIRE"]:
                    game.inventaireOuvert = not game.inventaireOuvert
        #appui sur un bouton de souris
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
                        elif b.name == "charger":
                            dessin.initCharge(fenetre)
                            state = ETAT_CHARGE
                        elif b.name == "option":
                            state = ETAT_OPTION
                elif state == ETAT_NOUVEAU:
                    b = mouse.getBoutonAt("nouveau",x,y)
                    if b:
                        if b.name == "PTSI":
                            dessin.newGameSelectedInfo = "PTSI"
                            classe = "PTSI"
                        elif b.name == "PCSI":
                            dessin.newGameSelectedInfo = "PCSI"
                            classe = "PCSI"
                        elif b.name == "MPSI":
                            dessin.newGameSelectedInfo = "MPSI"
                            classe = "MPSI"
                        elif b.name == "commencer":
                            if option.debugSave:
                                game.player.classe = dessin.newGameSelectedInfo
                                save.create("debugSave_","PTSI")
                                save.load("debugSave_",game.player)
                                dessin.overlaySaved = False
                                #charge les ennemis sur la map
                                game.init()
                                state = ETAT_GAME
                                dessin.newGameName.updateTexte("")
                            elif dessin.newGameName.texte == "":
                                state = ETAT_NOUVEAU_FAIL
                            elif dessin.newGameName.texte in save.getAllNames():
                                state = ETAT_NOUVEAU_FAIL
                            else:
                                saveName = dessin.newGameName.texte
                                game.player.classe = dessin.newGameSelectedInfo
                                quete.loadQuetes()
                                save.create(saveName,classe)
                                save.load(saveName,game.player)
                                quete.refreshActive()
                                dessin.overlaySaved = False
                                #charge les ennemis sur la map
                                game.init()
                                state = ETAT_GAME
                                dessin.newGameName.updateTexte("")
                elif state == ETAT_CHARGE:
                    b = mouse.getBoutonAt("charger",x,y)
                    if b:
                        saveName = b.name
                        quete.loadQuetes()
                        save.load(saveName,game.player)
                        quete.refreshActive()
                        dessin.overlaySaved = False
                        #charge les ennemis sur la map
                        game.init()
                        state = ETAT_GAME
                elif state == ETAT_GAME:
                    for b in dessin.interfaceBoutonsQuetesAffiches:
                        if b.isInside(x,y):
                            dessin.setQueteEtendue(b.widgets[0].id)
                elif state == ETAT_OVERLAY:
                    b = mouse.getBoutonAt("overlay",x,y)
                    if b:
                        if b.name == "quitter":
                            if dessin.overlaySaved:
                                save.unload(game.joueur)
                                game.quit()
                                state = ETAT_QUIT
                            else:
                                state = ETAT_OVERLAY_Q
                        elif b.name == "menu":
                            if dessin.overlaySaved:
                                save.unload(game.joueur)
                                game.quit()
                                state = ETAT_MENU
                            else:
                                state = ETAT_OVERLAY_M
                        elif b.name == "sauvegarder" and not dessin.overlaySaved:
                            save.save( game.player )
                            dessin.overlaySaved = True
                elif state == ETAT_NOUVEAU_FAIL:
                    state = ETAT_NOUVEAU
                elif state == ETAT_OVERLAY_Q:
                    b = mouse.getBoutonAt("overlayV",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            state = ETAT_QUIT
                elif state == ETAT_OVERLAY_M:
                    b = mouse.getBoutonAt("overlayV",x,y)
                    if b:
                        if b.name == "non":
                            state = ETAT_OVERLAY
                        elif b.name == "oui":
                            state = ETAT_MENU
                elif state == ETAT_QUIT:
                    running = False
                elif state == ETAT_EDIT:
                    editGame.clickL(x,y)
            elif event.button == 2:#bouton molette
                x,y = event.pos
                if state == ETAT_EDIT:
                    editGame.clickMid(x,y)
            elif event.button == 3:#bouton droit
                x,y = event.pos
                if state == ETAT_EDIT:
                    editGame.clickR(x,y)
            elif event.button == 4:#molette vers le haut
                if state == ETAT_EDIT:
                    editGame.mouseWheel(1)
            elif event.button == 5:#molette vers le bas
                if state == ETAT_EDIT:
                    editGame.mouseWheel(-1)
    #gestion des déplacements
    if state == ETAT_GAME:
        listPressed = pygame.key.get_pressed()
        game.actionKeys(listPressed)
    elif state == ETAT_EDIT:
        listPressed = pygame.key.get_pressed()
        editGame.actionKeys(listPressed)
    
    #  ***  update général  ***
    if state == ETAT_GAME:
        game.tick()
    #clock
    fps = clock.tick(60)

#arrêt du programme
son.stop()
pygame.mixer.quit()
pygame.quit()
