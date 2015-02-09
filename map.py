"""

Fichier de gestion des cartes
la gestion s'effectue par régions séparées,
qui sont chacune identifiées par un nom

"""

#variable contenant la carte utilisée tout au long du jeu
theMap = None

#defini un tableau de cases
class region:
    
    def __init__(self,name):
        self.name           = name #nom de la région
        self.data           = None #données de sprite
        self.ennemiBaseList = []   #position de spawn des ennemis
        self.ennemiList     = []   #liste des ennemis sur la carte
        self.teleportList   = []   #liste des points de changements de région
        
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
        except Exception as e:
            print( e )
        else:
            fileEnnemi.close()
            
        #chargement des points de transports
        try:
            fileLink = open("map/"+name+"_link.txt")
            for line in fileLink:
                infoLine = line.strip().split(",")
                posOrigin = ( int(infoLine[0]),int(infoLine[1]) )
                posDest   = ( infoLine[2],int(infoLine[3]),int(infoLine[4]) )
                self.teleportList.append( [ posOrigin , posDest ] )
        except:
            pass
        else:
            fileLink.close()
    
    #donne la case à un certain endroit
    def at(self,x,y):
        if x>self.width or x<0 or y>self.height or y<0:
            return 20
        try:
            return self.data[x][y]
        except:
            return 20
    
    def teleportAt(self,x,y):
        for i in self.teleportList:
            if i[0] == (int(x),int(y)):
                return i[1]
        return None

#defini l'ensemble des régions
class map:
    
    def __init__(self):
        self.regionList = {}
        #self.regionList["test"] = region("test")
        self.regionList["base"]    = region("base")
        self.regionList["atelier"] = region("atelier")
    