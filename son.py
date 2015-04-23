"""

Ce module permet la gestion du son,
à travers un flux reservé pour la musique de fond,
les autres sons trouvant d'eux-mêmes leurs places

"""


import pygame
import option

sons = {}
channelsActives = []
background = None

def init():
    global background
    #charge les musiques
    loadMusiques()
    
    #initialise les channels
    background = pygame.mixer.Channel(0)
    pygame.mixer.set_reserved(1)         #le flux 'background' est reservé
    
    #met le volume au bon niveau
    setGlobalVolume(option.musiqueVolume)

#arrète toutes les musiques en cours
def stop():
    background.stop()
    for c in channelsActives:
        if c.get_busy():
            c.stop()

def loadMusiques():
    sons["pirate"] = pygame.mixer.Sound(file = "musique/pirate.wav")
    sons["mort"] = pygame.mixer.Sound(file = "musique/sparta.ogg")

def setGlobalVolume(pourcent):
    for k in sons.keys():
        sons[k].set_volume(pourcent/100.0)

def play(name):
    if option.musiqueActive:
        ch = sons[name].play()
        if not ch in channelsActives:
            channelsActives.append(ch)
        
def playMusique(name):
    if option.musiqueActive:
        background.play(sons[name])
