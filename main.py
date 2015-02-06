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


#charge la map
map.theMap = map.map()

#charge les sprites
dessin.loadAllSprites()

#defini un joueur et ennemi
player = joueur.Joueur(2,2)
listEnnemis = []

listEnnemis.append( ennemi.Ennemi(5,5))


#vitesse du déplacement
speed = 1/16
speedDiag = speed

#crée la fenetre
fenetre = pygame.display.set_mode( (dessin.SCR_WIDTH*64,dessin.SCR_HEIGHT*64) )
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

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
            if event.key == K_a:
                pass
        """
        different deplacement et capacité
        """
    #gestion des déplacements
    listPressed = pygame.key.get_pressed()
    if listPressed[K_LEFT] and listPressed[K_UP]:
        player.mouvement( -speedDiag , -speedDiag )
    elif listPressed[K_LEFT] and listPressed[K_DOWN]:
        player.mouvement( -speedDiag ,  speedDiag )
    elif listPressed[K_RIGHT] and listPressed[K_DOWN]:
        player.mouvement(  speedDiag ,  speedDiag )
    elif listPressed[K_RIGHT] and listPressed[K_UP]:
        player.mouvement(  speedDiag , -speedDiag )
    elif listPressed[K_LEFT]:
        player.mouvement( -speed , 0 )
    elif listPressed[K_DOWN]:
        player.mouvement( 0 ,  speed )
    elif listPressed[K_RIGHT]:
        player.mouvement( speed ,  0 )
    elif listPressed[K_UP]:
        player.mouvement( 0 , -speed )
    elif listPressed[K_SPACE]:
        attackJoueur.attack(player,listEnnemis)
    else:
        player.mouvement( 0 , 0 )
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