"""

Fichier de gestion des cartes
la gestion s'effectue par régions séparées,
qui sont chacune identifiées par un nom

"""

convertDic = {  "1"   : "s" ,
                "0"   : "v" ,
                "100" : "s" ,
                "2"   : "m1",
                "14"  : "m1",
                "4"   : "m3",
                "15"  : "m3",
                "6"   : "m5",
                "16"  : "m5",
                "8"   : "m7",
                "17"  : "m7",
                "3"   : "a3",
                "5"   : "a5",
                "7"   : "a7",
                "9"   : "a1",
                "10"  : "b7",
                "11"  : "b1",
                "12"  : "b3",
                "13"  : "b5",
                "18"  : "p"  ,
                
                "19"  : "tm9",
                "26"  : "tm7",
                "36"  : "tm8",
                "46"  : "tm5",
                "25"  : "tm3",
                "35"  : "tm5",
                "45"  : "tm7",
                "55"  : "tm1",
                
                "23"  : "ta6",
                "24"  : "ta5",
                "33"  : "ta8",
                "34"  : "ta7",
                "43"  : "ta2",
                "44"  : "ta1",
                "53"  : "ta4",
                "54"  : "ta3",
                
                "20"  : "e1",
                "30"  : "e4",
                "40"  : "e7",
                "50"  : "e10",
                "22"  : "e2",
                "32"  : "e5",
                "42"  : "e8",
                "52"  : "e11",
                "21"  : "e3",
                "31"  : "e7",
                "41"  : "e9",
                "51"  : "e12"}

#variable contenant la carte utilisée tout au long du jeu
theMap = None

#défini une zone d'évenement
class EventReg:
    
    def __init__(self,line):
        line = line.strip().split(":")
        #points A et B de la zone (angles)
        position = line[0].split(",")
        self.pA  = [ float(position[0]) , float(position[1]) ]
        self.pB  = [ float(position[2]) , float(position[3]) ]
        #type d'évenement
        info = line[1].split(",")
        if info[0] == "t": #point de téléport
            self.type = "teleport"
            self.dest = [ info[1],int(info[2]) , int(info[3]) ]
        if info[0] == "q": #découverte de quete
            self.type = "quest"
            self.q    = int(info[1])
            
    def changeSize(self,dx,dy):
        if dx<0:
            if self.pA[0] == self.pB[0]:
                return
        if dy<0:
            if self.pA[1] == self.pB[1]:
                return
        self.pB[0] += dx
        self.pB[1] += dy
        
    #si l'evenement s'active
    def activate(self,x,y):
        return (x>=self.pA[0] and x<= self.pB[0] and y>=self.pA[1] and y<= self.pB[1])
    
    def translate(self,dx,dy):
        self.pA[0] += dx
        self.pA[1] += dy
        self.pB[0] += dx
        self.pB[1] += dy
    
    #représentation (str) de cet evenement
    def __str__(self):
        area = str( self.pA[0] )+","+str( self.pA[1] )+","+str( self.pB[0] )+","+str( self.pB[1] )
        info = ""
        if self.type == "teleport":
            info = "t,"+self.dest[0]+","+str(self.dest[1])+","+str(self.dest[2])
        return area + ":" + info
        
    #représentation (str) de cet evenement, plus compact
    def __repr__(self):
        if self.type == "teleport":
            return "t,"+self.dest[0]+","+str(self.dest[1])+","+str(self.dest[2])
        else:
            return ""

class Item:
    
    def __init__(self,name):
        self.name = name
        try:
            file = open( "sprites/Items/"+str(name)+".txt" )
        except:
            pass

