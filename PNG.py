
class PNG():
    def __init__(self,name,position):
        file = open( "PNG/" + name + ".txt")
        self.name = file.readline().strip().split(";")
        self.spriteName  = file.readline().strip().split(";")