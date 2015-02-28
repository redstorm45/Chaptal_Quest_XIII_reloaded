"""

Fichier de gestion des cartes
la gestion s'effectue par régions séparées,
qui sont chacune identifiées par un nom

"""

#variable contenant la carte utilisée tout au long du jeu
theMap = None

#défini une zone d'évenement
class EventReg:
    
    def __init__(self,line):
        line = line.strip().split(":")
        #points A et B de la zone (angles)
        position = line[0].split(",")
        self.pA  = [ int(position[0]) , int(position[1]) ]
        self.pB  = [ int(position[2]) , int(position[3]) ]
        #type d'évenement
        info = line[1].split(",")
        if info[0] == "t": #point de téléport
            self.type = "teleport"
            self.dest = [ info[1],int(info[2]) , int(info[3]) ]
        if info[0] == "q": #découverte de quete
            self.type = "quest"
            self.q    = int(info[1])
    
    #si l'evenement s'active
    def activate(self,x,y):
        return  x>=self.pA[0] and x<= self.pB[0] and y>=self.pA[1] and y<= self.pB[1]
    

#defini un tableau de cases
class Region:
    
    def __init__(self,name):
        self.name           = name #nom de la région
        self.data           = None #données de sprite
        self.ennemiBaseList = []   #position de spawn des ennemis
        self.ennemiList     = []   #liste des ennemis sur la carte
        self.eventList      = []   #liste des points d'évenements
        
        #chargement de la base de la région
        try:
            file = open("map/"+name+".txt")
            #taille du niveau
            size = file.readline().strip().split("\t")
            self.width,self.height =  int(size[0]),int(size[1])
            #charge les données des cases
            self.data = [ [ 0 for i in range(self.height) ] for j in range(self.width)]
            for y in range(self.height):
                line = file.readline().strip().split("\t")
                for x in range(len(line)):
                    self.data[x][y] = int(line[x])
        except Exception as e:
            raise Exception("FATAL ERROR:\n"+str(e))
        else:
            file.close()
            
        #chargement des ennemis présents
        try:
            fileEnnemi = open("map/"+name+"_ennemi.txt")
            for l in fileEnnemi:
                lineEnnemi = l.strip().split(",")
                self.ennemiBaseList.append( [ lineEnnemi[2] , int(lineEnnemi[0]) , int(lineEnnemi[1]) ] )
        except:
            pass
        else:
            fileEnnemi.close()
            
        #chargement des points d'évenements
        try:
            fileEvent = open("map/"+name+"_event.txt")
            for line in fileEvent:
                self.eventList.append( EventReg(line) )
        except:
            pass
        else:
            fileEvent.close()
        print("loaded region:",self.name)
    
    #donne la case à un certain endroit
    def at(self,x,y):
        if x>self.width or x<0 or y>self.height or y<0:
            return 20
        try:
            return self.data[x][y]
        except:
            return 20
    
    def eventAt(self,x,y,type=None):
        l = []
        for i in self.eventList:
            if i.activate(int(x),int(y)):
                if (not type) or type==i.type:
                    l.append(i)
        return l

#defini l'ensemble des régions
class Map:
    
    def __init__(self):
        self.regionList = {}
        self.regionList["salle/1.V1.1"] = Region("salle/1.V1.1")
        self.regionList["salle/1.V1.2"] = Region("salle/1.V1.2")
        self.regionList["salle/1.V1.3"] = Region("salle/1.V1.3")
        self.regionList["salle/1.V1.4"] = Region("salle/1.V1.4")
        
        self.regionList["salle/2.V1.1"] = Region("salle/2.V1.1")
        self.regionList["salle/2.V1.2"] = Region("salle/2.V1.2")
        self.regionList["salle/2.V1.3"] = Region("salle/2.V1.3")
        self.regionList["salle/2.V1.4"] = Region("salle/2.V1.4")
        
        self.regionList["couloir/1.V1"]  = Region("couloir/1.V1")
        self.regionList["couloir/1.V1N"] = Region("couloir/1.V1N")
        self.regionList["couloir/2.V1"]  = Region("couloir/2.V1")
        
        self.regionList["escalier/2.7"] = Region("escalier/2.7")
        self.regionList["escalier/1.7"] = Region("escalier/1.7")
        self.regionList["escalier/0.7"] = Region("escalier/0.7")
        self.regionList["escalier/0_5.7"] = Region("escalier/0_5.7")
        self.regionList["base"]    = Region("base")
        self.regionList["atelier"] = Region("atelier")