#defini un tableau de cases
class Region:
    
    def __init__(self,name):
        self.name           = name #nom de la région
        self.data           = None #données de sprite
        self.itemList       = []   #liste des items sur la carte
        self.ennemiBaseList = []   #position de spawn des ennemis
        self.ennemiList     = []   #liste des ennemis sur la carte
        self.eventList      = []   #liste des points d'évenements
        self.PNGbaseList    = []
        self.PNGlist        = []
        
        self.readOffset = [0,0]
        
        #chargement de la base de la région
        try:
            file = open("map/"+name+".txt")
            oldRegion = False
            #taille du niveau
            first = file.readline().strip().split("\t")
            if len(first) >= 3:
                self.width,self.height,self.style =  int(first[0]),int(first[1]),first [2]
            else:
                oldRegion = True
                self.width,self.height = int(first[0]),int(first[1])
                self.style = "style1"
            #charge les données des cases
            self.data = [ [ 0 for i in range(self.height) ] for j in range(self.width)]
            for y in range(self.height):
                line = file.readline().strip().split("\t")
                for x in range(self.width):
                    self.data[x][y] = line[x]
            #converti les anciennes régions
            if oldRegion:
                for y in range(self.height):
                    for x in range(self.width):
                        self.data[x][y] = convertDic[ self.data[x][y] ]
        except Exception as e:
            raise Exception("FATAL ERROR:\n"+str(e)+"\nat ")
        else:
            file.close()
            
        #chargement des items de la région
        try:
            file = open("map/"+name+"_item.txt")
            #charge les données des cases
            for line in file:
                xI,yI,type = line.strip().split(",")
                xI,yI = int(xI) , int(yI)
                self.itemList.append( [xI,yI,type] )
        except:
            pass
        else:
            file.close()
            
        #chargement des ennemis présents
        try:
            fileEnnemi = open("map/"+name+"_ennemi.txt")
            for l in fileEnnemi:
                lineEnnemi = l.strip().split(",")
                self.ennemiBaseList.append( ( lineEnnemi[2] , int(lineEnnemi[0]) , int(lineEnnemi[1]) ) )
        except:
            pass
        else:
            fileEnnemi.close()
        #chargement PNG
        try:
            filePNG = open("map/"+name+"_PNG.txt")
            for l in filePNG:
                linePNG = l.strip().split(",")
                self.PNGbaseList.append( ( linePNG[2], int(linePNG[0]) , int(linePNG[1])))
        except:
            pass
        else:
            filePNG.close()    
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
        tX,tY = x-self.readOffset[0] , y-self.readOffset[1]
        if tX>self.width or tX<0 or tY>self.height or tY<0:
            return "v"
        try:
            return self.data[tX][tY]
        except:
            return "v"
    
    def setAt(self,x,y,val):
        tX,tY = x-self.readOffset[0] , y-self.readOffset[1]
        #try to expand data size
        if tX>=self.width or tX<0 or tY>=self.height or tY<0:
            if tX>=self.width:
                expandX = tX-self.width +1
                self.data.extend( [["v" for i in range(self.height)] for j in range(expandX) ] )
                self.width += expandX
            if tY>=self.height:
                expandY = tY-self.height +1
                for i in range(self.width):
                    self.data[i].extend( ["v" for j in range(expandY) ] )
                self.height += expandY
            if tX<0:
                expandX = -tX
                for i in range(expandX):
                    self.data.insert( 0 , ["v" for i in range(self.height)] )
                self.width += expandX
                self.readOffset[0]-=expandX
            if tY<0:
                expandY = -tY
                for j in range(self.width):
                    for i in range(expandY):
                        self.data[j].insert( 0 , "v" )
                self.height += expandY
                self.readOffset[1]-=expandY
        #set the value
        tX,tY = x-self.readOffset[0] , y-self.readOffset[1]
        self.data[tX][tY] = val
    
    def eventAt(self,x,y,type=None):
        l = []
        for i in self.eventList:
            if i.activate(int(x),int(y)):
                if (not type) or type==i.type:
                    l.append(i)
        return l
    
    def resetReadOffset(self):
        for e in self.ennemiList:
            e.translate( -self.readOffset[0] ,-self.readOffset[1] )
        for e in self.eventList:
            e.translate( -self.readOffset[0] ,-self.readOffset[1] )
        self.readOffset = [0,0]

#defini l'ensemble des régions
class Map:
    
    def __init__(self):
        self.regionList = {}
        self.regionList["couloir/2.V1"] = Region("couloir/2.V1")
        
        self.regionList["salle/2.V1.1"] = Region("salle/2.V1.1")
        self.regionList["salle/2.V1.2"] = Region("salle/2.V1.2")
        self.regionList["salle/2.V1.3"] = Region("salle/2.V1.3")
        self.regionList["salle/2.V1.4"] = Region("salle/2.V1.4")
        
        self.regionList["salle/1.V1.1"] = Region("salle/1.V1.1")
        self.regionList["salle/1.V1.2"] = Region("salle/1.V1.2")
        self.regionList["salle/1.V1.3"] = Region("salle/1.V1.3")
        self.regionList["salle/1.V1.4"] = Region("salle/1.V1.4")
        
        self.regionList["salle/E.1"] = Region("salle/E.1")
        
        self.regionList["couloir/1.V1"]  = Region("couloir/1.V1")
        self.regionList["couloir/1.V1N"] = Region("couloir/1.V1N")
        self.regionList["couloir/2.V1"]  = Region("couloir/2.V1")
        
        self.regionList["escalier/2.7"] = Region("escalier/2.7")
        self.regionList["escalier/1_5.7"] = Region("escalier/1_5.7")
        self.regionList["escalier/1.7"] = Region("escalier/1.7")
        self.regionList["escalier/0_5.7"] = Region("escalier/0_5.7")
        self.regionList["escalier/0.7"] = Region("escalier/0.7")
        
        self.regionList["cours/D"] = Region("cours/D")
        self.regionList["cours/E"] = Region("cours/E")











