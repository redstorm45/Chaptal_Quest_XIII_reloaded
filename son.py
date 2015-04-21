import pygame

def musique():
    music = pygame.mixer.Sound(file = "musique/pirate.wav")
    return(music)

def mort():
    music = pygame.mixer.Sound(file = "musique/sparta.ogg")
    return(music)