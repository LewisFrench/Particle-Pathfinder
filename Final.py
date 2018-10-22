## Pygame Setup
import pygame
pygame.init()
import random
#Screen = pygame.display.set_mode((Width,Height))
Active = True
Clock = pygame.time.Clock()
#Used to calculate distance from the endcoord
import math
import sys

#Number of particles that will be generated per iteration
NumberOfParticles = 260

#Used to change the grid size later
#TileDimensionsList = [18 , 36, 72 , 90]


BackgroundColour = ((235,235,235))

##      DEFINING MENU ITEMS  ##
#General data structure / variable declaration
VectorList = []
BrushType = ""




Colour = ((235,235,235))
        #### FOR ALGORTIHM ####
AllNodes= []
##
pygame.display.set_caption("Particle Pathfinder")
#Height, Width = 1000,720


infoObject = pygame.display.Info()
Screen = pygame.display.set_mode((((infoObject.current_w, infoObject.current_h))), pygame.FULLSCREEN)

ResolutionList = [[1280 , 1024, [32,64,128 , 256]] , [1366, 768 , [32 , 48 , 64 , 96]] , [1440, 900 ,[45,60,90,100]	] , [1600 , 900 , [25,50,90,100]] , [1680, 1050 , [30 , 50 , 75 , 105]] , [1280 , 720 , [18 , 30 , 60, 72] ] , [1920 , 1080, [30 , 60 , 90 , 108]]]

GridHeight = infoObject.current_h
GridWidth  = infoObject.current_h

#Determines size of Grid based on monitor size
for i in ResolutionList:
    #If the size of the monitor is equal to a value in the list:
    if (infoObject.current_w, infoObject.current_h) == (i[0] , i[1]):
        #Set variables based on screen height
        GridWidth = infoObject.current_h
        GridHeight = infoObject.current_h
        #The list of tile dimensions in ResolutionList are loaded to be used to generate the grid
        TileDimensionsList = i[2]
        #TileDimensionsList =[32 , 48 , 64 , 96]


# Grid Setup
Height = infoObject.current_h
Width = infoObject.current_w

TileDimensions = TileDimensionsList[1]
#Screen = pygame.display.set_mode((Height , Width))
Active = True
Clock = pygame.time.Clock()

NewLine = 0
CentreWidth = ((GridWidth +(Width -GridWidth)/2)-20)

#Font Setup
MyFont =  pygame.font.SysFont("Calibri", 12)
HelpFont =  pygame.font.SysFont("Calibri", 10)
OptionFont = pygame.font.SysFont("Calibri" , 16)
        #### FOR ALGORTIHM ####

Mouse = pygame.mouse.get_pos()


#Setting format for list used to determine particle movement later
    # second and third values are the x and y components of each direction
FullThing = [['NW',-1,-1] , ['N',0,-1] , ['NE',1,-1] , ['W',-1,0] , ['E',1,0] , ['SW',-1,1] , ['S',0,1] , ['SE',1,1]]
#   FullThing[0]     =    VectorDir
#   FullThing[1]     =    x Vel
#   FullThing[2]     =    y Vel




# Boolean determining whether particles are spawned
ParticleBool = False


TileGroup = pygame.sprite.Group()

#####################
#Setup of data structures for the BFS algorithm
HeuristicValue = 0
NeighbourList = []
ProcessedList = []
ImpassableNodes = []
NodesToSearch = []
ImpassableList = []
TileList = []
####################

# A variable necessary when placing tiles using the slider. Variable must be inversely large relative to tile dimensions
RowQuantity = GridWidth / TileDimensions

#Looking back this seems a bit redundant considering I have FullThing with both of these earlier, but there's probably a reason for it
DirectionList = [ 'NW' , 'N' , 'NE' , 'W', 'E' , 'SW' , 'S' , 'SE']
Directions = [[-1,-1] , [0,-1] , [1,-1] , [-1,0] , [1,0] , [-1,1] , [0,1] , [1,1]]
ValidPath = False
def FindNeighboursVector(TileList):
    global ValidPath
    global Directions
    global StartCoords
    global DirectionList
    global ParticleBool
    global VectorList
    global EndCoords
    #Vectorlist is used throughout, Unvalidated is local
    VectorList = []
    #Unvalidated = []
    #TileList is a list of all tiles
    ValidPath = False
    for Node in TileList:
            Unvalidated = []
            #If the tile is traversable, a coordinate showing its x,y values are added to Unvalidated
            if Node not in ImpassableNodes:
                for y in Directions:
                        Coord = ((y[0] * TileDimensions) + Node.rect.x), ((y[1] * TileDimensions) + Node.rect.y)
                        Unvalidated.append(Coord)
                Neighbours = []
                #Validateds the node by checking it is in ALlNodes, which holds all feasible nodes
                for i in Unvalidated:
                    if i in AllNodes:
                        #Added to Neighbours
                         Neighbours.append(i)
                    else:
                        #This is necessary as when a tile was nect to the border, it would have at least 3 fewer neighbours
                        #this would mean the vector given was skewed and the program woudn't move the particles properly when the hit the border
                        Neighbours.append("")
                for i in Neighbours:
                    for y in TileList:
                        # Finds the position of the coordinates of each tile in Neighbours and gives it a numerical value based on its position in the list
                        if (y.rect.x, y.rect.y) == i:
                            Neighbours[Neighbours.index(i)] = y.Value


            #DirectionList = [ 'NW' , 'N' , 'NE' , 'W', 'E' , 'SW' , 'S' , 'SE']
            # Make it so it does the reverse vector when its just the two diagonal nodes
            for i in Neighbours:
                if i == '':
                    i = 1000
            if Neighbours[1] == '' and Neighbours[3] == '' :#and Neighbours[0] !='' and Neighbours[7]!='' :
                #Node.Vector = 'SE'
                Neighbours[0] = 1000
            if Neighbours[1] == '' and Neighbours[4] == '' :#and Neighbours[2] !='' and Neighbours[5] !='' :
                #Node.Vector = 'SW'
                Neighbours[2] = 1000
            if Neighbours[3] == '' and Neighbours[6] =='' :#and Neighbours[5] != '' and Neighbours[2] != '':
                #Node.Vector = 'NE'
                Neighbours[5] = 1000
            if Neighbours[4] == '' and Neighbours[6] =='': #and Neighbours[7] !='' and Neighbours[0] !='':
                #Node.Vector = 'NW'
                Neighbours[7] = 1000
            if Node.Title == "Wall":
                Node.Vector = ''
            Node.Vector = DirectionList[Neighbours.index(min(Neighbours))]
            if Node.Title == "Wall":
                Node.Vector = ''
#           #           #           #           #           #           #           #           #           #

            #Creates a variable used to place particles based on the x and y coordinates of the origin node
            if Node.Title == "Start":
                    StartCoords =(((Node.rect.x ) , (Node.rect.y)))
                    #It didn't work without this and it works with it
                    GlobalStartCoords()
            #Sets the end coordinates
            if Node.Title == "EndNode":
                    Node.Vector = ''
                    #Node.image = pygame.image.load("EndNode.png").convert()
                    EndCoords =((((Node.rect.x)+20) , ((Node.rect.y)+20)))
            #Creates a list called Vectorlist with all the necessary information used to facilitate the generation of particles
            for y in FullThing:
                if Node.Vector ==y[0] or Node.Title == "EndNode":
                    Information = (Node.rect.x , Node.rect.y,Node.Vector, y[1] , y[2], Node.Title)
                    VectorList.append(Information)
    #Triggers the procedure that creates the particles
    for i in TileList:
        if i.Title=='Start':
            if i.Value != 1000:
                ValidPath = True

    if ValidPath==True:
        ParticleBool = True
        SpawnParticles()


