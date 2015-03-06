"""

Fichier responsable de la sauvegarde et du chargement des informations
sur une partie (avancement des quetes, fillière etc...)

"""

import option
import os

currentSaveName = None

#vérification d'existence d'un fichier de sauvegarde
def check(name):
    return os.path.exists("save/"+name+".save")

#donne la liste des sauvegardes
def getAllNames():
    l = os.listdir("save/")
    #extrait seulement les noms de sauvegardes
    lnames = []
    for item in l:
        if item.endswith(".save"):
            lnames.append(item[:-5])
    return lnames

#création d'un nouveau fichier de sauvegarde
def create(name):
    if check(name):
        return False
    try:
        saveFile = open("save/"+name+".save","w")
        saveFile.write("salle/2.V1.1,2,2\n") #position
    except:
        return False
    else:
        saveFile.close()
    return True

#chargement d'un fichier de sauvegarde
def load(name,player):
    global currentSaveName
    if currentSaveName:
        return False
    else:
        currentSaveName = name
        try:
            saveFile = open("save/"+currentSaveName+".save","r")
            #position
            l = saveFile.readline()
            player.position = l.strip().split(",")
            player.position[1] = float(player.position[1])
            player.position[2] = float(player.position[2])
        except Exception as e:
            return False
        else:
            saveFile.close()
    if option.debugMode:
        print("game loaded!")
    return True

#sauvagarde des données dans un fichier de sauvegarde
def save(player):
    global currentSaveName
    try:
        saveFile = open("save/"+currentSaveName+".save","w")
        saveFile.write(player.position[0]+","+str(player.position[1])+","+str(player.position[2])) #position
    except:
        return False
    else:
        saveFile.close()
    if option.debugMode:
        print("game saved!")
    return True

#déchargement du fichier courrant de la mémoire
def unload():
    global currentSaveName
    currentSaveName = None
    #RAZ des quetes






