

class item():
    def __init__(self,name,type):
        self.name = name
        self.type = type
        if type == 'arme':
            try:
                file = open("item/arme/" + name+".txt")
                self.degatarme = file.readline().strip().split(";")[0]
            except:
                pass
            
            
    
            