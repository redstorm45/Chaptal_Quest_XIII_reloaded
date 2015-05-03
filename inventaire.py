"""

module qui gère la sauvegarde d'items,
ainsi que l'inventaire du joueur

"""

class objet():
    
    
    def __init__(self,name):
        self.name = name
        
        try:
            file = open( "objets/" + name + ".txt",encoding = "utf-8")
            self.gameName = file.readline().strip().split(";")[0]
            self.stackable = bool(int(file.readline().strip().split(";")[0]))
            self.sprite = file.readline().strip().split(";")[0]
            self.type      = file.readline().strip().split(";")[0]
            if self.stackable:
                self.stackSize = 1
            else:
                self.stackSize = 0
            
            if self.type == 'arme':
                self.degatarme = file.readline().strip().split(";")[0]
            if self.type in ["casque","armure"]:
                self.defense = file.readline().strip().split(";")[0]
                
            file.close()
        except:
            print("défaut d'un objet:",name)
    
    def toString(self):
        return self.name+","+str(self.stackSize)
        
    def fromString(self,s):
        self.stackSize = int( s[1] )

class inventaire:
    
    def __init__(self):
        self.listObjets = []
    
    def add(self,obj):
        if obj.stackable:
            found = False
            for i in self.listObjets:
                if i.type == obj.type:
                    i.stackSize += 1
                    found = True
                    break
            if not found:
                self.listObjets.append(obj)
        else:
            self.listObjets.append(obj)
    
    def toString(self):
        str = ""
        for i in self.listObjets:
            str += ";"+i.toString()
        str = "["+str[1:] + "]"
        return str
    
    def fromString(self,str):
        str = str[1:-1]
        if len(str) == 0:
            return
        theList = str.split(";")
        self.listObjets = []
        for i in theList:
            if len(i) > 0:
                infos = i.split(",")
                obj = objet( infos[0] )
                obj.fromString(infos)
                self.listObjets.append( obj )
    
    