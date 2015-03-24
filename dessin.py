"""

Fichier de gestion du dessin et des sprites

à faire:
  - augmenter le nombre de sprites
  - ajouter le scrolling de map, pour ne dessiner les sprites que de
    quelques cases plus loins que la taille de l'écran


Liste des sprites:

1   : beton
2   : mur std haut
3   : mur std haut-gauche intérieur
4   : mur std gauche
5   : mur std bas-gauche intérieur
6   : mur std bas
7   : mur std bas-droite intérieur
8   : mur std droite
9   : mur std haut-droite intérieur
10  : mur std haut-gauche extérieur
11  : mur std bas-gauche extérieur
12  : mur std bas-droite extérieur
13  : mur std haut-droite extérieur
14  : mur escalier haut
15  : mur escalier gauche
16  : mur escalier bas
17  : mur escalier droite
18  : planches de bloquage
19  : tapis central
20  : escalier vers le haut, partie gauche
21  : escalier vers le haut, partie droite
22  : escalier vers le haut, partie centrale
23  : fin de tapis vers le haut, partie gauche
24  : fin de tapis vers le haut, partie droite
25  : fin de tapis vers le haut, partie centrale
26  : tapis vers le haut

30  : escalier vers la gauche, partie gauche
31  : escalier vers la gauche, partie droite
32  : escalier vers la gauche, partie centrale
33  : fin de tapis vers la gauche, partie gauche
34  : fin de tapis vers la gauche, partie droite
35  : fin de tapis vers la gauche, partie centrale
36  : tapis vers la gauche

40  : escalier vers le bas, partie gauche
41  : escalier vers le bas, partie droite
42  : escalier vers le bas, partie centrale
43  : fin de tapis vers le bas, partie gauche
44  : fin de tapis vers le bas, partie droite
45  : fin de tapis vers le bas, partie centrale
46  : tapis vers le bas

50  : escalier vers la droite, partie gauche
51  : escalier vers la droite, partie droite
52  : escalier vers la droite, partie centrale
53  : fin de tapis vers la droite, partie gauche
54  : fin de tapis vers la droite, partie droite
55  : fin de tapis vers la droite, partie centrale
56  : tapis vers la droite

100 : plancher
"""

import map
import ennemi
import os
import pygame
import mouse
import option
import debug
import option as opt
import texte
import elementDessin as elt

SCR_WIDTH   = 20   #largeur de l'écran (en termes de nombre de cases)
SCR_HEIGHT  = 10   #hauteur de l'écran

xOffset = 0
yOffset = 0

sprites = {}

listStyleSprites =   ["v" ,"s","p"                               #vide , sol , planches
                     ,"m1","m2","m3","m4","m5","m6","m7","m8"    #murs
                     ,"a1","a2","a3","a4","a5","a6","a7","a8"    #angles interieurs
                     ,"b1","b2","b3","b4","b5","b6","b7","b8"    #angles exterieurs
                     ,"e1","e2","e3","e4","e5","e6","e7","e8","e9","e10","e11","e12"   #escaliers
                     ,"ta1","ta2","ta3","ta4","ta5","ta6","ta7","ta8"   #angles tapis
                     ,"tp1","tp2","tp3","tp4","tp5","tp6","tp7","tp8","tp8"]   #plat tapis

listSprites = { 0   : "vide",
                1   : "beton",
                2   : "mur std haut",
                3   : "mur std haut-gauche intérieur",
                4   : "mur std gauche",
                5   : "mur std bas-gauche intérieur",
                6   : "mur std bas",
                7   : "mur std bas-droite intérieur",
                8   : "mur std droite",
                9   : "mur std haut-droite intérieur",
                10  : "mur std haut-gauche extérieur",
                11  : "mur std bas-gauche extérieur",
                12  : "mur std bas-droite extérieur",
                13  : "mur std haut-droite extérieur",
                14  : "mur escalier haut",
                15  : "mur escalier gauche",
                16  : "mur escalier bas",
                17  : "mur escalier droite",
                18  : "planches de bloquage",
                19  : "tapis central",
                20  : "escalier vers le haut, partie gauche",
                21  : "escalier vers le haut, partie droite",
                22  : "escalier vers le haut, partie centrale",
                23  : "fin de tapis vers le haut, partie gauche",
                24  : "fin de tapis vers le haut, partie droite",
                25  : "fin de tapis vers le haut, partie centrale",
                26  : "tapis vers le haut",
                
                30  : "escalier vers la gauche, partie gauche",
                31  : "escalier vers la gauche, partie droite",
                32  : "escalier vers la gauche, partie centrale",
                33  : "fin de tapis vers la gauche, partie gauche",
                34  : "fin de tapis vers la gauche, partie droite",
                35  : "fin de tapis vers la gauche, partie centrale",
                36  : "tapis vers la gauche",
                
                40  : "escalier vers le bas, partie gauche",
                41  : "escalier vers le bas, partie droite",
                42  : "escalier vers le bas, partie centrale",
                43  : "fin de tapis vers le bas, partie gauche",
                44  : "fin de tapis vers le bas, partie droite",
                45  : "fin de tapis vers le bas, partie centrale",
                46  : "tapis vers le bas",
                
                50  : "escalier vers la droite, partie gauche",
                51  : "escalier vers la droite, partie droite",
                52  : "escalier vers la droite, partie centrale",
                53  : "fin de tapis vers la droite, partie gauche",
                54  : "fin de tapis vers la droite, partie droite",
                55  : "fin de tapis vers la droite, partie centrale",
                56  : "tapis vers la droite",
                
                100 : "plancher"}

