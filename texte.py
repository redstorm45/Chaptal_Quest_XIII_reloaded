"""

Module qui gère les différents textes affichés à l'écran
ainsi que leur chargement

"""

import option

texteList = {}

#donne un texte chargé par famille et nom
def getTexte(groupe,name):
    return texteList[groupe][name]

#charge tous les textes
def loadTextes():
    global texteList
    i = 0
    while True:
        i += 1
        #lis un fichier de texte
        try:
            file = open("texte/"+str(i)+".txt")
            groupe = file.readline().strip()
            name = file.readline().strip()
            texte = ""
            while True:
                l = file.readline()
                texte += l
                if l == "":
                    break
            texte.strip()
            if not groupe in texteList.keys():
                texteList[groupe] = {}
            texteList[groupe][name] = texte
        except:
            break
        else:
            file.close()
    if option.debugMode:
        print("loaded",i,"textes")


