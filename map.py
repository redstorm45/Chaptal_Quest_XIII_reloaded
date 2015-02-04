

theMap = None
#defini un tableau de cases
class region:
    
    def __init__(self,name):
        self.name = name
        try:
            file = open("map/"+name+".txt")
            #taille du niveau
            size = file.readline().strip().split(";")
            self.width,self.height =  int(size[0]),int(size[1])
            #charge les données de type de case
            self.data = [ [ 0 for i in range(self.height) ] for j in range(self.width)]
            for y in range(self.height):
                line = file.readline().strip().split(";")
                for x in range(len(line)):
                    self.data[x][y] = int(line[x])
        except Exception as e:
            raise Exception("noooo!!!!\n"+str(e))
    
    def at(self,x,y):
        return self.data[x][y]

class map:
    
    def __init__(self):
        self.regionList = {}
        self.regionList["test"] = region("test")
    