#polices
menuFont = None
buttonFontXXS = None
buttonFontXS = None
buttonFontS = None
buttonFontM = None
buttonFontL = None

#surfaces du menu
menuBack = None
menuTitle = None
menuButtons = {}

#surfaces de l'écran d'option
optionBack = None
optionTitle = None

#surfaces de l'overlay en jeu
overlayBack = None
overlayTitle = None
overlayButtons = {}
overlaySaved = False

#surface de validation de quitter
overlayQuit = None
overlayQuitCadre = None

#surface de validation de retour au menu
overlayMenu = None
overlayMenuCadre = None

#surface de validation de retour à l'édition du menu
overlayFail = None
overlayFailOk = None

#surface des boutons pour Oui/Non
overlayYesNo = None

#surfaces de l'écran de nouvelle partie
newGameBack = None
newGameTitle = None
newGameName = None
newGameButtons = {}
newGameInfo = {}
newGameSelectedInfo = "PTSI"

#surfaces de l'écran de nouvelle partie
chargeBack = None
chargeTitle = None
chargeName = None

#surfaces avant de quitter
quitSurf = None
quitPython = None
quitPygame = None
quitChaptal = None
quitTxt = {}

def initDraw(fenetre):
    #taille de l'écran
    global SCR_WIDTH , SCR_HEIGHT
    
    SCR_WIDTH  = fenetre.get_width()  / opt.SPRITE_SIZE
    SCR_HEIGHT = fenetre.get_height() / opt.SPRITE_SIZE
    
    #polices
    global menuFont , buttonFontXXS , buttonFontXS , buttonFontS , buttonFontM , buttonFontL
    menuFont = pygame.font.SysFont("vinerhanditc",120)
    buttonFontXXS= pygame.font.SysFont("chillernormal",30)
    buttonFontXS = pygame.font.SysFont("chillernormal",52)
    buttonFontS  = pygame.font.SysFont("chillernormal",72)
    buttonFontM  = pygame.font.SysFont("chillernormal",92)
    buttonFontL  = pygame.font.SysFont("chillernormal",120)
    
    #écran overlay
    global overlayBack , overlayTitle , overlayButtons
    
    overlayBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    overlayBack.fill( (128,128,128) )
    overlayBack.set_alpha(150)
    
    overlayTitle = menuFont.render("PAUSE",True,(250,20,20))
    
    overlayButtons = mouse.boutons["overlay"]
    overlayButtons["quitter"].surf      = buttonFontM.render("Quitter"     ,True,(20 ,20 ,20))
    overlayButtons["menu"].surf         = buttonFontM.render("Menu"        ,True,(20 ,20 ,20))
    overlayButtons["sauvegarder"].surf  = buttonFontM.render("Sauvegarder" ,True,(20 ,20 ,20))
    overlayButtons["sauvegarder"].surf2 = buttonFontM.render("Sauvegarder" ,True,(60 ,60 ,60))
    
    #validation de quittage de l'overlay, boutons Oui et Non
    global overlayYesNo
    overlayYes = elt.BoutonTexte( 0,0,10,10,10,(230,230,230),(120,120,120),buttonFontM,"Oui",(20,20,20) )
    overlayNo  = elt.BoutonTexte( 0,0,10,10,10,(230,230,230),(120,120,120),buttonFontM,"Non",(20,20,20) )
    overlayYes.setRight( -overlayNo.w )
    overlayNo.setLeft( overlayYes.w )
    overlayYesNo = elt.Cadre( fenetre.get_width()//2 , 0 , [ overlayYes,overlayNo ] )
    
    #validation de quittage de l'overlay et du jeu
    global overlayQuit
    textOverlayQuit = renderMultiLine(buttonFontS,texte.getTexte("overlay","confirmQ"),30,(10,10,10),(230,230,230))
    overlayQuit = elt.BoutonRempli(0,0,10,10,10,(230,230,230),textOverlayQuit,(120,120,120))
    overlayQuit.setCenterX( fenetre.get_width() //2 )
    overlayQuit.setCenterY( fenetre.get_height()//2 )
    
    #validation de quittage de l'overlay vers le menu
    global overlayMenu
    textOverlayMenu = renderMultiLine(buttonFontS,texte.getTexte("overlay","confirmM"),30,(10,10,10),(230,230,230))
    overlayMenu = elt.BoutonRempli(0,0,10,10,10,(230,230,230),textOverlayMenu,(120,120,120))
    overlayMenu.setCenterX( fenetre.get_width() //2 )
    overlayMenu.setCenterY( fenetre.get_height()//2 )
    
    #position des boutons oui et non
    top = fenetre.get_height()//2 + max( overlayQuit.h , overlayMenu.h )//2
    overlayYesNo.setTop(top)
    mouse.boutons["overlayV"]["oui"].linkElement(overlayYes)
    mouse.boutons["overlayV"]["non"].linkElement(overlayNo)
    
    #écran de menu
    global menuBack , menuTitle , menuButtons
    menuBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    menuBack.fill( (0,0,0) )
    
    menuTitle = menuFont.render("MENU",True,(250,20,20))
    
    menuButtons = mouse.boutons["menu"]
    menuButtons["quitter"].surf = buttonFontM.render("Quitter" ,True,(240,240,240))
    menuButtons["nouveau"].surf = buttonFontM.render("Nouveau" ,True,(240,240,240))
    menuButtons["option"].surf  = buttonFontM.render("Options" ,True,(240,240,240))
    menuButtons["charger"].surf = buttonFontM.render("Charger" ,True,(240,240,240))
    
    #écran d'option
    global optionBack , optionTitle
    optionBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    optionBack.fill( (0,0,0) )
    
    optionTitle = menuFont.render("Options",True,(250,20,20))
    
    #écran de nouveau jeu
    global newGameBack , newGameTitle , newGameButtons , newGameInfo , newGameName
    newGameBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    newGameBack.fill( (0,0,0) )
    
    newGameTitle = buttonFontM.render("Choisissez votre classe",True,(240,240,240))
    newGameName = elt.BoutonTexte( fenetre.get_width()//2,int(fenetre.get_height()*0.18),10,10,10,(0,0,0),(0,0,0),buttonFontM,"",(81,88,220) )
    newGameButtons = mouse.boutons["nouveau"]
    newGameButtons["PTSI"].setSurfCenterTop( buttonFontM.render("PTSI" ,True,(240,240,240)) )
    newGameButtons["PTSI"].surf2 = buttonFontM.render("PTSI" ,True,(120,120,120))
    newGameButtons["MPSI"].setSurfCenterTop( buttonFontM.render("MPSI" ,True,(240,240,240)) )
    newGameButtons["MPSI"].surf2 = buttonFontM.render("MPSI" ,True,(120,120,120))
    newGameButtons["PCSI"].setSurfCenterTop( buttonFontM.render("PCSI" ,True,(240,240,240)) )
    newGameButtons["PCSI"].surf2 = buttonFontM.render("PCSI" ,True,(120,120,120))
    newGameButtons["commencer"].setSurfCenterTop( buttonFontM.render("APB" ,True,(240,240,240)) )
    
    newGameInfo["PTSI"] = renderMultiLine(buttonFontS,texte.getTexte("nouveau","PTSI"),30,(240,240,240),(0,0,0) )
    newGameInfo["PCSI"] = renderMultiLine(buttonFontS,texte.getTexte("nouveau","PCSI"),30,(240,240,240),(0,0,0) )
    newGameInfo["MPSI"] = renderMultiLine(buttonFontS,texte.getTexte("nouveau","MPSI"),30,(240,240,240),(0,0,0) )
    
    #écran de nouveau jeu
    global chargeBack , chargeTitle , chargeName
    chargeBack = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    chargeBack.fill( (0,0,0) )
    
    chargeTitle = buttonFontM.render("Choisissez votre partie",True,(240,240,240))
    chargeName = elt.BoutonTexte( fenetre.get_width()//2,int(fenetre.get_height()*0.18),10,10,10,(0,0,0),(0,0,0),buttonFontM,"",(81,88,220) )
    
    #édition ratée du nom de la nouvelle sauvegarde
    global overlayFail , overlayFailOk
    textOverlayFail = renderMultiLine(buttonFontS,texte.getTexte("overlay","confirmF"),30,(10,10,10),(230,230,230))
    overlayFail = elt.BoutonRempli(0,0,10,10,10,(230,230,230),textOverlayFail,(120,120,120))
    overlayFail.setCenterX( fenetre.get_width() //2 )
    overlayFail.setCenterY( fenetre.get_height()//2 )
    
    #écran de sortie
    global quitSurf , quitPython , quitPygame , quitChaptal , quitTxt
    quitSurf = pygame.Surface( ( fenetre.get_width(),fenetre.get_height()) )
    quitSurf.fill( (0,0,0) )
    quitTxt["Chaptal"] = renderMultiLine(buttonFontXS,texte.getTexte("quit","chaptal"),30,(240,240,240),(0,0,0) )
    quitTxt["Python"]  = renderMultiLine(buttonFontXS,texte.getTexte("quit","python") ,30,(240,240,240),(0,0,0) )
    quitPython  = getLoaded("python.jpg",False)
    quitPygame  = getLoaded("pygame.png",False)
    quitChaptal = getLoaded("chaptal.jpg",False)

#dessine un texte sur plusieurs lignes
def renderMultiLine(font,text,spacing,color,backColor,align="center"):
    #crée les différentes surfaces
    lines = text.split("\n")
    surfaces = []
    totHeight,maxWidth = 0,0
    for t in lines:
        s = font.render(t,True,color)
        totHeight += s.get_height()
        maxWidth = max( maxWidth,s.get_width() )
        surfaces.append(s)
    #blitte les surfaces sur une seule surface commune
    totSurf = pygame.Surface( (maxWidth,totHeight+(len(lines)-1)*spacing) )
    totSurf.fill(backColor)
    h = 0
    for s in surfaces:
        if align == "center":
            totSurf.blit( s , ( (maxWidth-s.get_width())//2 , h ) )
        elif align == "left":
            totSurf.blit( s , ( 0 , h ) )
        h += s.get_height()+spacing
    return totSurf

#charge un sprite seul
def getLoaded(name,makeAlpha=True):
    try:
        s = pygame.image.load("sprites/"+name).convert()
    except Exception as e:
        s = pygame.Surface( (64,64) )
        s.fill( (255,255,255) )
    if makeAlpha:
        s.set_colorkey((255,255,255))
    return s
    
#charge les sprites animés d'un personnage
def loadAnimSprite(spriteName,directory):
    sprite = []
    sprited , spriteg , spriteb , spriteh = [] , [] , [] , []
    for i in range(8):
        sprited.append(getLoaded(directory+spriteName + "D" + str(i)+".png"))
        spriteg.append(getLoaded(directory+spriteName + "G" + str(i)+".png"))
        spriteb.append(getLoaded(directory+spriteName + "B" + str(i)+".png"))
        spriteh.append(getLoaded(directory+spriteName + "H" + str(i)+".png"))
        sprite.append(getLoaded(directory+spriteName + str(i+1)+".png"))
    sprites[spriteName] = sprite
    sprites[spriteName + "D"] = sprited
    sprites[spriteName + "G"] = spriteg
    sprites[spriteName + "B"] = spriteb
    sprites[spriteName + "H"] = spriteh

def loadStyle(styleName):
    sprites[styleName] = {}
    sprites[styleName]["sol"] = getLoaded( "Tiles/"+styleName+"/sol.bmp" )
    
    sprites[styleName]["mur"]    = []
    for i in range(8):
        sprites[styleName]["mur"].append( getLoaded( "Tiles/"+styleName+"/mur"+str(i+1)+".bmp" ) )
        
    sprites[styleName]["angleI"]  = []
    for i in range(8):
        sprites[styleName]["angleI"].append( getLoaded( "Tiles/"+styleName+"/angleInt"+str(i+1)+".bmp" ) )
        
    sprites[styleName]["angleE"]  = []
    for i in range(8):
        sprites[styleName]["angleE"].append( getLoaded( "Tiles/"+styleName+"/angleExt"+str(i+1)+".bmp" ) )
        
    sprites[styleName]["escalier"]  = []
    for i in range(12):
        sprites[styleName]["escalier"].append( getLoaded( "Tiles/"+styleName+"/escalier"+str(i+1)+".bmp" ) )

#charge tous les sprites utilisés dans le jeu en mémoire
def loadAllSprites():
    loadStyle("style1")
    
    #tapis
    sprites["tapis"]={}
    sprites["tapis"]["plat"]=[]
    sprites["tapis"]["angle"]=[]
    for i in range(8):
        sprites["tapis"]["plat"].append(  getLoaded( "Tiles/tapis"+str(i+1)+".bmp") )
        sprites["tapis"]["angle"].append( getLoaded( "Tiles/angle"+str(i+1)+".bmp") )
    sprites["tapis"]["plat"].append(  getLoaded( "Tiles/tapis9.bmp") )
    """
    #tapis
    sprites["escalier"]["TH"]  = getLoaded("Tiles/tapis_haut.bmp")
    sprites["escalier"]["TG"]  = getLoaded("Tiles/tapis_gauche.bmp")
    sprites["escalier"]["TB"]  = getLoaded("Tiles/tapis_bas.bmp")
    sprites["escalier"]["TD"]  = getLoaded("Tiles/tapis_droite.bmp")
    sprites["escalier"]["TM"]  = getLoaded("Tiles/tapis_milieu.bmp")
    
    sprites["escalier"]["mH"] = getLoaded("Tiles/mur_escalier_haut.bmp")
    sprites["escalier"]["mG"] = getLoaded("Tiles/mur_escalier_gauche.bmp")
    sprites["escalier"]["mB"] = getLoaded("Tiles/mur_escalier_bas.bmp")
    sprites["escalier"]["mD"] = getLoaded("Tiles/mur_escalier_droite.bmp")
    sprites["beton"]          = getLoaded("Tiles/beton.png")
    sprites["plancher"]       = getLoaded("Tiles/plancher.bmp")
    """
    sprites["planche"]        = getLoaded("Tiles/planche.bmp")
    
    sprites["eclair"] = getLoaded("eclair.bmp")
    sprites["stun"] = getLoaded("eclair.bmp")
    
    sprites["attackH"] = getLoaded("attackH.bmp")
    sprites["attackB"] = getLoaded("attackB.png")
    sprites["attackG"] = getLoaded("attackG.png")
    sprites["attackD"] = getLoaded("attackD.png")
    
    sprites["eclairH"] = getLoaded("hacheurH.png")
    sprites["eclairB"] = getLoaded("hacheurB.png")
    sprites["eclairG"] = getLoaded("hacheurG.png")
    sprites["eclairD"] = getLoaded("hacheurD.png")
    
    sprites["Laplace"] = getLoaded("Laplace.png")
    
    
    sprites["projectile"] = getLoaded("projectile.png")
        
    loadAnimSprite("gobelin","Ennemis/gobelin/")
    loadAnimSprite("orc"    ,"Ennemis/orc/"    )
    
    
#gère le décalage de l'écran à partir de la position du joueur
def centerOffset(player):
    global xOffset
    global yOffset
    
    reg = map.theMap.regionList[ player.position[0] ]
    
    #centrage si taille supèrieure à celle de l'écran
    #selon x
    if SCR_WIDTH > reg.width:
        xOffset = (SCR_WIDTH - reg.width)*opt.SPRITE_SIZE/2
    else:
        xOffset = ((SCR_WIDTH /2) - player.position[1] )*opt.SPRITE_SIZE
        if reg.width - player.position[1] < (SCR_WIDTH /2):
            xOffset = -(reg.width-SCR_WIDTH)*opt.SPRITE_SIZE
        if player.position[1] < (SCR_WIDTH /2):
            xOffset = 0
            
    #selon y
    if SCR_HEIGHT > reg.height:
        yOffset = (SCR_HEIGHT - reg.height)*opt.SPRITE_SIZE/2
    else:
        yOffset = ((SCR_HEIGHT/2) - player.position[2] )*opt.SPRITE_SIZE
        if reg.height - player.position[2] < (SCR_HEIGHT /2):
            yOffset = -(reg.height-SCR_HEIGHT)*opt.SPRITE_SIZE
        if player.position[2] < (SCR_HEIGHT /2):
            yOffset = 0

def drawMenu(fenetre):
    fenetre.blit( menuBack , (0,0) )
    fenetre.blit( menuTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-menuTitle.get_width()/2),0) )
    for k in menuButtons.keys():
        fenetre.blit( menuButtons[k].surf , (menuButtons[k].pX , menuButtons[k].pY) )

def drawOverlay(fenetre):
    fenetre.blit( overlayBack , (0,0) )
    fenetre.blit( overlayTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-overlayTitle.get_width()/2),0) )
    for k in overlayButtons.keys():
        if k == "sauvegarder" and overlaySaved:
            fenetre.blit( overlayButtons[k].surf2 , (overlayButtons[k].pX , overlayButtons[k].pY) )
        else:
            fenetre.blit( overlayButtons[k].surf , (overlayButtons[k].pX , overlayButtons[k].pY) )

def drawOverlayQuit(fenetre):
    overlayQuit.drawOn(fenetre)
    overlayYesNo.drawOn(fenetre)

def drawOverlayMenu(fenetre):
    overlayMenu.drawOn(fenetre)
    overlayYesNo.drawOn(fenetre)
    
def drawOverlayFail(fenetre):
    overlayFail.drawOn(fenetre)
    
def drawOption(fenetre):
    fenetre.blit( optionBack, (0,0) )
    fenetre.blit( optionTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-optionTitle.get_width()/2),0) )
    
def drawNewGame(fenetre):
    fenetre.blit( newGameBack, (0,0) )
    fenetre.blit( newGameTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-newGameTitle.get_width()/2),20) )
    newGameName.drawOn( fenetre )
    for k in newGameButtons.keys():
        if k == newGameSelectedInfo or k=="commencer":
            fenetre.blit( newGameButtons[k].surf , (newGameButtons[k].pX , newGameButtons[k].pY) )
        else:
            fenetre.blit( newGameButtons[k].surf2 , (newGameButtons[k].pX , newGameButtons[k].pY) )
    infoTxt = newGameInfo[newGameSelectedInfo]
    fenetre.blit( infoTxt , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-infoTxt.get_width()/2) ,int(SCR_HEIGHT*opt.SPRITE_SIZE*0.4) ) )
    
def drawCharge(fenetre):
    fenetre.blit( chargeBack, (0,0) )
    fenetre.blit( chargeTitle , (int(SCR_WIDTH*opt.SPRITE_SIZE/2-chargeTitle.get_width()/2),20) )
    chargeName.drawOn( fenetre )

def drawQuit(fenetre):
    fenetre.blit( quitSurf , (0,0) )
    fenetre.blit( quitTxt["Chaptal"] , (600,100) )
    fenetre.blit( quitTxt["Python"]  , (100,500) )
    fenetre.blit( quitChaptal, (100,100) )
    fenetre.blit( quitPython, (800,400) )
    fenetre.blit( quitPygame, (800,600) )

#dessine une région entière
def drawRegion(fenetre,regionName):
    #recupère le tableau
    region = map.theMap.regionList[regionName]
    #dessine les sols
    for x in range( region.width ):
        for y in range( region.height ):
            drawCase(fenetre,region,x+region.readOffset[0],y+region.readOffset[1])
    #dessine la case selectionnée
    if option.debugMode and debug.caseSel != [-1,-1]:
        xEcran = debug.caseSel[0] * opt.SPRITE_SIZE  + xOffset
        yEcran = debug.caseSel[1] * opt.SPRITE_SIZE  + yOffset
        pygame.draw.rect( fenetre , (250,250,250) , (xEcran,yEcran,64,64) )

#dessine un sprite seul d'une case
def drawCase(fenetre,region,x,y):
    xEcran = x * opt.SPRITE_SIZE  + xOffset
    yEcran = y * opt.SPRITE_SIZE  + yOffset
    
    #style de dessin
    drawStyle = region.style
    
    if region.at(x,y) == "v":
        pass
    elif region.at(x,y) == "s":
        fenetre.blit(sprites[drawStyle]["sol"] , (xEcran,yEcran))
    elif region.at(x,y) == "p":
        fenetre.blit(sprites[drawStyle]["sol"] , (xEcran,yEcran))
        fenetre.blit(sprites["planche"] , (xEcran,yEcran))
    elif region.at(x,y)[:1] == "m":
        num = int( region.at(x,y)[1:] )
        if num <= 8 and num >= 1:
            fenetre.blit(sprites[drawStyle]["mur"][num-1] , (xEcran,yEcran))
    elif region.at(x,y)[:1] == "a":
        num = int( region.at(x,y)[1:] )
        if num <= 8 and num >= 1:
            fenetre.blit(sprites[drawStyle]["angleI"][num-1] , (xEcran,yEcran))
    elif region.at(x,y)[:1] == "b":
        num = int( region.at(x,y)[1:] )
        if num <= 8 and num >= 1:
            fenetre.blit(sprites[drawStyle]["angleE"][num-1] , (xEcran,yEcran))
    elif region.at(x,y)[:1] == "e":
        num = int( region.at(x,y)[1:] )
        if num <= 8 and num >= 1:
            fenetre.blit(sprites[drawStyle]["escalier"][num-1] , (xEcran,yEcran))
    elif region.at(x,y)[:2] == "ta":
        num = int( region.at(x,y)[2:] )
        if num <= 8 and num >= 1:
            fenetre.blit(sprites["tapis"]["angle"][num-1] , (xEcran,yEcran))
    elif region.at(x,y)[:2] == "tm":
        num = int( region.at(x,y)[2:] )
        if num <= 9 and num >= 1:
            fenetre.blit(sprites["tapis"]["plat"][num-1] , (xEcran,yEcran))
    else:
        print("unregistered:",region.at(x,y) )
    
    """
    #sols
    if region.at(x,y) == 1:
        fenetre.blit(sprites["beton"] , (xEcran,yEcran))
    elif region.at(x,y) == 100:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
    #murs
    elif region.at(x,y) == 2:
        fenetre.blit(sprites["mur"]["H"] , (xEcran,yEcran))
    elif region.at(x,y) == 3:
        fenetre.blit(sprites["mur"]["HG"], (xEcran,yEcran))
    elif region.at(x,y) == 4:
        fenetre.blit(sprites["mur"]["G"] , (xEcran,yEcran))
    elif region.at(x,y) == 5:
        fenetre.blit(sprites["mur"]["BG"], (xEcran,yEcran))
    elif region.at(x,y) == 6:
        fenetre.blit(sprites["mur"]["B"] , (xEcran,yEcran))
    elif region.at(x,y) == 7:
        fenetre.blit(sprites["mur"]["BD"], (xEcran,yEcran))
    elif region.at(x,y) == 8:
        fenetre.blit(sprites["mur"]["D"] , (xEcran,yEcran))
    elif region.at(x,y) == 9:
        fenetre.blit(sprites["mur"]["HD"], (xEcran,yEcran))
    elif region.at(x,y) == 10:
        fenetre.blit(sprites["mur"]["HG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 11:
        fenetre.blit(sprites["mur"]["BG2"] , (xEcran,yEcran))
    elif region.at(x,y) == 12:
        fenetre.blit(sprites["mur"]["BD2"] , (xEcran,yEcran))
    elif region.at(x,y) == 13:
        fenetre.blit(sprites["mur"]["HD2"] , (xEcran,yEcran))
    #murs d'escaliers
    elif region.at(x,y) == 14:
        fenetre.blit(sprites["escalier"]["mH"] , (xEcran,yEcran))
    elif region.at(x,y) == 15:
        fenetre.blit(sprites["escalier"]["mG"] , (xEcran,yEcran))
    elif region.at(x,y) == 16:
        fenetre.blit(sprites["escalier"]["mB"] , (xEcran,yEcran))
    elif region.at(x,y) == 17:
        fenetre.blit(sprites["escalier"]["mD"] , (xEcran,yEcran))
    #planche
    elif region.at(x,y) == 18:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["planche"] , (xEcran,yEcran))
    #tapis
    elif region.at(x,y) == 19:
        fenetre.blit(sprites["escalier"]["TM"] , (xEcran,yEcran))
    #escaliers haut
    elif region.at(x,y) == 20:
        fenetre.blit(sprites["escalier"]["HD"] , (xEcran,yEcran))
    elif region.at(x,y) == 21:
        fenetre.blit(sprites["escalier"]["HG"] , (xEcran,yEcran))
    elif region.at(x,y) == 22:
        fenetre.blit(sprites["escalier"]["HM"] , (xEcran,yEcran))
    elif region.at(x,y) == 23:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 24:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 25:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["H_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 26:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TH"] , (xEcran,yEcran))
    #escaliers gauche
    elif region.at(x,y) == 30:
        fenetre.blit(sprites["escalier"]["GD"] , (xEcran,yEcran))
    elif region.at(x,y) == 31:
        fenetre.blit(sprites["escalier"]["GG"] , (xEcran,yEcran))
    elif region.at(x,y) == 32:
        fenetre.blit(sprites["escalier"]["GM"] , (xEcran,yEcran))
    elif region.at(x,y) == 33:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 34:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 35:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["G_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 36:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TG"] , (xEcran,yEcran))
    #escaliers bas
    elif region.at(x,y) == 40:
        fenetre.blit(sprites["escalier"]["BD"] , (xEcran,yEcran))
    elif region.at(x,y) == 41:
        fenetre.blit(sprites["escalier"]["BG"] , (xEcran,yEcran))
    elif region.at(x,y) == 42:
        fenetre.blit(sprites["escalier"]["BM"] , (xEcran,yEcran))
    elif region.at(x,y) == 43:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 44:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 45:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["B_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 46:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TB"] , (xEcran,yEcran))
    #escaliers droite
    elif region.at(x,y) == 50:
        fenetre.blit(sprites["escalier"]["DD"] , (xEcran,yEcran))
    elif region.at(x,y) == 51:
        fenetre.blit(sprites["escalier"]["DG"] , (xEcran,yEcran))
    elif region.at(x,y) == 52:
        fenetre.blit(sprites["escalier"]["DM"] , (xEcran,yEcran))
    elif region.at(x,y) == 53:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_D"] , (xEcran,yEcran))
    elif region.at(x,y) == 54:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_G"] , (xEcran,yEcran))
    elif region.at(x,y) == 55:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["D_M"] , (xEcran,yEcran))
    elif region.at(x,y) == 56:
        fenetre.blit(sprites["plancher"] , (xEcran,yEcran))
        fenetre.blit(sprites["escalier"]["TD"] , (xEcran,yEcran))
"""
#dessine le sprite d'un object JoueurBase
def drawPlayer(fenetre,player):
    x,y = player.position[1] , player.position[2]
    xEcran = (x-0.5) * opt.SPRITE_SIZE  + xOffset
    yEcran = (y-0.5) * opt.SPRITE_SIZE  + yOffset
    
    if player.direction == 4:
        fenetre.blit(sprites[player.spriteName + "D"][int(player.anim)%player.spriteNb], (xEcran,yEcran))
    elif player.direction == 8:
        fenetre.blit(sprites[player.spriteName + "G"][int(player.anim)%player.spriteNb], (xEcran,yEcran))
    elif player.direction == 2:
        fenetre.blit(sprites[player.spriteName + "B"][int(player.anim)%player.spriteNb], (xEcran,yEcran))
    elif player.direction == 6:
        fenetre.blit(sprites[player.spriteName + "H"][int(player.anim)%player.spriteNb], (xEcran,yEcran))
    else:
        fenetre.blit(sprites[player.spriteName][player.direction-1], (xEcran,yEcran))
    
    #affiche l'aura
    if player.auratimer > 0 :
        fenetre.blit(sprites[player.aura], (xEcran-150,yEcran))
        player.auratimer -= 1
    else:
        player.aura = ""
        
    
    #affiche la vie au dessus du sprite
    pygame.draw.rect( fenetre , (255,0,0) , (xEcran,yEcran-10,64,10) )
    pygame.draw.rect( fenetre , (0,255,0) , (xEcran,yEcran-10,64*player.hp/(100*player.lvl),10) )


def animAttack(fenetre,player):
    
    x,y = player.position[1] , player.position[2]
    xEcran = (x-0.5) * opt.SPRITE_SIZE  + xOffset
    yEcran = (y-0.5) * opt.SPRITE_SIZE  + yOffset
    
    if player.direction in [3,4]:
        fenetre.blit(sprites["attack" + "D"], (xEcran+1,yEcran))
    elif player.direction  in [7,8]:
        fenetre.blit(sprites["attack" + "G"], (xEcran-1,yEcran))
    elif player.direction in [1,2]:
        fenetre.blit(sprites["attack" + "B"], (xEcran,yEcran+1))
    elif player.direction  in [5,6]:
        fenetre.blit(sprites["attack" + "H"], (xEcran,yEcran-1))


def drawProjectile(fenetre,projectile):
    x,y = projectile.position
    xEcran = x * opt.SPRITE_SIZE  + xOffset
    yEcran = y * opt.SPRITE_SIZE  + yOffset
    
    fenetre.blit(sprites["projectile"],(xEcran,yEcran))


def drawCapacite(player,fenetre):
    xEcran = player.positionCapacite[0] * opt.SPRITE_SIZE  + xOffset
    yEcran = player.positionCapacite[1] * opt.SPRITE_SIZE  + yOffset
    fenetre.blit(sprites[player.spriteCapacite],(xEcran, yEcran))
        
    



    