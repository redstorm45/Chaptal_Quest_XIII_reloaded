
import texte

class PNG():
    def __init__(self,name,position):
        self.name = ""
        self.position = position
        self.spriteName = ""
        self.texte = ""
        try:
            file = open( "PNG/" + name + ".txt",encoding="utf-8")
            self.name = file.readline().strip().split(";")[0]
            self.spriteName  = file.readline().strip().split(";")[0]
            self.texteId = file.readline().strip().split(";")[0]
            self.texte = texte.getTexte("PNJ" , self.texteId )
        except Exception as e:
            print("no load pnj",e)
        else:
            file.close()