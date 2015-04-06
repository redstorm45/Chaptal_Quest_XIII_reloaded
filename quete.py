"""

Fichier qui gère toutes les quetes en cours
ainsi que les quêtes faites et à faires

les quêtes sont identifiées par un id, càd un nombre

"""

import option

listeQuetes = []
listeQuetesActives = []


class Quete:
    
    def __init__(self,id):
        self.id        = id
        self.active    = False     #si la quête est disponible au joueur (il peut la trouver)
        self.trouvee   = False     #si le joueur a trouvé la quête, qui est alors affiché dans son menu des quetes
        self.completed = False     #si le joueur a terminée cette quête
        self.type      = 0         #quête principale/secondaire/cachée
        self.name      = "no name" #nom de la quête
        self.info      = "no info" #desciption de la quête
        self.required  = []        #quêtes requises pour activer celle-ci
        self.objType   = 0         #type d'objectif de la quête
        #lecture du fichier correspondant à l'id
        try:
            f = open("quete/"+str(id)+".txt",encoding = "utf-8")
            self.type      = int( self.getNextLine(f) )
            self.name      = self.getNextLine(f).strip()
            self.info      = self.getMultiLine(f).strip()
            self.required  = eval( self.getNextLine(f) )
            self.objType   = int(self.getNextLine(f).strip())
        except:
            self.id = 0
            return
    
    #donne une représentation de l'object sous forme de string
    def __repr__(self):
        return str(self.id)+" "+self.name+":"+self.info+str(self.required)+"\n"
        
    #donne la prochaine ligne qui n'est pas commentée
    def getNextLine(self,f):
        line = ""
        while True:
            line = f.readline()
            if not line.startswith("#"):
                break
        return line
    
    #donne plusieurs lignes de texte à la suite
    def getMultiLine(self,f):
        line = self.getNextLine(f)
        while True:
            l = f.readline()
            if not l.startswith("#"):
                line += l
            else:
                break
        return line
        
#charge toutes les quêtes disponibles
def loadQuetes():
    i = 0
    while True:
        i += 1
        q = Quete(i)
        if q.id:
            listeQuetes.append(q)
        else:
            break
    if option.debugMode:
        print("loaded",i,"quests")
        print(listeQuetes)

#donne une quete par son id
def getQuete(id):
    for q in listeQuetesActives:
        if q.id == id:
            return q
    return None

#active les quetes qui sont débloquables
def refreshActive():
    for q in listeQuetes:
        if not q.active:
            activate = True
            for check in q.required:
                if not listeQuetes[check-1].completed:
                    activate = False
            if activate:
                q.active = True
                listeQuetesActives.append(q)