#           #           #           #           #           #           #           #           #           #

StartCoods = ''
def GlobalStartCoords():
    global StartCoords
    if StartCoods != '':
        return StartCoords

def ResetTerrain(TileList):
    global WallPresent
    global ImpassableList
    global ImpassableNodes
    #Changes all wall tiles in the list of tile class objects into regular tiles
    for i in TileList:
                if i.Title == "Wall":
                    i.Title = ""
                  #  ImpassableNodes.remove(Coord)
                    ImpassableList = []
                    ImpassableNodes = []
                    i.Colour = ((235,235,235))
            #sets its image back to normal
#            i.image = pygame.image.load("Clear.png").convert()
    WallPresent = False

PresetInterval = (GridWidth-200)/5
class Preset1(pygame.sprite.Sprite):
    def __init__(self):
        super(Preset1, self).__init__()
        self.image = pygame.image.load("Preset1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = GridWidth - 300
        self.rect.y = 100+PresetInterval
    def update(self, Mouse):
        if self.rect.collidepoint(Mouse):
            ResetTerrain(TileList)
            Preset = 1
            GeneratePresets(RowQuantity,Preset )


class Preset2(pygame.sprite.Sprite):
    def __init__(self):
        super(Preset2, self).__init__()
        self.image = pygame.image.load("Preset2.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = GridWidth - 300
        self.rect.y = 100+(PresetInterval*2)
    def update(self, Mouse):
        if self.rect.collidepoint(Mouse):
            ResetTerrain(TileList)
            Preset = 2
            GeneratePresets(RowQuantity, Preset)


class Preset3(pygame.sprite.Sprite):
    def __init__(self):
        super(Preset3, self).__init__()
        self.image = pygame.image.load("Preset3.png").convert()
        self.rect = self.image.get_rect()
        self.rect.y = 100 + (PresetInterval*3)
        self.rect.x = GridWidth - 300
    def update(self, Mouse):
        if self.rect.collidepoint(Mouse):
            Preset = 3
            ResetTerrain(TileList)
            GeneratePresets(RowQuantity, Preset)



WallPresent = False
class ResetButton(pygame.sprite.Sprite):
    def __init__(self):
        super(ResetButton, self).__init__()
        self.image = pygame.image.load("Clear.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = CentreWidth + 94
        self.rect.y = 590
    def update(self):
        global WallPresent
        global Mouse
        global TileList
        global ImpassableList
        global ImpassableNodes

        #If there is a wall tile located in the grid, the image will change to show this
        if WallPresent == True:
            self.image = pygame.image.load("NotClear.png").convert()
            WallPresent = False
        else:
            self.image = pygame.image.load("Clear.png").convert()
        if self.rect.collidepoint(Mouse[0], Mouse[1]):
            ResetTerrain(TileList)




def FindNeighbours(NodesToSearch):
    global ProcessedList
    #global HeuristicValue
    TempList = []
    #for each node surroinding the node being searched:
    for i in NodesToSearch:
        #Added to a list containing all processed nodes
        ProcessedList.append(i)
        #If tile is traversable
        if i not in ImpassableNodes:
            #Generates the coordinates of its immediate neighbours, not including those diagonally
            Directions = [[0 , -1] , [-1 , 0], [1 , 0], [0 , 1] ]
            for y in Directions:
                    Coord = ((y[0] * TileDimensions) + i[0]), ((y[1] * TileDimensions) + i[1])
                    if Coord not in ImpassableNodes:
                            TempList.append(Coord)
    #Resets the list of nodes to search, fills it with all the nodes surrounding all the nodes that were set to be searched at the beginning of the procedure
    NodesToSearch = []
    for i in TempList:
        if i not in NodesToSearch:
            if i in AllNodes:
                if i not in ProcessedList:
                    NodesToSearch.append(i)

    return NodesToSearch


# Talk about what happened at this point  20x20 = 40 , 40x40 tiles --> multiplier = 20
#Multiplier is used as larger tiles will be fewer in number, therefore variables used to navigate lists must be different
#Like RowQuantity, this must be inversely sized with the particle, but to a larger degree here as it is used to index a list
def SetValues(NodesToSearch):
    global TileList
    global TileDimensions
    global Multiplier
    Multiplier = GridWidth/TileDimensions
    for i in NodesToSearch:
        Index = ((i[0]/TileDimensions) + (i[1]/TileDimensions)*Multiplier)

        TileList[Index].Value = HeuristicValue


#Generates the colours used to show the distance of a tile from the goal node
def SetHeatmap(TileList):
    #255 used to each tile has a unique colour. any lower and multiple ((0,0,0)) occur, and higher and multiple ((255,255,255))'s
    ColourIntensity = 255
    # the heuristic values of the tiles are added to a list, the largest is found and called Val
    AllVals = []
    for i in TileList:
        if i.Value not in AllVals:
            if i.Value != '' and i.Value >1:
                AllVals.append(i.Value)
    if AllVals == []:
        pass
    else:
        Val = (max(AllVals))
        #An interval is generated with using Val such that all colours are within the range, as no value will be larger than Val
        Interval  = ((ColourIntensity)/((Val*0.9)))
    ##    if Interval>235:
    ##        Interval = 235
        #Gives each traversable, non-start-or-end tile a colour based on their value. The stronger colours are nearer to the goal
        for i in TileList:
            if i.Value !="":
                i.ColourVar = (Interval*(i.Value))
                if i.ColourVar > 245:
                    i.ColourVar = 245
                elif i.ColourVar < 10:
                    i.ColourVar = 10
                #Prevents colours from being too light or dark




#Used to display labels to help the user
HelpBool = False
class Help(pygame.sprite.Sprite):
    def __init__(self):
        super(Help, self).__init__()
        self.image = pygame.image.load('HelpButton.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = CentreWidth-20
        self.rect.y = 720
        self.image.set_colorkey((255,255,255))
        HelpBool = False
    def update(self):
        global Mouse
        global HelpBool
        #Changes the state of HelpBool
        if self.rect.collidepoint(Mouse):
            if HelpBool == True:
                HelpBool = False
            else:
                HelpBool = True



#Sets the checkbox generation function up
BoxCount= 0
State = "Checked"

class CheckBox(pygame.sprite.Sprite):
    def __init__(self):
        global BoxCount
        super(CheckBox, self).__init__()

        #Uses a function to generate the unique purpose and state of each checkbox, so it may be indexed from a list and used for different purposes within the program
        self.Purpose = ""
        y, Purpose = GetInfoCheckBox(BoxCount)
        self.image = pygame.image.load("Checked.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = CentreWidth + 100
        self.rect.y = y
        self.Purpose = Purpose
        # I chose these to be un-defaulted as they're intrusive
        if self.Purpose == 'HeatMap' or self.Purpose =='ParticleBorders':
            self.image = pygame.image.load("Unchecked.png").convert()
            self.State = 'Unchecked'
        global State
        self.State = State
    def update(self):
        global Mouse
        # Switches between states of yes and no when clicked
        if self.rect.collidepoint(Mouse[0], Mouse[1]):
            if self.State == "Unchecked":
                self.image = pygame.image.load("Checked.png").convert()
                self.State = "Checked"
            else:
                self.image = pygame.image.load("Unchecked.png").convert()
                self.State = "Unchecked"

# Alloctes an extra 30 pixels in the y direction per checkbox, returns to class object contructor
def GetInfoCheckBox(BoxCount):
    y = (BoxCount*30) + 500
    if BoxCount ==0:
        Purpose = 'GridLines'
    elif BoxCount == 1:
        Purpose = 'HeatMap'
    else:
        Purpose = 'ParticleBorders'
    return y, Purpose

SliderStart = 0
#Used mostly as a static image on which Pointer is interacted with
class Slider(pygame.sprite.Sprite):
    def __init__(self):

        super(Slider, self).__init__()
        global SliderStart
        self.image = pygame.image.load("Slider.png").convert()

        self.image.set_colorkey((255,255,255))
        self.Value = SliderCount
        self.rect= self.image.get_rect()
        if self.Value == 0:
            self.rect.x = CentreWidth - 40
            SliderStart = self.rect.x
            self.rect.y = 660

    def CheckDrag(self):
        global Drag
        global Mouse
        #Sets 'Drag', a boolean used to determine whether the user is trying the change the grid dimensions, to true or false

        if self.rect.collidepoint(Mouse):
            Drag = True
        else:
            Drag = False

    def update(self):
        pass




QuantityDrag = False
ControlDrag = False
SpeedDrag = False

class ClearSlider(pygame.sprite.Sprite):
    def __init__(self):
        super(ClearSlider, self).__init__()
        self.image = pygame.image.load("Clear Slider.png").convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.Purpose = ""

    def CheckDrag(self, Mouse):
        global QuantityDrag
        global ControlDrag
        global SpeedDrag
        global OptionsBool
        if 100 <= Mouse[0] <= 400 and OptionsBool == True:  # and event.type == pygame.MOUSEBUTTONDOWN:
            if 100 <= Mouse[1] <= 100 + (3*Distance):
                if QuantityDrag == True:
                    QuantityDrag = False
                else:
                    QuantityDrag = True
            if 200 <= Mouse[1] <= 200 + 3*Distance:
                if ControlDrag == True:
                    ControlDrag = False
                else:
                    ControlDrag = True
            if 300 <= Mouse[1] <= 300 + 3*Distance:
                if SpeedDrag == True:
                    SpeedDrag = False
                else:
                    SpeedDrag = True


Distance = GridWidth/20

class ClearPointer(pygame.sprite.Sprite):
    def __init__(self):
        super(ClearPointer, self).__init__()
        self.image = pygame.image.load("Clear Pointer.png").convert()
        self.image.set_colorkey((255,255,255))
        self.Purpose = ""
        self.rect = self.image.get_rect()
        self.rect.x = 180 + Distance


    def update(self, Mouse, QuantityDrag, ControlDrag, SpeedDrag):
        global NumberOfParticles
        global ControlUpper
        global ControlLower
        global SpeedMultiplier
        global VelocityLower
        global VelocityUpper
        if QuantityDrag == True:# and self.Purpose == 'ParticleQuantity':
            Index = 0
            ControlDrag = False
            SpeedDrag = False
        elif ControlDrag == True:
            Index = 1
            QuantityDrag = False
            SpeedDrag = False
        elif SpeedDrag == True:
            Index = 2
            QuantityDrag = False
            ControlDrag = False
        ClearPointerList[Index].rect.x = Mouse[0]
        if 100+Distance > ClearPointerList[Index].rect.x:
                ClearPointerList[Index].rect.x = 100+Distance
        elif ClearPointerList[Index].rect.x > 264 + Distance:
                ClearPointerList[Index].rect.x = 264 + Distance

        NumberOfParticles = (((ClearPointerList[0].rect.x)-138)*(int(TileDimensions/18)))+1


        CentreDistance = ClearPointerList[1].rect.x - 214
        ControlUpper = int(400+(CentreDistance *1.2))
        ControlLower = int(100+(CentreDistance*0.8))

        SpeedDistance = ClearPointerList[2].rect.x -214
        VelocityLower = (40 + SpeedDistance/6)
        VelocityUpper = (70 + SpeedDistance/8)




# Define Option Labels
QuantityLabel = OptionFont.render((str(NumberOfParticles)), 4, ((100,100,100)))
QuantityTextLabel = MyFont.render(("N u m b e r   o f   P a r t i c l e s "), 4 , (100,100,100))

ControlLabel = MyFont.render (("P a r t i c l e    C o n t r o l"), 4, (100,100,100))

SpeedLabel = MyFont.render(("P a r t i c l e   S p e e d"), 4, (100,100,100))


SchemeLabel = MyFont.render(("H e a t m a p   C o l o u r"), 4 , (100,100,100))

PresetLabel =MyFont.render(("L o a d   P r e s e t s") , 4 , (100,100,100))


ExtraDistance = 100 + Distance

def DrawOptionLabels(QuantityLabel, QuantityTextLabel, ControlLabel, SpeedLabel, SchemeLabel, PresetLabel):
    global NumberOfParticles
    QuantityLabel = OptionFont.render((str(NumberOfParticles)), 4, ((100,100,100)))
    global ExtraDistance
    Screen.blit(QuantityLabel, (300+Distance,Distance+103))
    Screen.blit(QuantityTextLabel , ((ExtraDistance+10, ExtraDistance+30)))


    Screen.blit(ControlLabel , (ExtraDistance+30 , ExtraDistance+130))
    Screen.blit(SpeedLabel , (ExtraDistance + 30 , ExtraDistance + 230))

    Screen.blit(SchemeLabel, (ExtraDistance + 20, GridWidth - 280))

    Screen.blit(PresetLabel , (GridWidth-307, 60+PresetInterval))



#Drag is set to False by default
Drag = False

#Slider() is used to check for drag, as it is larger and easier to click
#also means users can click on their desired intervals rather than having to drag, though both are available
class SizePointer(pygame.sprite.Sprite):
    def __init__(self):
        super(SizePointer,self).__init__()
        global SliderStart
        self.image = pygame.image.load('Pointer.png').convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = SliderStart + 33
        self.rect.y = 662

    def update(self):
        global TileDimensionsList
        global Mouse
        global TileDimensions
        if Drag == True:
            self.rect.x = Mouse[0]
            #Keeps the pointer within the imaginary boundary of the slider
            if not SliderStart <= self.rect.x <= SliderStart + 106:
                if self.rect.x < SliderStart:
                    self.rect.x = SliderStart + 2
                if self.rect.x > SliderStart + 106:
                    self.rect.x = SliderStart + 105
        #When the pointer is let go:
        if Drag == False:
            Intervals = [[SliderStart , SliderStart + 20 , SliderStart+1] , [SliderStart + 21 , SliderStart + 54 , SliderStart + 33] , [SliderStart + 55 , SliderStart + 85 , SliderStart + 72] , [SliderStart + 86 , SliderStart+110 , SliderStart + 108]]
            # If the pointer is let go, it snaps to the boundary it is nearest to
            for i in Intervals:
                #Parameters made wider than slider itself due to the need for mouse to be off-rect for pointer to go to edges
                if i[0] <= self.rect.x <= i[1] and (630 <=Mouse[1] <=680) and (GridWidth <= Mouse[0] <= Width):
                    #sets its x coordinate to the interval by judging the approximation by the user
                    self.rect.x = i[2]
                    #If the grid size is changed, all particles are removed from the screen, as no vectors will be generated
                    ParticleGroup.empty()
                    #The Tile dimensions are generated using a list of the length of the sides of the tiles, which line up with the positions on the slider
                    TileDimensions = TileDimensionsList[Intervals.index(i)]
                    #This is then used to generate the grid
                    SetGridDimensions()





# FullThing = [['NW',-1,-1] , ['N',0,-1] , ['NE',1,-1] , ['W',-1,0] , ['E',1,0] , ['SW',-1,1] , ['S',0,1] , ['SE',1,1]]
def DrawVectorDirections(TileList, TileDimensions, FullThing):
    StartPoint = 0
    EndPoint = 0
    for i in TileList:
        if i.Vector != "":
            StartPoint = ((i.rect.x+TileDimensions/2) , (i.rect.y + TileDimensions/2))
            for y in FullThing:
                if y[0] == i.Vector:
                    EndX = (i.rect.x + TileDimensions/2) + y[1]*10
                    EndY = (i.rect.y + TileDimensions/2) + y[2]*10
                    EndPoint = (EndX, EndY)
        if StartPoint + EndPoint != 0:
            pygame.draw.line(Screen, ((75,75,75)), (StartPoint), (EndX, EndY) , 2)


## Created so that the slider can be updated every frame rather than every click when being dragged by the mouse
#SizePointerGroup is separate as it will be called every clock iteration when being dragged
#the other UI elements in MiscGroup will only be updated when clicked
SizePointerGroup = pygame.sprite.Group()
MiscGroup = pygame.sprite.Group()
#Created to more easily change the state of the three checkboxes
CheckBoxList = []


# Adds the checkboxes , BoxCount is used to offset the Y coordinates so I can add more easily in future
checkbox = CheckBox()
for i in range (3):
    checkbox = CheckBox()
    MiscGroup.add(checkbox)
    CheckBoxList.append(checkbox)
    BoxCount +=1

# I only wanted grid regions to be defaulted, as it's less intrusive than the others
CheckBoxList[1].State = 'Unchecked'
CheckBoxList[2].State = 'Unchecked'


#Adding other UI elements into MiscGroup
reset = ResetButton()
MiscGroup.add(reset)

help = Help()
MiscGroup.add(help)

OptionsGroup = pygame.sprite.Group()
OptionsExtraGroup = pygame.sprite.Group()

ClearSliderList = []
ClearPointerList = []


for i in range(3):
    clearslider = ClearSlider()
    OptionsGroup.add(clearslider)
    ClearSliderList.append(clearslider)

for i in range(3):
    clearpointer = ClearPointer()
    OptionsExtraGroup.add(clearpointer)
    ClearPointerList.append(clearpointer)

preset1 = Preset1()
OptionsGroup.add(preset1)

preset2 = Preset2()
OptionsGroup.add(preset2)

preset3 = Preset3()
OptionsGroup.add(preset3)


def SetPurpose(ClearSliderList, ClearPointerList):
    Distance = GridWidth/20
    # Slider 1
    #   #   #   #   #   #   #
    ClearSliderList[0].Purpose = "ParticleQuantity"
    ClearSliderList[0].rect.x = 100 + Distance
    ClearSliderList[0].rect.y = 100 + Distance

    ClearPointerList[0].Purpose = "ParticleQuantity"
    ClearPointerList[0].rect.y = 102 + Distance
    #   #   #   #   #   #   #

    # Slider 2
    #   #   #   #   #   #   #
    ClearSliderList[1].Purpose = "ParticleControl"
    ClearSliderList[1].rect.x = 100 + Distance
    ClearSliderList[1].rect.y = 200 + Distance

    ClearPointerList[1].Purpose = "ParticleControl"
    ClearPointerList[1].rect.y = 202 + Distance
    #   #   #   #   #   #   #

    # Slider 3
    #   #   #   #   #   #   #
    ClearSliderList[2].Purpose = "ParticleSpeed"
    ClearSliderList[2].rect.x = 100 + Distance
    ClearSliderList[2].rect.y = 302 + Distance

    ClearPointerList[2].Purpose = "ParticleSpeed"
    ClearPointerList[2].rect.y = 302 + Distance
    #   #   #   #   #   #   #

SetPurpose(ClearSliderList, ClearPointerList)


SliderCount = 0
slider = Slider()
MiscGroup.add(slider)


pointer = SizePointer()
SizePointerGroup.add(pointer)


#   #   #   #   #   #   #   #   #   #   #

SpeedMultiplier = 1
# I used colour scheme as grey as it contrasts the white particles the best
ColourScheme = 'Grey'

DrawOutlines = True

#declared here to be changed later in order to use to help particle movement
# Boundaries for values based on trial and error
EndCoords = (0,0)
VelocityLower = 40
VelocityUpper = 70
ControlBoundary = (100,400)
ControlLower = 100
ControlUpper = 400
#Class for the particle function
class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super(Particle, self).__init__()
        global ColourScheme
        global VelocityLower
        global VelocityUpper
        #Object is set as an invisible black square to maintain calculations based on the 10x10 nature
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey((0,0,0))
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect()
        self.Colour = ((0,0,0))
        self.xVelocity = 0
        self.yVelocity = 0
        #Generates a random velocity limit for the particles to add more variety in movement
        self.VelocityLimit = (float(random.randint(VelocityLower, VelocityUpper))/10)
        StartCoordinates = GlobalStartCoords()
        # Generates a random offset within starting node to prevent uniformity in spawn
        self.xOffset = random.randint(1,TileDimensions - 6)
        self.yOffset = random.randint(1,TileDimensions - 6)

        #Gives each particle a slightly varying level of control when affected by tile vectors
        #self.Control = random.randrange(100,400, 1)
        self.Control = random.randrange(ControlLower, ControlUpper,1)
        if ColourScheme == 'Grey':
            self.Colour = ((255,255,255))
    # Generates the starting coordinates for each particle
    def SetSpawn(self):
        global StartCoords
        self.rect.x = StartCoords[0] + self.xOffset
        self.rect.y = StartCoords[1] + self.yOffset

    def CollisionDetect(self):
        # I will improve this function, as it still has issues
        # two variables are set to check if a particle collides with a wall in the x or y direction
        global ImpassableList
        self.xCollide = 0
        self.yCollide = 0
        self.CornerX = False
        self.CornerY = False
        self.xDestination = self.rect.x + self.xVelocity
        self.yDestination = self.rect.y + self.yVelocity
        #   Explain why you chose 7 , velocity limit is 6 and closes a particle can get is the boundary.
        #If Particle is moving:
        if self.xVelocity!=0 and self.yVelocity!=0:
            #Each wall tile in the list of impassable tiles is indexed
            for i in ImpassableList:
                #checks if it comes into contact with the particle
                if i.rect.collidepoint(self.xDestination,self.yDestination):
                    # if the particle is set to collide with the left side of the tile, xCollide is set to one
                    if i.rect.collidepoint(self.xDestination , self.yDestination):
                        if self.xDestination <= (i.rect.x + TileDimensions/1.3) and (i.rect.y <= self.rect.y <= i.rect.y + TileDimensions):  #  From LEFT
                            self.xVelocity = -1
                            self.rect.x -=1
                        if self.xDestination >= (i.rect.x + TileDimensions/1.3) and (i.rect.y <= self.rect.y <= i.rect.y + TileDimensions): # From RIGHT
                            self.xVelocity = 1
                            self.rect.x+=1
                            self.CornerX = True
                        if self.yDestination <= (i.rect.y + TileDimensions/1.3) and (i.rect.x <= self.rect.x <= i.rect.x + TileDimensions): # From TOP
                            self.yVelocity = -1
                            self.rect.y -=1
                            self.CornerY = False
                        if self.yDestination >= (i.rect.y + TileDimensions/1.3) and (i.rect.x <= self.rect.x <= i.rect.x + TileDimensions): # From BOTTOM
                            self.yVelocity = 1
                            self.rect.y+=2
                            self.CornerY = True



                    if self.CornerX == True and self.CornerY == True:
                        self.rect.x +=4
                        self.rect.y +=1

                        self.xVelocity = 2
                        self.yVelocity = 2


        return self.xVelocity, self.yVelocity

    def update(self):

        #global VelocityLimit
        #self.image.blit(self.image , (self.x, self.y))
        self.centre = ((self.rect.x + 5), (self.rect.y + 5))
        #Returns the velocity value from the particlemovement function using the centre of the particle as a reference
        self.xVelocity, self.yVelocity = self.ParticleMovement(self.centre[0] , self.centre[1])
        # Returns the velocity after checking if any collisions were set to occue
        self.xVelocity, self.yVelocity = self.CollisionDetect()

#               Validation (Outsource to separate procedure??)
        #Keeps the velocity of the particles within their designated velocity limit
        if not -self.VelocityLimit < self.xVelocity < self.VelocityLimit :
            if self.xVelocity < 0:
                self.xVelocity = -self.VelocityLimit
            else:
                self.xVelocity = self.VelocityLimit
        if not -self.VelocityLimit < self.yVelocity < self.VelocityLimit :
            if self.yVelocity < 0:
                self.yVelocity = -self.VelocityLimit
            else:
                self.yVelocity = self.VelocityLimit
        #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #



        # Keeps the particles within the grid
        #790 is used as the particle is 10 pixels wide, meaning no part of it will leave the grid
        #The same bounce mechanic is used as in collisiondetect()
        if not 0 < self.rect.x <GridWidth - 10:
            if self.rect.x > GridWidth - 10:
                self.xVelocity = -1
            elif self.rect.x < 0:
                self.xVelocity = 1
        if not 0 < self.rect.y < GridWidth - 10:
            if self.rect.y > GridWidth - 10:
                self.yVelocity = -1
            elif self.rect.y < 0:
                self.yVelocity = 1


        #Adds the calculated unique velocity limit to the x and y values of the particle
        self.rect.x += self.xVelocity
        self.rect.y += (self.yVelocity)

        #Draws the ellipse on to the surface constructor
        pygame.draw.ellipse(self.image,((255,255,255)),[0,0,10,10] , 0)

        #if the user chooses to show a border to help differentiate particles, a second, unfilled circle is drawn as a border
        if CheckBoxList[2].State == 'Checked':
            pygame.draw.ellipse(self.image,((40,40,40)),[0,0,10,10] , 1)
        # I had a small but where if the borders were turned on then off, small residual ugly borders remained
        # the else conditions draws over them with a white outline instead
        #Does not affect the size of the particle
        else:
            pygame.draw.ellipse(self.image,((255,255,255)),[0,0,10,10] , 1)

    # Point of analysis: optimised mivement by writing more optimised code.
    def ParticleMovement(self,x,y):
        global VectorList
        global EndCoords
        StartCoords = GlobalStartCoords()
        #Created in order to prevent an annoying feature of the program
        #Around the end node, all vectors would point in such a way that most particles would end up circline the end without getting there
        self.Distance = math.sqrt(((self.rect.x - EndCoords[0])**2) +((self.rect.y - EndCoords[1])**2))
        for i in VectorList:
            if (i[0]<= x <= i[0]+TileDimensions) and (i[1] <= y <= i[1] + TileDimensions):
                # Point of analysis, did this so particle movement is less uniform. self.Control is how much control the particle has, i.e how much it is affected by a changing vector.
                #Used to increase how influenced by vector directions a partile is, so it will be driven into the endnode, where it slows down

                if self.Distance < 90:

                    self.xVelocity  += ((i[3])*(float('0.'+str(self.Control)))*(self.Distance/90))
                    self.yVelocity +=  ((i[4])*(float('0.'+str(self.Control)))*(self.Distance/90))
                else:
                    self.xVelocity  += (i[3]*(float('0.'+str(self.Control))))
                    self.yVelocity +=  (i[4]*(float('0.'+str(self.Control))))
                if i[-1] == "EndNode":
                    self.xVelocity *=0.98
                    self.yVelocity *=0.98
        return (self.xVelocity), (self.yVelocity)


#Used to show the grid lines
def GenerateTileIntervals():
    global TileIntervals
    TileYIntervals = []
    TileXIntervals = []
    TileIntervals = []
    #Finds the x and y coordinates of tiles and adds them to their respective lists
    for i in TileList:
            LineXCoords = [[i.rect.x, 0] , [i.rect.x, GridHeight]]
            LineYCoords = [[0 , i.rect.y], [GridWidth , i.rect.y]]
            if LineXCoords not in TileIntervals:
                TileIntervals.append(LineXCoords)
            if LineYCoords not in TileYIntervals:
                TileIntervals.append(LineYCoords)


#The class for the tiles that make up the grid
class Tile(pygame.sprite.Sprite):
    def __init__(self, Colour):
        super(Tile, self).__init__()
        #Used to be two separarate variables, TileHeight and TileWidth
        self.Width = TileDimensions
        self.Height = TileDimensions
        #Set as a surfact object based on TileDimensions
        self.image = pygame.Surface((self.Width,self.Height))
        self.ColourVar = 235
        #self.Colour = ((self.ColourVar,100, 100))
        self.Colour = (235,235,235)
        self.image.fill(self.Colour)
        self.rect = self.image.get_rect()
        #Uses a function to place the tiles and start new rows of tiles when necessary
        x,y = PlaceTiles(Shift)
        self.rect.x = x
        self.rect.y = y
        self.Value = ""
        self.Traversable = True
        self.Coord = (self.rect.x , self.rect.y)
        self.Title = ""
        self.Vector = ""

        #Adds its coordinates to all nodes, so every tile on the grid is present, and no tiles that cannot be accessed are in the list.
        #Used for validation to prevent redundancy later
        AllNodes.append(self.Coord)



    def Draw(self):
        global WallPresent
        self.Colour = ((100,100,100))
        WallPresent = True
        MiscGroup.update()
        self.Traversable = False
        Coord = (self.rect.x, self.rect.y)
        if Coord not in ImpassableNodes:
            self.Value = ""
            ImpassableNodes.append(Coord)
            self.Title = "Wall"
            ImpassableList.append(self)

    def Erase(self):
        global WallPresent
        global StartCoords
        if self.Title == "Wall" or "Start" or "Goal" or "End":
            self.Title = ""
            self.Colour = ((235,235,235))
            Coord = (self.rect.x, self.rect.y)
            if Coord in ImpassableNodes:
                ImpassableNodes.remove(Coord)
            if self in ImpassableList:
                ImpassableList.remove(self)
            if ImpassableNodes == []:
                if ImpassableList == []:
                    WallPresent = False
                #If the last wall is erased, the reset button returns to normal
                MiscGroup.update()
        if self.Title == "Start":
            self.Draw()
            self.Erase()
            StartCoords = ''

    def ResetCoords(self):
        self.Vector = ""
    #The update() is sorta messy and I'll clean i[ up/send bits to different procedures at some point
    def update(self):
        #ColourScheme = 'Blue'
        global ColourScheme
        global TileList
        global NodesToSearch
        global HeuristicValue
        global ProcessedList
        global WallPresent
        global BrushType
        global ImpassableList
        #Shows the HeatMap by assigning individual colours values when the checkbox responsible is checked
        if CheckBoxList[1].State == 'Checked':
            if self.Title == "":
                if ColourScheme == 'Blue':
                    self.Colour = ((self.ColourVar, self.ColourVar, 235))
                elif ColourScheme == "Red":
                    self.Colour = ((235, self.ColourVar, self.ColourVar))
                elif ColourScheme == 'Green':
                    self.Colour = (( self.ColourVar,235, self.ColourVar))
                elif ColourScheme == 'Grey':
                    self.Colour = ((self.ColourVar, self.ColourVar, self.ColourVar))
        else:
            if self.Title == "":
                self.Colour = ((235,235,235))

        #Var Definition used to facilitate searching and triggers later
        #   #   #   #   #   #   #   #   #
        Mouse = pygame.mouse.get_pos()
        KeyPressed = pygame.key.get_pressed()
        StartBool = False
        #   #   #   #   #   #   #   #   #
        ##          I m p a s s a b l e     N o d e s         ##

        #when clicked and the Wall tool is selected, the clicked node gets all the credentials of an impassable node
        if self.rect.collidepoint(Mouse[0], Mouse[1]) and BrushType == "Draw" and event.type == pygame.MOUSEBUTTONDOWN:
                #self.image = pygame.image.load("TileImpassable.png").convert()
                self.Draw()

        #When clicked as endnode, it gains the credentials, and removes those of a potentially previously existing endnode
        if self.rect.collidepoint(Mouse[0], Mouse[1]) and event.type == pygame.MOUSEBUTTONDOWN:
            if BrushType =="EndNode":
                self.Erase()
                for i in TileList:
                    if i.Title == "EndNode":
                        i.Colour = ((235,235,235))
                        i.Title = ""

                self.Colour = ((255,0,0))
                self.Title= "EndNode"
                self.Value = 0
            elif BrushType == "StartNode":
                for i in TileList:
                    if i.Title == "Start":
                        i.Colour = ((235,235,235))
                        i.Title = ""
                        i.Value = 0
                self.Title ="Start"
                #Assigned as the largest value so it will always deter particles from it when vectors are generated
                self.Value = 1000
                self.Colour = ((0,255,0))
            #Erases any wall tiles when clicked, removes from containing lists
            elif BrushType == "Eraser":
                self.Erase()

        if KeyPressed[pygame.K_p] and self.rect.collidepoint(Mouse):
            if BrushType == "Draw":
                self.Draw()
            elif BrushType == 'Eraser':
                self.Erase()


        #while there are still nodes to search, the algorithm will continue to find the neighbours of nodes
        #a heatmap value is also assigned
        #Each iteration, the algorithm branches further out ffrom the end, so the heuristic value increases as each node searched in this iteration will be one position further away
        if HeuristicValue < 1000 and NodesToSearch!=[]:
            NodesToSearch = FindNeighbours(NodesToSearch)
            HeuristicValue +=1
            SetValues(NodesToSearch)
            SetHeatmap(TileList)
        #When the number of nodes processed is the same as all the available nodes discounting impassable nodes
        #   Vectors are assigned to each tile
        #       ProcessedList is cleared to ensure vectors are not needlessly assigned to each tile more than once
        if NodesToSearch == [] and len(ProcessedList) > 0:
            self.Vector = ''
            FindNeighboursVector(TileList)
            ProcessedList = []

        self.image = pygame.Surface((self.Width,self.Height))
        self.image.fill(self.Colour)


#Uses RowQuantity, as a larger tile is used less per row
#NewLine counts iterations in the Y - direction, shift in the x - direction
#the position based on these variables are returned to the contructor of the tile class

def PlaceTiles(Shift):
    global NewLine
    global TileDimensions
    x = (Shift%RowQuantity)*TileDimensions
    if Shift%RowQuantity == 0 and Shift >1:
        NewLine +=1
    y = NewLine * TileDimensions
    return x , y


Shift = 0
#The number of tiles in the entire program
#generated in a roundabout way for clarity
# Could be (Gridwith/TileDimensions)**2
TotalTiles = (GridWidth / TileDimensions)* (GridHeight / TileDimensions)


#Made this into a function when I added the functionality to change the grid size while the program runs
def SetGridDimensions():
    #Has to reset all lists as everything has to be generated again
    global TileList
    global Shift
    global AllNodes
    global ImpassableList
    AllNodes = []
    global ProcessedList
    ProcessedList = []
    ImpassableList = []
    global ImpassableNodes
    ImpassableNodes = []
    #Generates new variables based on tile dimensions
    Multiplier = GridWidth/TileDimensions
    global RowQuantity
    TotalTiles = (GridWidth / TileDimensions)* (GridHeight / TileDimensions)
    RowQuantity = GridWidth / TileDimensions
    global NewLine
    TileList = []
    TileGroup.empty()
    Shift = 0
    NewLine = 0



#Places Tiles based on new dimensions and adds them to the necessary list aand froups
    for i in range(TotalTiles):
        tile = Tile(Colour)
        TileGroup.add(tile)
        TileList.append(tile)
        Shift +=1
    GenerateTileIntervals()

#Generates grid of tiles and their intervals at the start of the program
SetGridDimensions()
#TotalTiles = ((GridWidth * GridHeight)/ (TileDimensions*16))
GenerateTileIntervals()


ColourSchemeList = [['Grey',((160,160,160))],['Red',((255,0,0))],['Green',((0,255,0))],['Blue',((0,0,255))]]
def DrawColourSchemeIcon(ColourSchemeList, Mouse):
    global ColourScheme
    for i in ColourSchemeList:
        if i[0] == ColourScheme:
            CurrentColour = i[1]
    pygame.draw.rect(Screen, ((CurrentColour)), ((Distance+160), GridWidth-350,50,50), 0)
    pygame.draw.rect(Screen, ((120,120,120)), ((Distance+160), GridWidth-350,50,50), 2)

CIndex = 0
def CycleColourScheme(ColourSchemeList, Mouse):
    global ColourScheme
    global CIndex
    if (Distance + 160) <= Mouse[0] <= (Distance + 210) and GridWidth-350 <=Mouse[1] <=GridWidth-300:
        CIndex += 1
        if CIndex >3:
            CIndex = 0
    ColourScheme = ColourSchemeList[CIndex][0]


def CheckPresent(TileList):
    AllPresent = False
    StartPresent = False
    EndPresent = False
    for i in TileList:
        if i.Title == "Start":
            StartPresent = True

        if i.Title == "EndNode":
            EndPresent = True
    if StartPresent == True and EndPresent == True:
        AllPresent = True
    return AllPresent

OptionsBool = False
class MoreOptions(pygame.sprite.Sprite):
    def __init__(self):
        super(MoreOptions, self).__init__()
        self.image = pygame.image.load("Additional.png").convert()
        self.image.set_colorkey((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = CentreWidth+50
        self.rect.y = 725
    def CheckCollide(self, Mouse):
        global OptionsBool
        global QuantityDrag
        global ControlDrag
        global SpeedDrag
        #Sliders would be affected when the additional options menu was not visible from this point.
        if self.rect.collidepoint(Mouse):
            if OptionsBool == True:
                OptionsBool = False
                QuantityDrag = False
                ControlDrag = False
                SpeedDrag = False
            else:
                OptionsBool = True
        return OptionsBool


    def update(self):
        pass


options = MoreOptions()
MiscGroup.add(options)


def GeneratePresets(RowQuantity, Preset):
    LineChange = 0
    Range = len(TileList)

#  For preset 2 only
    FirstOrLast = 0

    for i in range (Range):
        RowPlace =  i% RowQuantity
        if RowPlace == 0 :
            if LineChange == 0:
                LineChange = 1
                Entry = random.randrange(0,RowQuantity-2,1)
                if FirstOrLast == RowQuantity-1:
                        FirstOrLast = 0
                else:
                        FirstOrLast = RowQuantity-1
            else:
                LineChange = 0
       #Preset1
        if Preset == 1:
            if LineChange == 0:
                if RowPlace%2 != 0:
                    MakeImpassable(i)
#       Preset2
        if Preset == 2:
            if  LineChange == 0:
                if RowPlace != FirstOrLast:
                    MakeImpassable(i)

        if Preset == 3:
            if LineChange == 0:

                if (RowPlace != Entry):
                    MakeImpassable(i)

def MakeImpassable(i):
    TileList[i].Colour = ((100,100,100))
    WallPresent = True
    MiscGroup.update()
    TileList[i].Traversable = False
    Coord = (TileList[i].rect.x, TileList[i].rect.y)
    if Coord not in ImpassableNodes:
        TileList[i].Value = ""
        ImpassableNodes.append(Coord)
        TileList[i].Title = "Wall"
        ImpassableList.append(TileList[i])


ParticleGroup = pygame.sprite.Group()
ParticleList = []
def SpawnParticles():
    global HeuristicValue
    HeuristicValue = 0
    global NumberOfParticles
    global ParticleGroup
    global ParticleList
    ParticleGroup.empty()
    ParticleList = []
    for i in range(NumberOfParticles):
        particle = Particle()
        Particle.SetSpawn(particle)
        ParticleGroup.add(particle)
        ParticleList.append(particle)

def WallHighlight(TileList):
    global ImpassableList
    global TileDimensions
    for i in ImpassableList:
        x = i.rect.x
        y = i.rect.y
        pygame.draw.rect(Screen, ((245,245,245)), (x,y, TileDimensions, TileDimensions), 2)

    #Implemented due to the red heatmap obscuring the red tile.
    #Deepest possible red is 255,0,0  , nearest heatmap red can be almost indistungui





    # Handles mostly cosmetic elements of the program
#Sets the areas allocated for the buttons that allow users to add certain tile types into grid
StartNodeParam = ((CentreWidth,CentreWidth+40), (100,140))
EndNodeParam = ((CentreWidth,CentreWidth+40) , (200,240))
EraserParam = ((CentreWidth, CentreWidth +40) , (300,340))
DrawParam = ((CentreWidth, CentreWidth +40) , (400,440))


#On click , the position of the mouse determines which brush the user has selected, returns value
def DetermineBrushType(Mouse, StartNodeParam, EndNodeParam, DrawParam):
    if  (StartNodeParam[0][0] <= Mouse[0] <=StartNodeParam[0][1]) and StartNodeParam[1][0]<=Mouse[1]<=StartNodeParam[1][1] and event.type == pygame.MOUSEBUTTONDOWN:
        BrushType = "StartNode"
        return BrushType


    elif (EndNodeParam[0][0] <= Mouse[0] <=EndNodeParam[0][1]) and EndNodeParam[1][0]<=Mouse[1]<=EndNodeParam[1][1]:
        BrushType = "EndNode"
        return BrushType


    elif (EraserParam[0][0] <= Mouse[0] <=EraserParam[0][1]) and EraserParam[1][0]<=Mouse[1]<=EraserParam[1][1]:
        BrushType = "Eraser"
        return BrushType

    elif (DrawParam[0][0] <= Mouse[0] <=DrawParam[0][1]) and DrawParam[1][0]<=Mouse[1]<=DrawParam[1][1]:
        BrushType = "Draw"
        return BrushType

    else:
        pass


#Draws all menu items onto the screen
def DrawMenuItems(Width, Height, GridWidth, GridHeight):
    global BrushType
    global CentreWidth

    #Menu
    pygame.draw.rect(Screen, ((220,220,220)), (GridWidth,0,(Width - GridWidth),GridHeight), 0)

    #Start
    pygame.draw.rect(Screen, (10,255,0), ((CentreWidth),100,40,40), 0)

    #End
    pygame.draw.rect(Screen, (255,0,0), ((CentreWidth),200,40,40), 0)

    #Brush
    pygame.draw.rect(Screen, (150,150,150) , ((CentreWidth), 400,40,40), 0)



    #Eraser
    #Due ot the light colour of the eraser, a grey border is drawn to prevent it from being ignored
    #The brush type determines which of the 4 options has a border drawn around it to show the user it is being used
    pygame.draw.rect(Screen, (250,250,250), (CentreWidth, 300, 40, 40), 0)
    if BrushType!="Eraser":
        pygame.draw.rect(Screen , (210,210,210), (CentreWidth, 300, 40, 40) ,2)
    else:
        pygame.draw.rect(Screen , (155,155,155), (CentreWidth, 300, 40, 40) ,2)

    if BrushType == "StartNode":
        pygame.draw.rect(Screen , (155,155,155) , ((CentreWidth,100,40,40)), 2)

    elif BrushType =="EndNode":
        pygame.draw.rect(Screen , (155,155,155) , ((CentreWidth,200,40,40)), 2)

    elif BrushType == "Draw":
        pygame.draw.rect(Screen , (235,235,235) , ((CentreWidth,400,40,40)), 2)


#       #       #       #       #       #       #       #       #       #       #


#Draws the gridlies onto the screen, made into a separate procedure for clarity
#Can be disabled after unchecking the ncessary checkbox
def DrawGridLines(TileIntervals):
    for i in TileIntervals:
        pygame.draw.line(Screen, ((200,200,200)), i[0],  i[1] , 1)

def CheckOptionsBounds(Mouse, OptionsBool):
    global BrushType

    if 100 <= Mouse[0] <= GridWidth-100 and 100 <= Mouse[1] <= GridHeight and OptionsBool == True:
        BrushType = ""


# Creates the labels that show the user the purpose of objects without the use of the help button
GridLinesLabel = MyFont.render(("S h o w    G r i d l i n e s"), 4, ((140,140,140)))
HeatMapLabel = MyFont.render(("S h o w   H e a t m a p"), 4, ((140,140,140)))
ResetLabel = MyFont.render(('R e s e t   T e r r a i n') ,   4 , ((140,140,140)))
BorderLabel = MyFont.render(('P a r t i c l e   B o r d e r s') , 4 ,((140,140,140)))
GridSizeLabel = MyFont.render(('C h a n g e   D i m e n s i o n s') , 4 , ((140,140,140)))
MoreOptionsLabel = MyFont.render(("M o r e   O p t i o n s"), 4, ((140,140,140)))
#Screen.blit(GridLinesLabel, (900, 500), 1)


#Creates the labels present when 'help' is clicked
StartLabel = HelpFont.render(("S t a r t                              P o i n t"), 4 , ((100,100,100)))
EndLabel  = HelpFont.render((" E n d                               P o i n t"), 4 , ((100,100,100)))
EraserLabel = HelpFont.render(("E r a s e                              T e r r a i n"), 4 , ((100,100,100)))
WallLabel = HelpFont.render((" D r a w                               T e r r a i n"), 4 , ((100,100,100)))
ExecuteLabel = MyFont.render(("Press ' S P A C E '  to run") , 4 , (100,100,100))
PaintLabel = HelpFont.render((" H o l d    ' P '  t o   d r a w"), (4) , ((100,100,100)))


OptionsRect = ((100,100,GridWidth-200, GridHeight-200))
AllPresent = False
#Used in separate procedure for clarity
#blits the labels that help the user into the screen when necessary
def DisplayHelp(StartLabel , EndLabel , EraserLabel , WallLabel, ExecuteLabel, PaintLabel):
    Screen.blit(StartLabel , (CentreWidth-40 , 113))
    Screen.blit(EndLabel , (CentreWidth-40 , 213))
    Screen.blit(EraserLabel ,(CentreWidth-40 , 313))
    Screen.blit(WallLabel , (CentreWidth-40 , 413))
    Screen.blit(ExecuteLabel , (CentreWidth-40 , 700))
    Screen.blit(PaintLabel , (CentreWidth + 40 , 363))
#Mainloop
while Active == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Active = False
        KeyPressed = pygame.key.get_pressed()
        #On click ~
        #Gets the position of the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mouse = pygame.mouse.get_pos()
            #if the click is in the menu area, is checks to see if the user clicked a brushtype
            if CentreWidth <=Mouse[0]:
                BrushType = DetermineBrushType(Mouse, StartNodeParam, EndNodeParam, DrawParam)
            #Updates the group containing UI elements that are only meant to update on click
            MiscGroup.update()
            #checks to see if the user is dragging the pointer
            slider.CheckDrag()
            options = MoreOptions()
            OptionsBool = options.CheckCollide(Mouse)
            clearslider.CheckDrag(Mouse)
            CheckOptionsBounds(Mouse, OptionsBool)
            CycleColourScheme(ColourSchemeList, Mouse)
            if OptionsBool== True:
                preset1.update(Mouse)
                preset2.update(Mouse)
                preset3.update(Mouse)
        #Sets drag to False, then updates the Pointer class
        #This is so it may access the part of the update function that sets the pointer to an interval and changes the grid dimensions
        if event.type == pygame.MOUSEBUTTONUP:
            Drag = False
            SizePointerGroup.update()
            options = MoreOptions()

        # Point of analysis - had to place this in mainloop as when placed in tile.update , on the faster, larger maps, it would spawn them multiple times, wasnt noticeable on maps like 20x20
        #when space is pressed once, it runs the breadth first search algorithm
        if KeyPressed[pygame.K_SPACE]:
            AllPresent = CheckPresent(TileList)
            if AllPresent == True:
                for i in TileList:
                    if i.Title == "EndNode":
                        Coord = (i.rect.x , i.rect.y)
                        NodesToSearch.append(Coord)
        if KeyPressed[pygame.K_ESCAPE]:
            Active = False
    Mouse = pygame.mouse.get_pos()

    Screen.fill((255,255,255))
    #Draws spritegroup objects onto screen, updates the necessary ones every iteration

    #Updates the pointer position only when drag is True, as it will need to move fluidly when being dragged, and remain still otherwise
    if Drag == True:
        SizePointerGroup.update()
    #Draws the squares showing the different brustypes on screeh
    DrawMenuItems(Width, Height, GridWidth, GridHeight)

    #Framerate of 60fps, necessary to show off the fluidity of the particles
    Clock.tick(60)

    #Dras gridlines evey iteration only when the checkbox is clicked
    #if CheckBoxList[0].State == "Checked":

    #blits the constant labels on to the screen
    Screen.blit(GridLinesLabel, (CentreWidth-40, 500))
    Screen.blit(HeatMapLabel, (CentreWidth-40, 530))
    Screen.blit(ResetLabel , (CentreWidth-40, 596))
    Screen.blit(GridSizeLabel , (CentreWidth-40, 640))
    Screen.blit(BorderLabel , (CentreWidth-40, 560))
    Screen.blit(MoreOptionsLabel, (CentreWidth+84, 732))

    #when helpbool is true, blits the help labels onto the screen by calling the procedure
    if HelpBool == True:
        DisplayHelp(StartLabel , EndLabel, EraserLabel , WallLabel, ExecuteLabel, PaintLabel)
    #only updates the particle group when they are set to be on the screen

    #Draws the pointer onto the screen, separately from MiscGroup due to need for updating more often

    TileGroup.draw(Screen)
    TileGroup.update()

    if CheckBoxList[0].State =="Checked":
        DrawGridLines(TileIntervals)
    #At the bottom of mainloop so it can overlay on already-drawn tile
        #Withouth drawing over the additional options menu etc.
    #Used so tiles can be distinguished when heatmap is present on the map
    if CheckBoxList[1].State == "Checked":
        WallHighlight(TileList)
    MiscGroup.draw(Screen)
    DrawVectorDirections(TileList , TileDimensions , FullThing)
    if QuantityDrag == True or ControlDrag == True or SpeedDrag == True:
        clearpointer.update(Mouse, QuantityDrag, ControlDrag, SpeedDrag)
    if ParticleBool == True:
        ParticleGroup.draw(Screen)
        ParticleGroup.update()
    #Draws the options menu when the button is pressed
    if OptionsBool == True:
        pygame.draw.rect(Screen, ((230,230,230)), (100,100,GridWidth-200, GridHeight-200), 0)
        pygame.draw.rect(Screen, ((200,200,200)), (100,100, GridWidth-200 , GridHeight - 200), 3)
        OptionsGroup.draw(Screen)
        OptionsExtraGroup.draw(Screen)
        DrawOptionLabels(QuantityLabel, QuantityTextLabel, ControlLabel, SpeedLabel, SchemeLabel, PresetLabel)
        DrawColourSchemeIcon(ColourSchemeList, Mouse)
    SizePointerGroup.draw(Screen)


    pygame.display.flip()
pygame.quit()


