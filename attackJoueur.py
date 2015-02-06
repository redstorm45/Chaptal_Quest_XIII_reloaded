"""

Fichier de gestion des attaques de joueur à ennemi
et d'ennemi à joueur

"""

from math import exp


def attack(joueur,ennemi):
    if joueur.direction <= 2:
        for i in range(len(ennemi)):
            if (int(ennemi[i].position[2] - joueur.position[2]) < 1):
                ennemi[i].hp = ennemi[i].hp - (joueur.dammage*exp(-ennemi[i].armure/300))