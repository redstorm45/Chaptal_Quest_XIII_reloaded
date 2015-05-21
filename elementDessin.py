"""

Module contenant plusieurs classe,
définissant différents éléments de base pouvant être dessinés

les classes nommées _<nom>
sont des classe abstraites, contenant seulement des dimensions

les autres sont des classes servant de support de dessin

b = BoutonTexte( 1,1,50,50,5,(0,0,0),pygame.font.Font("Verdana",20),"hello",(250,250,250))

"""

import pygame

#un rectangle de base redimensionable (intSize => arrondi à l'entier)
class _Rectangle():
    
    def __init__(self,x,y,w,h,intSize=True):
        self.x = x
        self.y = y
        self.pos = x,y
        self.w = w
        self.h = h
        self.size = w,h
        self.intSize=intSize
        self.container = None
    
    def translate(self,x,y):
        self.x += x
        self.y += y
        
    def setTop(self,y):
        self.y = y
        self.pos = self.x,y
        
    def setBot(self,y):
        self.y = y - self.h
        self.pos = self.x,self.y
        
    def setLeft(self,x):
        self.x = x
        self.pos = x,self.y
        
    def setRight(self,x):
        self.x = x - self.w
        self.pos = self.x,self.y
    
    def setSize(self,w,h):
        self.w , self.h = w,h
        self.size = w,h
    
    def setCenter(self,x,y):
        self.setCenterX(x)
        self.setCenterY(y)
    
    def setCenterX(self,x):
        if self.intSize:
            self.x = x-self.w//2
        else:
            self.x = x-self.w/2
        self.pos = self.x,self.y
        
    def setCenterY(self,y):
        if self.intSize:
            self.y = y-self.h/2
        else:
            self.y = y-self.h/2
        self.pos = self.x,self.y
    
    def setCSize(self,w,h):
        self.setCWidth(w)
        self.setCHeight(h)
            
    def setCWidth(self,w):
        if self.intSize:
            midX = self.x+self.w//2
            self.w = w
            self.size = w,self.h
            self.setLeft( midX - w//2 )
        else:
            midX = self.x+self.w/2
            self.w = w
            self.size = w,self.h
            self.setLeft( midX - w/2 )
            
    def setCHeight(self,h):
        if self.intSize:
            midY = self.y+self.h//2
            self.h = h
            self.size = self.w,h
            self.setTop( midY - h//2 )
        else:
            midY = self.y+self.h/2
            self.h = h
            self.size = self.w,h
            self.setTop( midY - h/2 )
        
    def getTruePos(self):
        if self.container:
            xc,yc = self.container.getTruePos()
            return self.x+xc,self.y+yc
        else:
            return self.pos
            
    def getCenterPos(self):
        if self.intSize:
            return self.x + self.w//2 , self.y + self.h//2
        else:
            return self.x + self.w/2 , self.y + self.h/2
    
    def isInside(self,x,y):
        tx,ty = self.getTruePos()
        return ( x>= tx and y>= ty and x<= tx+self.w and y<= ty+self.h )
    
    def __str__(self):
        return "rect at:"+str(self.pos)+"["+str(self.getTruePos())+"]"+" size "+str(self.size)

def roundedRect(w,h,radius,color):
    surf = pygame.Surface( (w,h) )
    surf.fill( (255,0,255) )
    surf.set_colorkey( (255,0,255) )
    pygame.draw.rect( surf , color , ( radius,0 , w-2*radius,h) )
    pygame.draw.rect( surf , color , ( 0,radius , w,h-2*radius) )
    pygame.draw.circle( surf , color , (radius,radius) , radius )
    pygame.draw.circle( surf , color , (w-radius,radius) , radius )
    pygame.draw.circle( surf , color , (w-radius,h-radius) , radius )
    pygame.draw.circle( surf , color , (radius,h-radius) , radius )
    return surf

#un rectangle avec bords arrondis, redimensionable
class RectangleArrondi(_Rectangle):
    
    def __init__(self,x,y,w,h,radius,color,colorBordure):
        self.radius = radius
        self.colorBack = color
        self.colorBordure = colorBordure
        _Rectangle.__init__(self,x,y,w,h,True)
        RectangleArrondi.redraw(self)
    
    def drawOn(self,surf):
        x,y = self.getTruePos()
        surf.blit( self.surf, (x,y) )
    
    def redraw(self):
        x,y,w,h,radius = self.x,self.y,self.w,self.h,self.radius
        self.surf = pygame.Surface( (w,h) )
        self.surf.fill( (255,0,255) )
        self.surf.set_colorkey( (255,0,255) )
        self.surf.blit( roundedRect(w,h,radius,self.colorBordure ) , (0,0) )
        self.surf.blit( roundedRect(w-4,h-4,radius-2,self.colorBack ) , (2,2) )

#un cadre pouvant accueillir d'autres éléments à l'intérieur de celui-ci
class Cadre(RectangleArrondi):
    
    def __init__(self ,xC ,yC ,widgets ,colorBordure=(0,0,0) ,radius=0 ,color=(0,0,0) ,apparent=False ,align="center" ,fixedSize=(-1,-1) ):
        self.widgets = widgets
        self.fixedSize = fixedSize
        self.calculateDim()
        self.align = align
        self.apparent = apparent
        if apparent:
            if align == "center":
                super(Cadre,self).__init__(xC - self.w//2,yC - self.h//2,self.w,self.h,radius,color,colorBordure)
            elif align == "topleft":
                super(Cadre,self).__init__(xC,yC,self.w,self.h,radius,color,colorBordure)
            elif align == "topright":
                super(Cadre,self).__init__(xC-self.w,yC,self.w,self.h,radius,color,colorBordure)
            elif align == "bottomright":
                super(Cadre,self).__init__(xC-self.w,yC-self.h,self.w,self.h,radius,color,colorBordure)
            RectangleArrondi.redraw(self)
        else:
            if align == "center":
                _Rectangle.__init__(self,xC-self.w//2,yC-self.h//2,self.w,self.h,True)
            elif align == "topleft":
                _Rectangle.__init__(self,xC,yC,self.w,self.h,True)
            elif align == "topright":
                _Rectangle.__init__(self,xC-self.w,yC,self.w,self.h,True)
            elif align == "bottomright":
                _Rectangle.__init__(self,xC-self.w,yC-self.h,self.w,self.h,True)
            self.surf = pygame.Surface( (self.w,self.h) )
            self.surf.fill( (255,0,255) )
            self.surf.set_colorkey( (255,0,255) )
        self.redraw()
    
    def setWidgets(self,widgets):
        self.widgets = widgets
        for w in self.widgets:
            if isinstance(w,RectangleArrondi):
                w.container = self
        self.calculateDim(False)
    
    def calculateDim(self,first = True):
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        
        for w in self.widgets:
            if isinstance(w,RectangleArrondi):
                self.minX = min( self.minX,w.x )
                self.maxX = max( self.maxX,w.x+w.w )
                self.minY = min( self.minY,w.y )
                self.maxY = max( self.minY,w.y+w.h )
            else:
                surf,x,y = w
                self.minX = min( self.minX,x )
                self.maxX = max( self.maxX,x+surf.get_width() )
                self.minY = min( self.minY,y )
                self.maxY = max( self.minY,y+surf.get_height() )
        
        if self.fixedSize == (-1,-1):
            self.w = self.maxX - self.minX
            self.h = self.maxY - self.minY
        else:
            self.w,self.h = self.fixedSize
        
        for w in self.widgets:
            if isinstance(w,RectangleArrondi):
                w.container = self
        
    def drawOn(self,surf):
        x,y = self.getTruePos()
        if self.apparent:
            surf.blit(self.surf,(x,y))
        for w in self.widgets:
            if isinstance(w,RectangleArrondi):
                w.drawOn(surf)
            else:
                wX,wY,wS = w
                surf.blit(wS,(wX,wY))
    
    def redraw(self):
        for w in self.widgets:
            if isinstance(w,RectangleArrondi):
                w.drawOn( self.surf )
            else:
                surf,x,y = w
                self.surf.blit( surf , (x,y) )
    
#un bouton avec une surface intérieure
class BoutonRempli(RectangleArrondi):
    
    def __init__(self,x,y,w,h,radius,colorBack,interieur,colorBordure,align="center"):
        RectangleArrondi.__init__(self,x,y,w,h,radius,colorBack,colorBordure)
        self.interieur = interieur
        self.align = align
        BoutonRempli.redraw(self)
    
    def redraw(self):
        x,y,w,h,radius = self.x,self.y,self.w,self.h,self.radius
        inW , inH = self.interieur.get_width() , self.interieur.get_height()
        if inW > w-2*radius or inH > h-2*radius:
            oldCX,oldCY = _Rectangle.getCenterPos(self)
            _Rectangle.setSize( self,max( inW+2*radius , w ) , max( inH+2*radius , h ) )
            if self.align == "center":
                _Rectangle.setCenter( self,oldCX,oldCY )
            elif self.align == "centertop":
                _Rectangle.setCenterX( self,oldCX )
        RectangleArrondi.redraw(self)
        self.xInPos = (self.w - inW) //2
        self.yInPos = (self.h - inH) //2
        self.surf.blit( self.interieur , (self.xInPos,self.yInPos) )

#un rectangle arrondi contenant du texte centré
#la taille s'agrandi si le texte ne rentre pas
class BoutonTexte(BoutonRempli):
    
    def __init__(self,x,y,w,h,radius,colorBack,colorBordure,police,texte,colorTexte,align="center",multiLine=False):
        self.police      = police
        self.texte       = texte
        self.colorBack   = colorBack
        self.colorTexte  = colorTexte
        self.align       = align
        self.multiLine   = multiLine
        self.radius      = radius
        self.w           = w
        self.drawInterieur()
        BoutonRempli.__init__(self,x,y,w,h,radius,colorBack,self.interieur,colorBordure,align)
    
    def redraw(self):
        BoutonTexte.drawInterieur(self)
        BoutonRempli.redraw(self)
    
    def drawInterieur(self):
        self.interieur  = self.police.render( self.texte , True, self.colorTexte , self.colorBack)
        if self.multiLine and self.interieur.get_width()> self.w-2*self.radius:
            #essaie de couper le texte
            lines = [self.texte]
            lastLine = ""
            current = 0
            while True:
                while True:
                    #enlève 1 mot de la fin
                    pos = lines[current].rfind(" ")
                    if "\n" in lines[current][:pos]:
                        pos = lines[current].find("\n")
                        lines[current].replace("\n"," ",1)
                    if lastLine == "":
                        lastLine = lines[current][pos+1:]
                    else:
                        lastLine = lines[current][pos+1:] + " " + lastLine
                    lines[current] = lines[current][:pos]
                    #réessaie de dessiner le texte
                    s = self.police.render( lines[current] , True, self.colorTexte , self.colorBack)
                    if s.get_width()< self.w-2*self.radius:
                        break
                lines.append(lastLine)
                current += 1
                lastLine = ""
                #éssaie de dessiner la dernière ligne
                s = self.police.render( lines[current] , True, self.colorTexte , self.colorBack)
                if s.get_width()< self.w-2*self.radius:
                    break
            #crée la surface complète
            surfs = []
            height = 0
            width = 0
            for l in lines:
                s = self.police.render( l , True, self.colorTexte , self.colorBack)
                height += s.get_height()
                width = max(width,s.get_width())
                surfs.append(s)
            self.interieur = pygame.Surface( (width,height) )
            self.interieur.fill( self.colorBack)
            pos = 0
            for i in range(len(lines)):
                self.interieur.blit( surfs[i], (0,pos) )
                pos += surfs[i].get_height()
            
    
    def updateTexte(self,texte):
        self.texte = texte
        BoutonTexte.redraw( self )
    
    def appendTexte(self,caract):
        if caract == "\b":
            if len(self.texte) > 1:
                self.updateTexte(self.texte[:len(self.texte)-1] )
            else:
                self.updateTexte( "" )
        else:
            if len(self.texte)<15:
                self.updateTexte( self.texte+caract )
            




