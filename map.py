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
        self.name = name
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
            raise Exception("noooo!!!!\n"+str(e))
    #donne la case à un certain endroit
    def at(self,x,y):
        try:
            return self.data[x][y]
        except:
            return 2

#defini l'ensemble des régions
class map:
    
    def __init__(self):
        self.regionList = {}
        #self.regionList["test"] = region("test")
        self.regionList["base"] = region("base")
    