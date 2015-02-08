"""

Fichier principal du programme
Il gère les évènements, et la fenêtre

"""

import pygame
from pygame.locals import *

import map
import dessin
import joueur
import ennemi
import math
import ia
import attackJoueur
import keybinding


#defini un joueur et ennemi
player = joueur.Joueur(2,2)
listEnnemis = []

#vitesse du déplacement
speed = 1/16
speedDiag = speed

#crée la fenetre
fenetre = pygame.display.set_mode( (0,0)  ) #add ", FULLSCREEN" argument for fullscreen mode
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

while not pygame.display.get_init():
    pass

#initialise l'affichage avec la taille de l'écran
dessin.SCR_WIDTH  = fenetre.get_width()  / dessin.SPRITE_SIZE
dessin.SCR_HEIGHT = fenetre.get_height() / dessin.SPRITE_SIZE

#charge la map
map.theMap = map.map()

#charge les sprites
dessin.loadAllSprites()

#initialisation de l'horloge
clock = pygame.time.Clock()

#main loop
running = True
while running:
    #dessin
    regionAffichee = player.position[0]
    dessin.centerOffset(player)
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    for e in listEnnemis:
        dessin.drawPlayer(fenetre,e)
    pygame.display.flip()
    #"evenements
    for event in pygame.event.get():
        #quitte le programme
        if event.type == QUIT:
            running = False
        #appui sur une touche
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_a:
                pass
        """
        different deplacement et capacité
        """
    #gestion des déplacements
    listPressed = pygame.key.get_pressed()
    if keybinding.areKeysActive(["LEFT","UP"],listPressed):
        player.mouvement( -speedDiag , -speedDiag )
    elif keybinding.areKeysActive(["LEFT","DOWN"],listPressed):
        player.mouvement( -speedDiag ,  speedDiag )
    elif keybinding.areKeysActive(["RIGHT","DOWN"],listPressed):
        player.mouvement(  speedDiag ,  speedDiag )
    elif keybinding.areKeysActive(["RIGHT","UP"],listPressed):
        player.mouvement(  speedDiag , -speedDiag )
    elif keybinding.isKeyActive( "LEFT" , listPressed ):
        player.mouvement( -speed , 0 )
    elif keybinding.isKeyActive( "DOWN" , listPressed ):
        player.mouvement( 0 ,  speed )
    elif keybinding.isKeyActive( "RIGHT" , listPressed ):
        player.mouvement( speed ,  0 )
    elif keybinding.isKeyActive( "UP" , listPressed ):
        player.mouvement( 0 , -speed )
    else:
        player.mouvement( 0 , 0 )
        
    if keybinding.isKeyActive( "ATTACK" , listPressed ):
        attackJoueur.attack(player,listEnnemis)
    player.anim += 0.28
    #IA
    for e in listEnnemis:
        if e.hp < 0:
            listEnnemis.remove(e)
        if ia.agro(player.position,e.position):
            ia.trajectoire(player.position,e)
        
        ia.attackIA(player,e)
        
    #clock
    clock.tick(60)

pygame.quit()