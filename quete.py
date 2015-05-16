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
        self.changed   = False     #la quete as-t-elle étée modifiée (avancement, etc..)
        self.type      = 0         #quête principale/secondaire/cachée
        self.name      = "no name" #nom de la quête
        self.info      = "no info" #desciption de la quête
        self.required  = []        #quêtes requises pour activer celle-ci
        self.autoTrouve= False     #la quete requiert d'être trouvée
        self.objType   = 0         #type d'objectif de la quête
        self.data      = {}        #données dépendant de la quête
        #lecture du fichier correspondant à l'id
        try:
            f = open("quete/"+str(id)+".txt",encoding = "utf-8")
            self.type      = int( self.getNextLine(f) )
            self.name      = self.getNextLine(f).strip()
            self.info      = self.getMultiLine(f).strip()
            self.required  = eval( self.getNextLine(f) )
            self.autoTrouve= eval( self.getNextLine(f) )
            self.objType   = int(self.getNextLine(f).strip())
            if self.objType == 1:
                self.data["target"] = eval( self.getNextLine(f).strip() )
            elif self.objType == 3:
                self.data["target"] = eval( self.getNextLine(f).strip() )
                self.data["current"] = {}
                for k in self.data["target"].keys():
                    self.data["current"][k] = 0
        except Exception as e:
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
    
    #valide la quête si tous les objectifs ont étés remplis
    def checkCompleted(self,player = None):
        if self.completed:
            return
        if player:
            pos = player.position
        else:
            pos = ("",0,0)
        #objectif de position
        if self.objType == 1:
            if self.data["target"][0] == pos[0]:
                if self.data["target"][1] == self.data["target"][2] == -1:
                    self.completed = True
                    self.changed = True
                elif int(pos[1]) == self.data["target"][1] and int(pos[2]) == self.data["target"][2]:
                    self.completed = True
                    self.changed = True
        #objectif d'ennemi
        elif self.objType == 3:
            compl = True
            for k in self.data["target"].keys():
                if self.data["current"][k] < self.data["target"][k]:
                    compl = False
            if compl:
                self.completed = True
                self.changed = True
    
    #donne un identificateur de statut pour stocker la quête dans la sauvegarde
    def status(self):
        if self.completed:
            return "c"
        elif self.trouvee:
            return "t"
        elif self.active:
            return "a"
        return "x"
    
    #change le statut de la quête à partir d'un identificateur
    def fromStatus(self,s):
        if s in ["a","t","c"]:
            self.active = True
        if s in ["t","c"]:
            self.trouvee = True
        if s in ["c"]:
            self.completed = True
    
#charge toutes les quêtes disponibles
def loadQuetes():
    global listeQuetes
    global listeQuetesActives
    i = 0
    listeQuetes = []
    listeQuetesActives = []
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
    for q in listeQuetes:
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
                if q.autoTrouve:
                    q.trouvee = True
                listeQuetesActives.append(q)

#représente les quêtes pour les sauvegarder
def getTextRepr():
    txt = ""
    for q in listeQuetes:
        txt += ";"+str(q.id)+","+q.status()
    return "["+txt[1:]+"]"

#charge la représentation
def fromTextRepr(txt):
    list = txt[1:-1].split(";")
    for i in list:
        if i != "":
            [qID,statut] = i.split(",")
            quest = getQuete( int(qID) )
            quest.fromStatus(statut)
            if quest.active:
                listeQuetesActives.append(quest)
        


