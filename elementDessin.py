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
    
    def setCenterX(self,x):
        if self.intSize:
            self.x = x-self.w//2
        else:
            self.x = x-self.w/2
            
    def setCenterY(self,y):
        if self.intSize:
            self.y = y-self.h/2
        else:
            self.y = y-self.h/2
    
    def setCSize(self,w,h):
        self.setCWidth(w)
        self.setCHeight(h)
        print("set size to:",w,h)
            
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

#un rectangle avec bords arrondis, redimensionable
class RectangleArrondi(_Rectangle):
    
    def __init__(self,x,y,w,h,radius,color):
        self.radius = radius
        self.colorBack = color
        super(RectangleArrondi,self).__init__(x,y,w,h,True)
        RectangleArrondi.redraw(self)
    
    def drawOn(self,surf):
        surf.blit( self.surf, (self.x,self.y) )
    
    def redraw(self):
        x,y,w,h,radius = self.x,self.y,self.w,self.h,self.radius
        color = self.colorBack
        self.surf = pygame.Surface( (self.w,self.h) )
        self.surf.fill( (255,0,255) )
        self.surf.set_colorkey( (255,0,255) )
        print("draw with :",w,h,radius)
        pygame.draw.rect( self.surf , color , ( radius,0 , w-2*radius,h) )
        pygame.draw.rect( self.surf , color , ( 0,radius , w,h-2*radius) )
        pygame.draw.circle( self.surf , color , (radius,radius) , radius )
        pygame.draw.circle( self.surf , color , (w-radius,radius) , radius )
        pygame.draw.circle( self.surf , color , (w-radius,h-radius) , radius )
        pygame.draw.circle( self.surf , color , (radius,h-radius) , radius )

#un cadre pouvant accueillir d'autres éléments à l'intérieur de celui-ci
class Cadre(RectangleArrondi):
    
    def __init__(self,x,y,w,h,widgets,radius=0,color=(0,0,0),apparent=False):
        self.widgets = widgets
        if apparent:
            super(Cadre,self).__init__(x,y,w,h,radius,color)
            RectangleArrondi.redraw(self)
        else:
            _Rectangle.__init__(self,x,y,w,h,True)
            self.surf = pygame.Surface( (w,h) )
            self.surf.fill( (255,0,255) )
            self.surf.set_colorkey( (255,0,255) )
        self.redraw()
    
    def redraw(self):
        for w in self.widgets:
            w.drawOn( self.surf )
    
#un bouton avec une surface intérieure
class BoutonRempli(RectangleArrondi):
    
    def __init__(self,x,y,w,h,radius,colorBack,interieur):
        super(BoutonRempli,self).__init__(x,y,w,h,radius,colorBack)
        self.interieur = interieur
        BoutonRempli.redraw(self)
    
    def redraw(self):
        x,y,w,h,radius = self.x,self.y,self.w,self.h,self.radius
        inW , inH = self.interieur.get_width() , self.interieur.get_height()
        print("int :",self.interieur)
        print("s :",self.size)
        if inW > w-2*radius or inH > h-2*radius:
            _Rectangle.setCSize( self,max( inW+2*radius , w ) , max( inH+2*radius , h ) )
        RectangleArrondi.redraw(self)
        self.xInPos = (self.w - inW) //2
        self.yInPos = (self.h - inH) //2
        print("blit at,",self.xInPos,self.yInPos)
        self.surf.blit( self.interieur , (self.xInPos,self.yInPos) )

#un rectangle arrondi contenant du texte centré
#la taille s'agrandi si le texte ne rentre pas
class BoutonTexte(BoutonRempli):
    
    def __init__(self,x,y,w,h,radius,colorBack,police,texte,colorTexte):
        self.police     = police
        self.texte      = texte
        self.colorBack  = colorBack
        self.colorTexte = colorTexte
        self.interieur  = self.police.render( self.texte , True, self.colorTexte , self.colorBack)
        super(BoutonTexte,self).__init__(x,y,w,h,radius,colorBack,self.interieur)
    
    def redraw(self):
        self.interieur  = self.police.render( self.texte , True, self.colorTexte , self.colorBack)
        BoutonRempli.redraw(self)








