
import texte

class PNG():
    def __init__(self,name,position):
        self.name = ""
        self.position = position
        self.spriteName = ""
        self.texte = ""
        try:
            file = open( "PNG/" + name + ".txt")
            self.name = file.readline().strip().split(";")[0]
            self.spriteName  = file.readline().strip().split(";")[0]
            self.texteId = file.readline().strip().split(";")[0]
            self.texte = texte.getTexte("PNG" , self.texteId )
        except:
            pass
        else:
            file.close()