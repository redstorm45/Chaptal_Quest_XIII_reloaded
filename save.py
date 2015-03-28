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
        saveFile.write("salle/2.V1.1,3,3\n") #position
        saveFile.write("PTSI\n")             #classe
        saveFile.write("0.5")
        saveFile.write("RLC")
        saveFile.write("RDM")
        saveFile.write("1")
        saveFile.write(str(player.capacite2Lvl))
        saveFile.write(str(player.pointbonus))
        saveFile.write(str(player.lvl))
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
            player.classe = saveFile.readline().strip()
            player.regen = float( saveFile.readline().strip() )
            player.capacite1 = saveFile.readline().strip()
            player.capacite2 = saveFile.readline().strip()
            player.capacite1Lvl = int( saveFile.readline().strip() )
            player.capacite2Lvl = int( saveFile.readline().strip() )
            player.pointbonus = int( saveFile.readline().strip() )
            player.lvl = int( saveFile.readline().strip() )
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
        saveFile.write(player.position[0]+","+str(player.position[1])+","+str(player.position[2])+"\n") #position
        saveFile.write(player.classe+"\n")
        saveFile.write(str(player.regen)+"\n")
        saveFile.write(str(player.capacite1)+"\n")
        saveFile.write(str(player.capacite2)+"\n")
        saveFile.write(str(player.capacite1Lvl)+"\n")
        saveFile.write(str(player.capacite2Lvl)+"\n")
        saveFile.write(str(player.pointbonus)+"\n")
        saveFile.write(str(player.lvl)+"\n")
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






