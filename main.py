import pygame
from pygame.locals import *

import map
import dessin
import joueur
import math


#charge la map
map.theMap = map.map()

#charge les sprites
dessin.loadAllSprites()

#defini un joueur
player = joueur.Joueur()

#vitesse du déplacement
speed = 1/16
speedDiag = speed/math.sqrt(2)

#crée la fenetre
fenetre = pygame.display.set_mode( (1024,680) )
pygame.display.set_caption("Chaptal Quest XIII - reloaded")

clock = pygame.time.Clock()

running = True
while running:
    #dessin
    regionAffichee = player.position[0]
    dessin.drawRegion(fenetre,regionAffichee)
    dessin.drawPlayer(fenetre,player)
    pygame.display.flip()
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
    print(player.position)
    #IA
    """
    à faire
    """
    #clock
    clock.tick(60)

pygame.quit()