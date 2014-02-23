#Noah Goetz 
#ngoetz 
#112 Term Project

# coding=UTF-8

from PIL import Image

import random, sys, os, pygame, string, copy


from pygame import *

class Colors(object):
    def __init__(self):
        self.lime = (70, 255, 13)
        self.orange = (240, 173, 12)
        self.red = (255, 4, 0)
        self.lightRed = (245, 139,145)
        self.blue = (24, 0, 178)
        self.darkBlue = (0, 2,64)
        self.lightBlue = (110, 157, 255)
        self.lightGreen = (168,255,158)
        self.green = (26, 204, 14)
        self.teal = (0, 234, 90)
        self.lightBlue = (112, 146, 255)
        self.brown = (178, 142, 43)
        self.beige = (255,231,145)
        self.roomBlue = (61,88,178)
        self.forestGreen = (11, 89, 2)
        self.black = (0,0,0)
        self.blackt = (60,60,60,0)
        self.white = (255,255,255)
        self.gray = (205,201,201)
        self.gold = (255, 228, 76)
        self.burntOrange = (255, 106, 23)
        self.yellow = (255,248,0)
        self.pink =(187,124,175)
        self.baseColor = (245,255,255)
        self.medBlue = (10, 97, 191)
        self.color1 = (123,212,158)
        self.color2 = (49,89,87)
        self.color3 = (89,65,73)
        self.color4 = self.pink
        self.titleColor = (168, 50, 23)
        self.boardColor = (114,124,133)
        self.colorList = [self.lightBlue, self.pink, self.lightGreen, self.white, 
                    self.lightRed, self.burntOrange, self.gold]


class KantanWrapper(object):
    '''contains shared methods beween the splash screen and the game'''

    def errorMsg(self, text):
        '''this draws an error box and blocks until the user clicks'''
        self.drawErrorBox(text)
        while self.answer == None and self.run == True:
            self.timerFired()

    def removeMarginSpaces(self, text):
        '''removes the leading and trailing spaces'''
        marker = False
        start = 0
        stop = len(text)
        for c in xrange(len(text)):
            if text[c] in string.whitespace:
                if marker == False:
                    start = c+1 
            else:
                marker = True
                stop = c
        return text[start:stop+1]

    def drawPopUp(self, text, boxColor, alignment="center"):
        #sets dimentions for the box and creates a rect object
        x0 = self.width/2-self.width/4
        y0 = self.height/2-self.height/4
        width = self.width/2
        height = self.height/2
        #make a temporary surface so the box can be translucent
        tempSurface = pygame.Surface((width, height))
        popRect =  Rect(0, 0, width, height)
        pygame.draw.rect(tempSurface, boxColor, popRect)
        tempSurface.set_alpha(175)
        self.screen.blit(tempSurface, (x0,y0))
        #draws the text
        #sets the color of the text based on how dark the backgound is 
        if sum(boxColor) < 650: 
            textColor = color.white
        else:
            textColor = color.black
        textList = text.split('\n')
        OffsetI = (len(textList)/2)*(self.playerFontSize/2)
        Yoffset = len(textList)
        #deals with multiple lines of text
        for line in textList:
            #draws the text
            offset = Yoffset*(self.playerFontSize/2)
            if alignment=="center":
                self.drawText(self.removeMarginSpaces(line), self.playerFont, 
                        self.playerFontSize/2, textColor,
                        center=(self.width/2, self.height/2+OffsetI-offset))
            elif alignment=="top":
                self.drawText(self.removeMarginSpaces(line), self.playerFont, 
                        self.playerFontSize/2,
                        textColor, top=y0-offset+(self.playerFontSize/2), 
                        centerx=self.width/2)
            Yoffset -= 1 
        return len(textList)/2 - len(textList)


    def drawErrorBox(self, text):
        '''displayes an error box that does not require user input'''
        #these setting ensure timerfired knows an error box is open
        self.answer = None
        self.pendingMessage = True
        self.error = True
        Yoffset=self.drawPopUp(text, color.red)
        offset = Yoffset*(self.playerFontSize/2)
        self.drawText("Click anywhere to continue...", self.playerFont, 
            self.playerFontSize/2, color.black, 
            center=(self.width/2+self.playerFontSize/2, 
                self.height/2-offset))
        pygame.display.flip()

    def drawConfirmationBox(self, text, alignment="center", skipYes=False, focus="yes"):
        '''displays a confirmation box to determine the 
            answer to a yes/no question'''
        #these setting ensure timerfired knows a confirmation box is open
        self.pendingMessage = True
        self.answer = None
        x0, y0 = self.width/2-self.width/4, self.height/2-self.height/4
        width, height = self.width/2, self.height/2
        #draws box and text
        self.drawPopUp(text, color.black, alignment)
        #makes the buttons
        noButtonX0 = int(x0+width/16.0)
        buttonY0 = int(y0+height*7/8.0)
        buttonWidth, buttonHeight = self.hexSideLegnth, self.hexSideLegnth/3
        self.noButton = Button(noButtonX0, buttonY0, buttonWidth, buttonHeight,
                         "No")
        self.drawButton(self.noButton, color.black, color.red)
        yesButtonX0 = int(x0+width - width/16.0 - buttonWidth)
        #If skips yes if the box closes for some other reason
        if skipYes == False:
            self.yesButton = Button(yesButtonX0, buttonY0, buttonWidth, buttonHeight,
                             "Yes")
            self.drawButton(self.yesButton, color.black, color.green)
        else:
            self.yesButton = Button()
        pygame.display.flip()

    def drawPassBox(self, text):
        self.pendingMessage = True
        self.answer = None 
        self.noButton = Button() #init an empty button
        x0, y0 = self.width/2-self.width/4, self.height/2-self.height/4
        width, height = self.width/2, self.height/2
        #draws the box and text
        self.drawPopUp(text, color.green)
        #makes the doneButton 
        buttonY0 = int(y0+height*7/8.0)
        buttonWidth, buttonHeight = self.hexSideLegnth, self.hexSideLegnth/3
        yesButtonX0 = int(x0+width - width/16.0 - buttonWidth)
        self.yesButton = Button(yesButtonX0, buttonY0, buttonWidth, buttonHeight,
                         "Done")
        self.drawButton(self.yesButton, color.black, color.white)
        pygame.display.flip()

    def drawButton(self, button, textColor, buttonColor=None, textSize = 12):
        if buttonColor == None: buttonColor = button.color
        buttonRect = Rect(button.x0, button.y0, button.width, button.height)
        pygame.draw.rect(self.screen, buttonColor, buttonRect)
        #draws the text on the button
        textCenter=(button.x0+button.width/2, button.y0+button.height/2)
        self.drawText(button.text, self.playerFont, textSize, 
            textColor, center=textCenter)

    def drawTitle(self):
        #unicode is to have the accent on the "a"
        text = "Residents of K" + unichr(0x00E1) +"tan"
        self.drawText(text, self.titleFont, self.titleSize, self.titleColor, 
                        centerx=self.width/2)

    def drawBackground(self):
        self.screen.fill(self.backgroundColor)
    
    def drawCaption(self):
        pygame.display.set_caption("Residents of Katan")

    def drawText(self, myText, font, size, textColor, **args):
        '''Text handler to easily draw text with one line, only suports one 
        line of text due to enable more flexibilty in the **args in specifying
        location. drawText(text, font, size, color, **locationArgs) -> None'''
        fontObject = pygame.font.Font(font, size)
        text = fontObject.render(myText, True, textColor)
        textRect = text.get_rect(**args)
        self.screen.blit(text, textRect)
        return textRect

    def initFontsAndColors(self):
        width = self.width
        height = self.height
        self.titleFont = pygame.font.match_font("msgothic") #luxiserif #papyrus?
        self.playerFont = pygame.font.match_font("corbel")
        self.titleSize = int(min(height/16, width/8))
        self.titleColor = color.titleColor 
        self.playerFontSize = int(self.hexSideLegnth/2)
        self.backgroundColor = color.medBlue


    def textWidth(self, myText, font, fontSize):
        fontObject = pygame.font.Font(font, fontSize)
        text = fontObject.render(myText, True, color.black)
        textRect = text.get_rect()
        width = textRect.width
        return width

class KatanSplashScreen(KantanWrapper):
    '''Controls the Splash Screen for a Katan Game on a Single Computer'''

    color = Colors()

    def startGame(self):
        '''starts the game if it is legal and the user wants that'''
        if self.checkLegalStart():
            self.drawConfirmationBox('''Are you sure you want start?
             All players that's names are not set to "" will play. ''')
            while self.answer == None and self.run == True:
                self.timerFired()
            answer = self.answer 
            self.answer = None
            if answer == True:
                newGame = Katan(self.timeLimit, self.startList)
                self.run = False
                pygame.quit()
            else: 
                self.sredrawAll()

    def duplicateNames(self):
        for i in xrange(len(self.playerList)):
            tempList = copy.copy(self.playerList)
            player = self.playerList[i]
            tempList.remove(player)
            if player in tempList and player != "":
                return True
        return False

    
    def checkLegalStart(self):
        self.startList = [] 
        for i in xrange(len(self.textBoxes)):
            if self.textBoxes[i].text != "":
                info = (self.playerList[i], self.textBoxes[i].color)
                self.startList += [info]
        if self.duplicateNames():
            self.errorMsg("Every player must have a unique name!")
            return False
        if len(self.startList)<2:
            self.errorMsg('''You must have at least 2 players.''')
            return False
        try:
            self.timeLimit = int(self.timeLimit)
        except:
            self.errorMsg("The time limit must be an integer")
            return False
        return True

    def enterPressed(self):
        if self.pendingMessage == True:
            if self.error == True:
                self.error = False
                self.pendingMessage = False
                self.sredrawAll()
            else: #defaults yes
                self.answer = True
                self.pendingMessage = False
                self.sredrawAll()

    def smousePressed(self, (x, y)):
        if self.pendingMessage == True:
            if self.error == True:
                self.error = False
                self.pendingMessage = False
                self.sredrawAll()
            elif self.yesButton.pressed(x,y):
                self.answer = True
                self.pendingMessage = False
            elif self.noButton.pressed(x,y):
                self.answer = False
                self.pendingMessage = False
        else:
            if self.doneButton.pressed(x, y):
                self.startGame()
            else:
                for b in xrange(len(self.textBoxes)):
                    box = self.textBoxes[b]
                    if  box.pressed(x,y): 
                        #sets which box they're typing in
                        self.focus = box
                        #clear the box the first time it is clicked
                        if self.ClickedList[b] == False: box.setText("")
                        self.ClickedList[b] = True 
                if self.timerButton.pressed(x,y):
                    self.focus = self.timerButton
                self.sredrawAll()

    def appendText(self, key):
        '''adds letters to the buttons's Text'''
        #capitalizes letters 
        if ord("a") <= key and key <= ord("z") and self.caps == True:
            diff = ord("a") - ord("A")
            char = chr(key-diff)
        else:
            char = chr(key)
        text = self.focus.text + char
        #checks if the text would get too Big
        size = self.textWidth(text, self.playerFont, self.playerFontSize)
        if size < self.boxWidth:
            #appends the charecter
            self.focus.setText(self.focus.text + char)
            self.updateValues()
            self.sredrawAll()

    def backspace(self):
        '''removes last charecter'''
        size = len(self.focus)
        #checks if there is text there
        if size > 0:
            text= self.focus.text[0:size-1]
            self.focus.setText(text)
            self.updateValues()
            self.sredrawAll()

    def rotateColors(self, forward=True):
        i = self.focus.colorIndex
        if self.focus in self.textBoxes and type(i) == int:
            self.usedColors.remove(self.focus.color)
            if forward== True:
                dColor = 1
            else:
                dColor = -1 
            i += dColor
            i %= len(color.colorList)
            while color.colorList[i] in self.usedColors:
                i+= dColor
                i %= len(color.colorList)
            self.focus.setColorFromList(i)
        self.updateValues()
        self.sredrawAll()

    def timerFired(self):
        '''event handler'''
        self.clock.tick(20)
        justBackSpaced = False
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False
                pygame.quit()
                return None
            else:
                if event.type == MOUSEBUTTONDOWN: 
                    self.smousePressed(event.pos)
                elif event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        self.caps = True
                    elif event.key == K_BACKSPACE:
                        justBackSpaced = True
                        self.backspace()
                    elif event.key == K_RIGHT:
                        self.rotateColors() #rotate forwards
                    elif event.key == K_LEFT:
                        self.rotateColors(False) #rotate backwards
                    elif event.unicode in string.ascii_letters or event.unicode in string.digits: #numebers
                        self.appendText(event.key)
                elif event.type == KEYUP:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        self.caps = False
        if self.run == True:
            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[K_BACKSPACE]:
                if justBackSpaced == False: self.backspace()
                pygame.time.delay(100)
                
    def __init__(self):
        pygame.init()
        self.backgroundColor = color.blue
        self.width = 1000
        self.height = 750
        self.hexSideLegnth = (self.width*3/(4.0*12))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.initFontsAndColors()
        self.player1Box = Button()
        self.player2Box = Button()
        self.player3Box = Button()
        self.player4Box = Button()
        self.player1, self.player2, self.player3, self.player4  = '','','',''
        self.playerList = [self.player1, self.player2, 
                        self.player3, self.player4]
        self.textBoxes = [self.player1Box, self.player2Box, 
                        self.player3Box, self.player4Box]
        self.doneButton = Button()
        self.initPlayerButtons()
        self.initTimerButton()
        self.updateValues()
        self.focus = self.player1Box
        self.clock = pygame.time.Clock()
        self.caps = False
        self.pendingMessage = False
        self.answer = None
        self.error = False
        self.sredrawAll()
        self.smainloop()
        
    def initTimerButton(self):
        left = self.width/2 + self.hexSideLegnth
        width = self.hexSideLegnth*1.5
        top = self.height/2 +(self.boxHeight+self.boxHeight/2)*2
        self.timerButton = Button(left, top, width, self.boxHeight, "15")

    def initPlayerButtons(self):
        font = self.playerFont
        size = self.playerFontSize
        self.boxWidth = self.width/3
        self.boxHeight = int(self.playerFontSize*1.3)
        margin = self.boxHeight/2 
        boxX0 = self.width/2 - self.boxWidth/2 
        #sets the y0 bassed on the size of the box and space in between
        boxY0 = self.height/2 - (self.boxHeight+margin)*2 
        count = 0 
        for box in self.textBoxes:
            count += 1 
            box.setText("Player %d" % count)
            y0 = boxY0 + (count-1)*(self.boxHeight+margin)
            box.setCoords(boxX0, y0, self.boxWidth, self.boxHeight)
        self.doneButton = Button(self.width-3*self.hexSideLegnth, 
            self.height-2*self.hexSideLegnth, 2*self.hexSideLegnth, 
            self.hexSideLegnth, "Ready")
        self.usedColors = []
        for c in xrange(len(self.textBoxes)):
            self.textBoxes[c].setColorFromList(c)
        self.Clicked1 = False
        self.Clicked2 = False
        self.Clicked3 = False
        self.Clicked4 = False
        self.ClickedList = [self.Clicked1, self.Clicked2, 
                    self.Clicked3, self.Clicked4]

    def smainloop(self):
        while self.run == True:
            self.timerFired()

    def sredrawAll(self):
        self.drawBackground()
        self.drawTitle()
        self.drawBoxes()
        self.drawButtons()
        pygame.display.flip()

    def updateValues(self):
        for i in xrange(len(self.playerList)):
            box = self.textBoxes[i]
            self.playerList[i] = box.text
        self.player1 = self.playerList[0]
        self.player2 = self.playerList[1]
        self.player3 = self.playerList[2]
        self.player4 = self.playerList[3]
        self.timeLimit = self.timerButton.text
        self.color1 = self.textBoxes[0].color
        self.color2 = self.textBoxes[1].color
        self.color3 = self.textBoxes[2].color
        self.color4 = self.textBoxes[3].color
        self.usedColors=[self.color1, self.color2, self.color3, self.color4]

    def drawButtons(self):
        self.drawButton(self.doneButton, color.black, 
                color.gold, self.playerFontSize)

    def drawBoxes(self):
        for box in self.textBoxes:
            self.drawButton(box, color.black, textSize=self.playerFontSize)
        self.drawButton(self.timerButton, color.black, color.white, 
                self.playerFontSize)
        self.drawText("Time Limit (min)", self.playerFont, self.playerFontSize, 
            color.black, left=self.width/2 - self.boxWidth/2, 
            top = self.height/2 + 3*self.boxHeight)


class Katan(KantanWrapper):
    color = Colors()

    def redrawAll(self, drawPersonal=True):
        '''Redraws the whole board'''
        self.drawBackground()
        self.drawCaption()
        self.drawTitle()
        if self.gameOver == False:
            self.drawBoard()
            self.drawRoads()
            self.drawBuildings()
            self.drawPlayerBox()
            self.drawDice()
            if drawPersonal: self.drawResources()
            self.drawButtons()
        else:
            self.drawGameOver()
        pygame.display.flip()

    def drawButtons(self):
        '''Draws the buttons'''
        self.drawButton(self.endTurn, color.black, 
                            color.gold, self.playerFontSize)
        self.drawButton(self.buyDevCardButton, color.black, 
                            color.gold, self.playerFontSize)
        self.drawButton(self.useDevCardButton, color.black, 
                            color.gold, self.playerFontSize)
        centerx = (self.buyDevCardButton.x1 + self.useDevCardButton.x0)/2
        bottom = self.buyDevCardButton.y0 - .5*self.playerFontSize
        self.drawText("Development Cards", self.playerFont, 
                    self.playerFontSize, color.black,
                    centerx=centerx, bottom=bottom)
        self.drawButton(self.timeButton, color.black, 
            self.backgroundColor, self.playerFontSize)

    def drawGameOver(self):
        text = "%s won" % (self.winner)
        self.drawText(text, self.titleFont, self.titleSize, self.titleColor, 
                    center=(self.width/2, self.height/2))

    def drawDice(self):
        '''draws the dice'''
        #for when pictures are implemented
        #pict1 = self.dice[self.die1]
        #pict2 = self.dice[self.die2]
        die1Text = "Die 1: " + str(self.die1)
        die2Text = "Die 2: " + str(self.die2)
        width = self.textWidth(die2Text, self.playerFont, self.playerFontSize)
        dieLeft = int(self.width-width-self.hexSideLegnth)
        die1Top = int(self.height - 2*self.hexSideLegnth)
        die2Top = int(self.height - self.hexSideLegnth)
        self.drawText(die1Text, self.playerFont, self.playerFontSize, 
            color.black, left = dieLeft, top = die1Top)
        self.drawText(die2Text, self.playerFont, self.playerFontSize, 
            color.black, left = dieLeft, top = die2Top)

    def drawResources(self):
        '''Draws the resurce amounts and buttons'''
        player = self.players[self.currentPlayer]
        #key: 0:wood, 1:brick, 2:stone, 3:Sheep, 4:wheat
        for r in xrange(len(self.resourceList)):
            #first update the button values with the current player's amount
            text = self.resourceList[r]+ ": "+ str(self.resourceDicts[r][player])
            self.resourceButtons[r].setText(text)
            #then draw the button 
            self.drawButton(self.resourceButtons[r], color.black, 
                self.resourceColors[r], self.playerFontSize)

    def drawRoads(self):
        '''Draws the roads'''
        cols, rows  = self.settlementCols, self.settlementRows
        roadKeys = self.roads.keys()
        for key in roadKeys:
            player = self.roads[key]
            #if there is a road there
            if player != 0:
                spotA = key[0]
                spotB = key[1]
                pointA = self.getVertexCoordinates(spotA[0],spotA[1])
                pointB = self.getVertexCoordinates(spotB[0],spotB[1])
                pygame.draw.line(self.screen, self.playerColors[player-1], 
                                pointA, pointB, 7)

    def drawBuildings(self):
        '''determines what building to draw and where'''
        cols, rows  = self.settlementCols, self.settlementRows
        for row in xrange(rows):
            for col in xrange(cols):
                settlement = self.buildings[row][col]
                #if there is a structure there
                ##print type(settlement)
                ##print settlement
                if type(settlement) == int and settlement != 0: 
                    #if it is a settlement
                    if settlement > 0 and settlement <= len(self.players):
                        player = settlement-1
                        self.drawSettlement(row, col, player)
                    elif settlement > self.totalPlayers:
                        player = settlement - len(self.players) -1 
                        self.drawCity(row,col, player)

    def drawSettlement(self, row, col, player):
        '''draws a settlement at a point'''
        xc, yc = self.getVertexCoordinates(row, col)
        r = int(self.hexSideLegnth/4)
        #draws a circle at the vertex
        pygame.draw.circle(self.screen, self.playerColors[player], 
            (xc, yc), r)       

    def drawCity(self, row, col, player):
        '''draws a city at a point'''
        xc, yc = self.getVertexCoordinates(row, col)
        rOut = int(self.hexSideLegnth/4)
        rIn = int(self.hexSideLegnth/8)
        #outer circle
        pygame.draw.circle(self.screen, self.playerColors[player], 
            (xc, yc), rOut)
        #inner circle
        pygame.draw.circle(self.screen, color.white, 
            (xc, yc), rIn)  

    def getVertexCoordinates(self, row, col):
        '''Converts the row, col of the vertex to graphics coordinets'''
        X0 = self.boardX
        Y0 = self.boardY
        s = self.hexSideLegnth
        c = ((3**.5)/2.0)
        newY = int(Y0 + c*row*s)
        #only rounds the "*.5" one because the other one is 
        #only added on the even cols
        newX = int(X0 + round(col/2.0)*.5*s+(col/2)*s)
        return (newX, newY)

    def drawPlayerBox(self):
        '''Draws the box with the list of playes, noting current player'''
        self.drawPlayerTitle()
        #draw each player's name
        for i in xrange(len(self.players)):
            cy = self.playerBoxY0+1.5*self.playerFontSize*(i+1)
            cx = (self.boxSizeX/2)+self.playerBoxX0
            nameRect = self.drawText(self.players[i],self.playerFont,
                self.playerFontSize, self.playerColors[i], center=(cx, cy))
            #circle next to the current player's name
            if i == self.currentPlayer: 
                #nameRect = ()
                x = int(self.playerBoxX0 - self.hexSideLegnth/2)
                r = int(self.hexSideLegnth/4)
                #pygame.draw.circle(self.screen,self.playerColors[i],(x,int(cy)),r)
                pygame.draw.rect(self.screen, self.playerColors[i], nameRect, 2)

    def drawPlayerTitle(self):
        '''draws "players" at the top of the player box'''
        self.drawText("Players:", self.titleFont, self.playerFontSize, 
            self.boardColor, left=self.playerBoxX0, 
            bottom=self.playerBoxY0-.1*self.playerFontSize)
        #draw box around all of the players
        playerRect = pygame.Rect(self.playerBoxX0, self.playerBoxY0, 
                        self.boxSizeX, self.boxSizeY)
        pygame.draw.rect(self.screen, self.boardColor, playerRect, 2)      

    def drawBoard(self):
        '''Draws the hexes with the resource deretmining the color'''
        cols, rows  = self.boardCols, self.boardRows
        s = self.hexSideLegnth
        c = ((3**.5)/2.0)
        for col in xrange(cols):
            x = 1.5*s*col + self.boardX
            for row in xrange(rows):
                y= c*s*row + self.boardY 
                resource = self.resources[row][col]
                #if there is a hexagon there
                if resource != None:
                    #math for a regular hexagon in terms of the 
                    #left center vertex
                    pointList = ((x,y),(x+.5*s,y-c*s),((x+1.5*s), y-c*s),
                        ((x+2*s), y), ((x+1.5*s), y+c*s), (x+.5*s, y+c*s))
                    #draw fill
                    pygame.draw.polygon(self.screen, 
                        self.resourceColors[resource], pointList, 0)
                    #draw boarder
                    pygame.draw.polygon(self.screen, self.boardColor,
                         pointList, 2)
                    #draw Probabilities
                    self.drawProbabilities(row, col, x, y)

    def drawProbabilities(self, row, col, x, y):
        '''draws the sum that corisponds to hexagon 
            in the middle of that hexagon'''
        xc = int(x + self.hexSideLegnth)
        yc = int(y) 
        r = int(self.hexSideLegnth/3)
        if self.resources[row][col] != 5:
            pygame.draw.circle(self.screen, color.beige, 
                                (xc, yc), r, 0)
            number = str(self.probs[(row,col)])
            fontObject = pygame.font.Font(self.titleFont, 
                int(self.hexSideLegnth/4))
            prob = fontObject.render(number, True, color.black)
            probRect = prob.get_rect(center=(xc, yc))
            self.screen.blit(prob, probRect)
        if self.robber == (row, col):
            pygame.draw.circle(self.screen, color.black, 
                                (xc, yc), r, 0)

    def playMonopoly(self):
        '''Plays the monopoly card '''
        player = self.players[self.currentPlayer]
        index = self.selectResource()
        resource = self.resourceDicts[index]
        total = 0
        for p in self.players:
            if p != player:
                total += resource[player]
                resource[player] = 0
        resource[player] += total

    def playDevelopment(self):
        '''Plays the "development" card '''
        player = self.players[self.currentPlayer]
        index = self.selectResource()
        resource = self.resourceDicts[index]
        resource[player] += 2 

    def devCardPressed(self, i):
        '''Tries to play a dev card if one was pressed'''
        player = self.players[self.currentPlayer]
        if self.devCardDicts[i][player]<1:
            self.pendingMessage=False
            self.redrawAll()
            self.errorMsg("You have 0 of those")            
        else: 
            self.pendingMessage=False
            self.usingDevCard = False
            self.redrawAll()
            if i != 1: self.devCardDicts[i][player] -= 1
            if i == 0:
                self.initMoveRobber()
            if i == 1:
                self.errorMsg("You don't need to play those!")
            if i == 2:
                self.playMonopoly()
            if i == 3:
                self.freeRoads[player] += 2
            if i == 4:
                self.playDevelopment()
            #self.updateDevCards()

    def cBoxMousePressed(self, (x,y)):
        '''Handles mouse presses when a conformation box is in the forground'''
        if self.error == True:
            self.redrawAll()
            self.pendingMessage = False
            self.error=False
        else:
            if self.trading:
                for b in xrange(len(self.tradeButtonList)):
                    button = self.tradeButtonList[b]
                    if button.pressed(x, y):
                        self.answer = b
                self.pendingMessage = False
                self.redrawAll()  
            if self.usingDevCard:
                for b in xrange(len(self.devCardButtons)):
                    if self.devCardButtons[b].pressed(x, y):
                        self.devCardPressed(b)
            try:
                if self.noButton.pressed(x,y):
                    self.pendingMessage = False
                    self.answer = False
                    self.redrawAll()
                elif self.yesButton.pressed(x,y):
                    self.pendingMessage = False
                    self.answer = True
                    self.redrawAll()
            except:
                pass

    def updateTimer(self):
        '''Uses the milisecond time to update the timer'''
        #pygame.time.set_timer(USEREVENT+1, 1000)
        #subtract amount of time since last turn from the time limit
        time = self.timeLimit - (pygame.time.get_ticks()-self.baseTime)
        if time < 0:
            self.changePlayer(True)
        humanTime = self.getHumanTime(time)
        self.timeButton.setText(humanTime)
        #if you update over a message the message will disapear
        while self.pendingMessage == True and self.run==True:
            self.timerFired()
        self.redrawAll()

    def timerFired(self):
        '''Event handler'''
        if self.gameOver == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                        self.run = False
                        pygame.quit()
                        break
                elif self.pendingMessage:
                    if event.type == MOUSEBUTTONDOWN:
                        self.cBoxMousePressed(event.pos)
                elif self.movingRobber:
                    if event.type == MOUSEBUTTONDOWN:
                        self.moveRobber(event.pos)
                elif self.waitForDevCard: 
                    pass 
                    #if event.type == MOUSEBUTTONDOWN:
                    #    self.checkDevCard(event.pos)
                else:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mousePressed(event.pos)
                    elif event.type == KEYDOWN:
                            #test the ability for the board to build
                        if event.key == K_t:
                            self.test()
                        #test the confirmation box
                        elif event.key == K_c:
                            self.testMode = True
                        elif event.key == K_m:
                            self.initMoveRobber()
                        elif event.key == K_r:
                            self.rollDice(7)
                        elif event.key == K_d:
                            self.testDevCards()
                        elif event.key == K_DOWN: pass 
                        elif event.key == K_UP:
                            self.changePlayer()
                        elif event.key == K_LEFT: pass
                        elif event.key == K_RIGHT: pass
                    elif event.type == USEREVENT+1:
                        self.updateTimer()

    def testDevCards(self): pass
#        '''cheat test function'''        
#        player = self.currentPlayer
#        for d in self.devCardDicts:
#            d[player] = 1
#    
    def test(self): pass 
#        '''cheat test function'''
#        player = self.players[self.currentPlayer]
#        for resource in self.resourceDicts:
#            resource[player] = 4
#        self.redrawAll()

    def mousePressed(self, (x, y)): 
        ''' checs if a vertex, then a road, then a botton was pressed halting 
        if any of the previous were. This prevents overlap problems'''
        #if a vertex was not pressed, check if a button was
        if self.checkVertexPressed(x,y) == (-1,-1):
            if self.roadPressed(x, y) == (-1,-1):
                self.checkButtonPresses(x, y)

    def roadPressed(self, x, y):
        '''checks if the area around a road was pressed, the tries to 
            buils ar road if it was pressed'''
        cols, rows  = self.settlementCols, self.settlementRows
        roadKeys = self.roads.keys()
        for key in self.roads:
            player = self.roads[key]
            #if there is a road there
            spotA = key[0]
            spotB = key[1]
            pointA = self.getVertexCoordinates(spotA[0],spotA[1])
            pointB = self.getVertexCoordinates(spotB[0],spotB[1])
            Ax, Ay = pointA
            Bx, By = pointB
            #if there is no road there now, and is it is within the "box"
            #made by the points
            if (player == 0 and ((x<=Ax and x>=Bx) or (x<=Bx and x >=Ax)) and
                        ((y<Ay and y>By) or (y<By and y>Ay) or (Ay == By))):
                d1 = self.distance((x,y), pointA)
                d2 = self.distance((x,y), pointB)
                #within a given tolereance of the 
                epsilon = self.hexSideLegnth*1.5
                if d1+d2 <= epsilon:
                    self.buildRoad(key, self.currentPlayer)
        return (-1,-1)

    def buildRoad(self, road, player):
        '''Builds a road if the player confirms and it is legal'''
        self.drawConfirmationBox("Are you sure you want to build a road there?")
        while self.answer == None and self.run == True:
            self.timerFired()
        if self.answer == True:
            if self.checkLeagalRoad(road[0], road[1]) and self.buyRoad():
                self.roads[road] = player+1
        self.redrawAll()

    def buyRoad(self):
        '''If the current player can buy the road, returns true and 
        spends the resources to do so. It otherwise returns an 
        error Message and False'''
        player = self.players[self.currentPlayer]
        if self.freeRoads[player] > 0:
            self.freeRoads[player] -= 1 
            return True
        #checks for sufficient resources
        if self.brick[player] < 1 or self.wood <1:
            self.errorMsg('''You do not have enough resources to build a Road
                            You need:
                            Brick X 1 
                            Wood X 1''')
            return False
        else:
            #spends resources
            self.wood[player] -= 1
            self.brick[player] -= 1
            return True

    def distance(self, (x1,y1),(x2,y2)):
        '''returns the distance between two points'''
        dx = x1-x2 
        dy = y1-y2
        dist = ((dx**2) + (dy**2))**0.5 
        return dist

    def selectResource(self, r=None):
        '''Creates a pop-up with resources to select. optional argument r is 
            an omitted resource durring trades'''
        self.trading = True
        self.drawConfirmationBox("Select the resource you wish to recieve:",
            "top", True)
        #self.tradeButtons = []
        width = self.boxSizeX
        #centers the boxes
        x = self.width/2 - width/2
        #dy is initially half the number of buttons, it is the yoffset
        dy = int(round(len(self.tradeButtonList)/2.0))
        if r != None: dy -=1 
        for b in xrange(len(self.tradeButtonList)):
            if b != r: #skips the inputed resource
                y = self.height/2-1.5*self.playerFontSize*(dy)
                button = self.tradeButtonList[b]
                button.setCoords(x,y,width, self.playerFontSize)
                self.drawButton(button, color.black, self.resourceColors[b], 
                    self.playerFontSize)
                dy -= 1 
        pygame.display.flip()
        while self.answer == None and self.run == True:
            self.timerFired()
        self.initTradeButtons() #resets the buttons
        return self.answer

    def selectDevCard(self, r=None):
        '''Plays a dev card the user choses'''
        self.usingDevCard = True
        self.drawConfirmationBox("Select the DevCard you wish to use:",
            "top", True)
        player = self.players[self.currentPlayer]
        #self.tradeButtons = []
        width = self.boxSizeX
        #centers the boxes
        x = self.width/2 - width/2
        #dy is initially half the number of buttons, it is the yoffset
        dy = int(round(len(self.devCardDicts)/2.0))
        if r != None: dy -=1 
        for c in xrange(len(self.devCardDicts)):
            y = self.height/2-1.5*self.playerFontSize*(dy)
            button = self.devCardButtons[c]
            button.setCoords(x,y,width, self.playerFontSize)
            numb = self.devCardDicts[c][player]
            title = self.devCardNames[c] 
            text = title + " X " + str(numb) 
            button.setText(text)
            self.drawButton(button, color.black, color.gold, 
                self.playerFontSize)
            dy -= 1 
        pygame.display.flip()
        while self.pendingMessage == True and self.run == True:
            self.timerFired()
        self.usingDevCard = False

    def bankTrade(self, r):
        '''Trades the resource, r, with to the bank'''
        player = self.players[self.currentPlayer]
        tradeValue = self.tradeValue[r][player]
        resource = self.resourceList[r]
        if self.resourceDicts[r][player] < tradeValue:
            self.errorMsg("You need %d %ss to trade with the bank!" %(tradeValue, resource))
        text = "Would you like to trade in %d %ss for 1 of another resource?" %(tradeValue, resource) 
        self.drawConfirmationBox(text)
        print "here!"
        while self.answer == None and self.run == True:
            self.timerFired()
        if self.answer == True:
            tradeResource = self.selectResource(r)
            if type(tradeResource) == int:
                self.resourceDicts[r][player] -= tradeValue
                self.resourceDicts[tradeResource][player] += 1
        self.redrawAll() 

    def checkButtonPresses(self, x, y):
        '''Checks if one of the buttons was press and calls the 
            functon corisponding to the button that was pressed'''
        if self.endTurn.pressed(x, y):
            self.drawConfirmationBox("Do you want to end your turn?")
            while self.answer==None and self.run == True:
                self.timerFired()
            if self.answer == True:
                self.changePlayer()
        for b in xrange(len(self.resourceButtons)):
            if self.resourceButtons[b].pressed(x, y):
                self.bankTrade(b)
        if self.useDevCardButton.pressed(x, y):
            self.selectDevCard()
        elif self.buyDevCardButton.pressed(x,y):
            self.buyDevCard()

    def buyDevCard(self):
        '''Buys a dev card. They are assigned randomly from a finite deck'''
        player = self.players[self.currentPlayer]
        if (self.sheep[player] <1 or self.wheat[player] <1 
                or self.stone[player] <1):
            self.errorMsg('''You do not have enough resources to buy a DevCard.
                            You need:
                            Sheep X 1
                            Wheat X 1
                            Stone X 1''')
        else:
            #buy it
            self.sheep[player] -= 1
            self.wheat[player] -= 1 
            self.stone[player] -= 1
            #pick a random devCard 
            legnth = len(self.allDevCards)-1 
            if legnth >0:
                index = random.randint(0, legnth)
                card = self.allDevCards.pop(index)
                self.devCardDicts[card][player] += 1
                if self.devCardDicts[card] == 1:
                    self.victoryPoints[player] += 1 
            #self.updateDevCards()

    def checkVertexPressed(self, x, y):
        '''checks if a vertex was clicked on, then tries to build there if 
            one was'''
        cols, rows  = self.settlementCols, self.settlementRows
        #loops through all possible points where there could 
        # be a vertex
        for row in xrange(rows):
            for col in xrange(cols):
                vertex = self.vertexList[row][col]
                #if there is a vertex at that point on the board
                if type(vertex) == tuple:
                    vX = self.vertexList[row][col][0]
                    vY = self.vertexList[row][col][1]
                    #if it is near a vertex, try to build there
                    if self.almostEquals(x, vX) and self.almostEquals(y, vY):
                        self.build(row, col)
                        return (row, col)
        #if a vertex was not pressed 
        return (-1,-1)

    def moveRobber(self, (x, y)):
        '''moves the robber'''
        cols, rows  = self.boardCols, self.boardRows
        prow,pcol = self.robber
        for row in xrange(rows):
            for col in xrange(cols):
                center = self.centerList[row][col]
                if center != None:
                    epsilon = self.hexSideLegnth/4
                    xc = center[0]
                    yc = center[1]
                    if (self.almostEquals(x,xc, epsilon) 
                    and self.almostEquals(y,yc, epsilon)):
                        if row != prow or col != pcol:
                            self.robber = (row, col)
                            self.redrawAll()
                            self.movingRobber = False
                            break
                        else:
                            self.errorMsg("You must move the robber to a new spot")

    def initMoveRobber(self):
        '''Starts the process of moving the robber'''
        self.drawConfirmationBox('''Click on a hex to move the robber there.
            Press no to cancel.''')
        while self.answer == None and self.run ==True:
            self.timerFired()
        if self.answer == True:
            self.movingRobber = True
            return True
        else:
            return False

    def tryMoveRobber(self, row, col):
        '''Checks if the spot is not the current position of the robber'''
        if self.robber != (row, col):
            return True

    def build(self, row, col):
        '''Detects which building to build and builds it 
            (if legal and player confirms)'''
        #don't build anything if the move is not leagal
        if not self.checkLeagalBuild(row, col): return False
        if self.buildings[row][col] > 0:
            self.buildCity(row, col)
        elif self.buildings[row][col] == 0:
            self.buildSettlement(row, col)

    def buildCity(self, row, col):
        '''builds a city if the player says yes and it is legal'''
        self.drawConfirmationBox("Do you want to build a city?")
        #this blocks while we wait for an answer
        while self.answer == None and self.run == True:
            self.timerFired()
        if self.answer == True:
            #checks available resources and spends them or returns an error
            if self.buyCity():
                #place a city
                self.buildings[row][col] += self.totalPlayers
                #add a victory point 
                self.victoryPoints[self.players[self.currentPlayer]] += 1 
                self.redrawAll()

    def buildSettlement(self, row, col):
        '''builds a settlement if the player says yes and it is legal'''
        player = self.players[self.currentPlayer]
        self.drawConfirmationBox("Do you want to build a settlement?")
        while self.answer == None and self.run == True:
            self.timerFired()
        if self.answer == True:
            #checks available resources and spends them or returns an error
            if self.buySettlement():
                #place a settlement
                self.buildings[row][col] = self.currentPlayer+1
                #add a victory point
                self.victoryPoints[player] += 1 
                if self.countBuildings(self.currentPlayer) == 2:
                    self.initFirstResources(player, row, col)
        self.redrawAll()      

    def buyCity(self):
        '''checks if the player has enough resources/free citties
        to build a citty, and spends said resources'''
        player = self.players[self.currentPlayer]
        #checks if they have enough reources
        if self.wheat[player] < 2 or self.stone[player] < 3:
            self.errorMsg('''You do not have enough resources to build a City.
                                It requires: \n Wheat X 2 \n Stone X 3''')
            return False
        else: 
            self.wheat[player] -= 2
            self.stone[player] -= 3
            return True
        return True

    def buySettlement(self):
        '''checks if the player has enough resources/free settlements
        to build a settlement, and spends said resources'''
        player = self.players[self.currentPlayer]
        #checks if they have a free settlement
        if self.freeSettlements[player] > 0: 
            self.freeSettlements[player] -= 1 
            return True
        #checks if they have enough reources
        if (self.brick[player] < 1 or self.wood[player] < 1 or 
            self.wheat[player] < 1 or self.sheep[player] < 1):
            error = '''You do not have enough resources to build a Settlement.
                    It requires: \n Brick X 1 \n Wood X 1 \n Wheat X 1
                     Sheep X 1'''
            self.errorMsg(error)
            return False
        else: 
            self.brick[player] -= 1 
            self.wood[player] -= 1 
            self.wheat[player] -= 1 
            self.sheep[player] -= 1
            return True

    def checkLeagalRoad(self, (row1, col1), (row2, col2)):
        '''checks if you can build a road from (row1, col1) to (row2, col2)'''
        #if it is adjacent to one of your buildings
        if (self.buildings[row1][col1] == self.currentPlayer+1 or 
        self.buildings[row1][col1] == self.currentPlayer+1+self.totalPlayers 
        or self.buildings[row2][col2] == self.currentPlayer+1 or 
        self.buildings[row2][col2] == self.currentPlayer+1+self.totalPlayers):
            return True
        rows, cols =  self.settlementRows, self.settlementCols
        dirs =  [(-1,-1),(-1,0),(-1,1),
                 ( 0,-1),       ( 0,1),
                 ( 1,-1),( 1,0),( 1,1)]
        roads = self.roads
        road1 = ((row1, col1), (row2, col2))
        road2 = ((row1, col1), (row2, col2))
        if road1 in roads: road = road1 
        if road2 in roads: road = road2 
        ((r1, c1), (r2, c2)) = road
        #finds if the road is adjacent to another road
        if (self.isPartOfRoad(r1, c1) or self.isPartOfRoad(r2, c2)):
            return True
        else:
            self.errorMsg("You cannot build a disconnected road!")
        return False

    def isPartOfRoad(self, row, col): 
        '''checks if the vertex is connected to a road'''
        rows, cols =  self.settlementRows, self.settlementCols
        if (row < 0 or col < 0 or row >= rows or col >= cols): return False
        if type(self.buildings[row][col]) != int: return False
        dirs =  [(-1,-1),(-1,0),(-1,1),
                 ( 0,-1),       ( 0,1),
                 ( 1,-1),( 1,0),( 1,1)]
        player = self.currentPlayer+1 
        for (drow, dcol) in dirs:
            arow, acol = row + drow, col + dcol
            acord = (arow, acol)
            if (arow >= 0 and acol >= 0 and arow < rows and acol<cols and 
                (type(self.buildings[arow][acol]) == int) and 
                ((((row,col),acord) in self.roads and 
                    self.roads[((row,col),acord)]==player)  or 
                (((acord,(row,col)) in self.roads) and 
                    self.roads[(acord,(row,col))]==player))):
                return True
        return False

    def checkLeagalBuild(self, row, col): 
        '''Returns true if the build folows the rules, false otherwise'''
        dirs =  [(-1,-1),(-1,0),(-1,1),
                 ( 0,-1),       ( 0,1),
                 ( 1,-1),( 1,0),( 1,1)]
        rows, cols =  self.settlementRows, self.settlementCols
        board = self.buildings
        if board[row][col] != 0 and board[row][col] != self.currentPlayer+1:
            self.errorMsg("You can't build ontop of someone else!")
            return False
        elif (board[row][col] == 0 and not self.isPartOfRoad(row,col) 
                    and self.turn > 1):
            self.errorMsg("You must build a road to that settlement!")
            return False
        for (drow, dcol) in dirs:
            arow, acol = row + drow, col + dcol
            #if the spot is not on the board
            if arow >0 and acol >0 and arow < rows and acol<cols:
                #if the spot is a settlement or city (and the proposed building
                #    is adjacent to another building)
                spot = board[arow][acol]
                if type(spot) == int and spot !=0:
                    text = '''You must maintain at least one space inbetween 
                            every building!'''
                    self.errorMsg(text)
                    return False
        return True

    def almostEquals(self, a, b, epsilon=0):
        if epsilon == 0: epsilon = self.hexSideLegnth/6
        return abs(a-b) <= epsilon

    def rollDice(self, rigged = None):
        '''rolls the dice'''
        if rigged == None:
            self.die1 = random.randint(1, 6)
            self.die2 = random.randint(1, 6)
        else:
            self.die1 = rigged/2 
            self.die2 = rigged - self.die1
        self.resourceSum = self.die1 + self.die2
        for key in self.probs:
            if (self.probs[key] == self.resourceSum 
                and self.robber != key):
                self.getResources(key)
        if self.resourceSum == 7:
            self.removeHalfCards()
            self.initMoveRobber() 
        self.redrawAll

    def removeHalfCards(self):
        '''removes half of each player's cards for each player that 
            has more than 7 cards randomly'''
        resourceList = []
        #make a list of the resources storing them as an int
        for player in self.players:
            for r in xrange(len(self.resourceDicts)):
                resource = self.resourceDicts[r]
                for i in xrange(resource[player]):
                    resourceList += [r]
            if len(resourceList) > 7:
                print "here"
                #resets the cureent values
                for r in self.resourceDicts:
                    r[player] = 0
                half = int(round(len(resourceList)/2.0))
                print half
                #makes a list with half the resources (rounded up)
                currentResources = []
                for c in xrange(half):
                    index = random.randint(0,len(resourceList)-1)
                    currentResources += [resourceList.pop(index)]
                print currentResources
                #adds the resources back
                for r in currentResources:
                    self.resourceDicts[r][player] += 1
                self.redrawAll()

    def getResources(self, (row, col)):
        '''gives a resource to all buildings around a given hexagon at 
        (row, col)'''
        resource = self.resources[row][col]
        resourceDict =  self.resourceDicts[resource]
        #converts the col from a board col to a vertex col
        bcol = 2*col
        #these are the change from the middle left vertex of the the hexagon
        #to get all of the vertecies
        dirs = [(0,0),(-1,1),(-1,2),(0,3),(1,1),(1,2)]
        for (drow, dcol) in dirs:
            nrow, ncol = row + drow, bcol+dcol
            building = self.buildings[nrow][ncol]
            if building > 0:
                #add 1 if it is a settlement
                if building <= self.totalPlayers:
                    player = self.players[building-1]
                    resourceDict[player] += 1 
                #add 2 if it is a city
                elif building <= 2*self.totalPlayers:
                    player = self.players[building - self.totalPlayers-1]
                    resourceDict[player] += 2 

    def makeResourceSums(self):
        '''Assigns probablities to each hexagon'''
        cols, rows  = self.boardCols, self.boardRows
        orderSumsList =[2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        self.probs = {}
        for row in xrange(rows):
            for col in xrange(cols):
                resource = self.resources[row][col]
                if resource != None and resource != 5:
                    index = random.randint(0, len(orderSumsList)-1)
                    dieSum = orderSumsList.pop(index)
                    self.probs[(row,col)] = dieSum

    def makeResourceList(self):
        '''Assigns resources to each hexagon'''
        #key: 0:wood, 1:brick, 2:stone, 3:sheep, 4:wheat, 5:desert
        #number of each wood:4, brick:4, ore:4, sheep:3, wheat:3, desert:1
        orderedResourceList = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,4,4,4,5]
        cols, rows  = self.boardCols, self.boardRows
        #init the resource 2d list
        self.resources = [[None for col in xrange(cols)]\
                            for row in xrange(rows)]
        #the board this makes is also the board "draw board uses"
        for row in xrange(rows):
            for col in xrange(cols):
                #first elimintes the corners and overflow eges
                if (row != 0 and (row != rows-1 or (col != 0 and 
                    col != cols-1)) and (row != 1 or (col != 0 and 
                    #the mod interweaves the hexagons
                    col != cols-1)) and (row-col)%2 == 1): 
                    #pick a random resource from the ones that are left
                    index = random.randint(0,len(orderedResourceList)-1)
                    resource = orderedResourceList.pop(index)
                    self.resources[row][col] = resource
                    if resource == 5: self.robber = (row, col)

    def makeVertexList(self):
        '''Makes the a list of the coordinates of the verticies'''
        cols, rows  = self.settlementCols, self.settlementRows 
        self.vertexList = [[None for col in xrange(cols)]\
                             for row in xrange(rows)]
        for row in xrange(rows):
            for col in xrange(cols):
             if type(self.buildings[row][col]) == int:
                self.vertexList[row][col] = self.getVertexCoordinates(row, col)

    def makeCentersList(self):
        '''Initializes the board of hexagons (resource and probablity)'''
        cols, rows  = self.boardCols, self.boardRows
        self.centerList = [[None for col in xrange(cols)]\
                             for row in xrange(rows)]
        for row in xrange(rows):
            for col in xrange(cols):
                if self.resources[row][col] != None:
                    bcol = 2*col
                    x,y = self.getVertexCoordinates(row, bcol)
                    x += self.hexSideLegnth
                    self.centerList[row][col] = (x, y)

    def makeBuildingList(self):
        '''Initializes the board of buildings'''
        cols, rows  = self.settlementCols, self.settlementRows 
        #first makes an empty lists, then fills it with the values
        self.buildings = [[None for col in xrange(cols)]\
                             for row in xrange(rows)]
        for row in xrange(rows):
            for col in xrange(cols):
                #only add a 0 where there is a vertex (not in the middle of)
                if (((row%2 == 0) and (col%4 == 1 or col%4 == 2) 
                    or (row%2 == 1 and (col%4 == 0 or col%4 == 3))) and 
                    #hardcode removing corners
                    #first don't mess with normal rows
                    ((row > 1 and row < rows - 2) or 
                    #first row and last row
                    ((row == 0 or row == rows -1) and 
                    col > cols/2 -2 and col < cols/2+2 ) or
                    #second row and second to last row
                    ((row == 1 or row == rows-2) and 
                    col > cols/2 -4 and col < cols/2+4))): 
                    #put a 0 for no settlement
                    self.buildings[row][col] = 0

    def makeRoadList(self):
        '''Makes a dictionary that storys the roads as a 2d tuple of
        vertecies'''
        self.roads = {}
        #only half the direcctions to define an order of the vertexes 
        dirs =  [(1,1),(1,0),(1,-1),( 0,1)]
        rows, cols =  self.settlementRows, self.settlementCols
        board = self.buildings
        for row in xrange(rows):
            for col in xrange(cols):
                if type(board[row][col]) == int:
                    for (drow, dcol) in dirs:
                        arow, acol = row + drow, col + dcol
                        #is the spot is on the board
                        if (arow >=0 and acol>=0 and arow<rows and acol<cols
                        #if the spot is a vertex
                        and type(board[arow][acol]) == int):
                            #the dictionary entries are the player (+1) who
                            #owns that road
                            index = ((row,col),(arow,acol))
                            self.roads[index] = 0

    def initTurn(self):
        '''Starts the turn'''
        self.checkWin()
        if self.gameOver == False:
            self.baseTime = pygame.time.get_ticks()
            self.redrawAll()
            player = self.players[self.currentPlayer]
            #Checks if the want to play a dev Card - some must be used before they roll
            #only asks if they have a dev card to use
            if self.soldiers[player] > 0:
                text="Would you like to use a soldier before you roll?"
                self.drawConfirmationBox(text)
                while self.answer == None and self.run == True:
                    self.timerFired()
                if self.answer == True:
                    self.soldiers[player] -= 1
                    self.initMoveRobber()
            if self.turn > 1: self.rollDice()
        self.redrawAll()

    def deadTime(self):
        '''Times the time where no one is playing the game'''
        #draws communal functions
        self.redrawAll(False)
        self.drawPassBox("Pass the computer to %s."
                % self.players[self.currentPlayer])
        while self.pendingMessage == True and self.run == True:
            self.timerFired()


    def changePlayer(self, Forced=False): 
        '''Changes the current player if it is legal to do so'''
        if Forced==True or self.legalEndTurn():
            if self.currentPlayer == self.totalPlayers-1: 
                self.turn += 1
            #deals with the edge case of round 2(turns = 1)
            #in that turn players revers order
            if self.turn == 1:
                #gives people their second free settlement/road
                if self.currentPlayer == self.totalPlayers-1:
                    self.initFirstSettlements()
                #rests the game back to normal order
                if self.currentPlayer == 0:
                    self.turn += 1
                #change players backwards
                else:
                    self.currentPlayer -=1
                self.redrawAll()
            else:
                #rotates players in the normal case
                self.currentPlayer += 1 
                self.currentPlayer %= self.totalPlayers
            self.deadTime()
            self.initTurn()

    def legalEndTurn(self):
        '''Checks if the player can end their turn'''
        if self.testMode == True: return True
        player = self.players[self.currentPlayer]
        #the player cannot end their turn with "free" stuff
        if self.freeSettlements[player] > 0 :
            message = "You must build your free setlement before you can finnish your turn."
            self.errorMsg(message)
            return False
        elif self.freeRoads[player] > 0:
            message = "You must build your free road before you can finnish your turn."
            self.errorMsg(message)
            return False
        else:
            return True

    def checkWin(self):
        '''in accordance with the rules of Catan checks if 
        the current player, but only the current player, has won'''
        player = self.players[self.currentPlayer]
        if self.victoryPoints[player] >= self.winPoints:
            self.winner = player
            self.gameOver = True
            self.redrawAll()
    
    def __init__(self, timeLimit, infoList, width = 1000, height = 750):
        pygame.init()
        self.width = width
        self.height = height
        self.gameOver = False
        self.winPoints = 10 
        self.winner = None
        self.trading = False
        self.testMode = False
        self.movingRobber = False
        self.usingDevCard = False 
        self.turn = 0 
        self.hexSideLegnth = (width*3/(4.0*12))
        self.timeLimit = timeLimit*60*1000
        self.initPlayers(infoList)
        self.die1 = self.die2 = 0
        self.screen = pygame.display.set_mode((width, height))
        self.waitForDevCard = False
        self.initFontsAndColors()
        self.initBoard()
        self.initTime()
        self.makeBuildingList()
        self.makeVertexList()
        self.makeCentersList()
        self.makeRoadList()
        self.pendingMessage = False
        self.initButtons()
        self.error = False
        self.run = True
        self.baseTime = pygame.time.get_ticks()
        self.redrawAll()
        self.mainLoop()

    def getHumanTime(self, miliSec):
        '''Converts between number of miliseconds and min:sec timer forat'''
        secs = miliSec/1000.0
        mins = int(secs/60.0) 
        seconds = int(round(secs-mins*60))
        #print miliSec, secs, mins, seconds
        #format timer text
        if mins < 10:
            minText = "0"+str(mins)
        else:
            minText = str(mins) 
        if seconds<10:
            secText = "0"+str(seconds)
        else:
            secText = str(seconds)
        text = "%s:%s"% (minText, secText)
        return text

    def initTime(self):
        '''Starts and creates the timer'''
        self.clock = pygame.time.Clock()
        self.timeLeft = self.timeLimit
        width = self.hexSideLegnth*2 
        height = self.hexSideLegnth
        text = self.getHumanTime(self.timeLeft)
        self.timeButton = Button(self.hexSideLegnth/2, self.hexSideLegnth/2, 
                                width, height, text)
        pygame.time.set_timer(USEREVENT+1, 100)

    def initButtons(self):
        '''Creates all the button objectes for the game'''
        left = int(self.hexSideLegnth/2)
        bottom = int(self.height - self.hexSideLegnth/2) 
        height = int(.75*self.hexSideLegnth)
        width = self.hexSideLegnth*2 
        self.endTurn = Button(left, bottom-height, width, height, "End Turn")
        self.buyDevCardButton = Button(left+width*1.75, bottom-height, 
                                            width, height, "Buy")
        self.useDevCardButton = Button(left+width*3, bottom-height, 
                                            width, height, "Use")
        self.myStone = Button()
        self.myBrick = Button()
        self.myWood = Button()
        self.myWheat = Button()
        self.mySheep = Button()
        self.resourceButtons = [self.myWood, self.myBrick, self.myStone, 
                            self.mySheep, self.myWheat]
        x = self.playerBoxX0
        for r in xrange(len(self.resourceButtons)):
            y = self.playerBoxY0+self.boxSizeY+1.5*self.playerFontSize*(r)
            #sets the size of the button - this doesn't change but the text does
            self.resourceButtons[r].setCoords(x, y, 
                self.boxSizeX, 1.5*self.playerFontSize)
        self.initTradeButtons()

    def initTradeButtons(self):
        '''Create the button objects to trade with the bank'''
        self.woodTButton = Button()
        self.brickTButton = Button()
        self.stoneTButton = Button()
        self.sheepTButton = Button()
        self.wheatTButton = Button()
        self.tradeButtonList = [self.woodTButton, self.brickTButton, self.stoneTButton,
                            self.sheepTButton, self.wheatTButton]
        for b in xrange(len(self.tradeButtonList)):
            button = self.tradeButtonList[b]
            text = self.resourceList[b]
            button.setText(text)

    def initPlayers(self, infoList):
        '''Initializes the players'''
        self.players = []
        for person in infoList: self.players += [person[0]]
        self.initDicts()
        self.playerColors = []
        for person in infoList: self.playerColors += [person[1]] 
        self.currentPlayer = 0 
        self.totalPlayers =  len(self.players)
        self.playerBoxX0 = self.hexSideLegnth
        self.playerBoxY0 = self.hexSideLegnth*2
        self.boxSizeX = self.hexSideLegnth*5
        self.boxSizeY = self.hexSideLegnth*(len(self.players))

    def initDicts(self):
        '''initializes all of the dictionaries for the game parts'''
        self.stone = {}
        self.wheat = {}
        self.wood = {}
        self.brick = {}
        self.sheep = {}
        self.victoryPoints = {}
        self.resourceList = ["Wood", "Brick","Stone","Sheep","Wheat"]
        self.resourceDicts = [self.wood, self.brick, self.stone, 
                self.sheep, self.wheat]
        dicts = self.resourceDicts + [self.victoryPoints]
        for player in self.players:
            for d in dicts:
                d[player] = 0
        self.devCards = {}
        for player in self.players:
            self.devCards[player] = []
        self.initFirstSettlements()
        self.initTrades()
        self.initDevCards()

    def initDevCards(self):
        '''initializes the devcard dicts'''
        self.soldiers = {}
        self.victoryPointCard = {}
        self.monopoly = {}
        self.roadBuilding = {}
        self.development = {}
        self.devCardDicts = [self.soldiers, self.victoryPointCard,
            self.monopoly, self.roadBuilding, self.development]
        self.soldiersB = Button()
        self.victoryPointsB = Button()
        self.monopolyB = Button()
        self.roadBuildingB = Button()
        self.developmentB = Button()
        self.devCardButtons = [self.soldiersB, self.victoryPointsB, 
        self.monopolyB, self.roadBuildingB, self.developmentB]
        for player in self.players:
            for d in self.devCardDicts:
                d[player] = 0 
        self.devCardNames=["Soldier", "Victory Point", "Monopoly", 
                "Road Building", "Year of Plenty"]
        #14 Soldiers, 5 VPs, 2 Monopoly, 2 Road Building, 2 Development, 
        self.allDevCards = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,2,3,3,4,4]

    def updateDevCards(self):
        '''updates the devcard dicts'''
        player = self.currentPlayer
        total = 0
        self.devCards = {}
        for d in self.devCardDicts:
            total += d[player]
        self.devCards[player] = total

    def initTrades(self):
        '''creates dictionaries of trade ratios'''
        self.stoneT = {}
        self.wheatT = {}
        self.woodT = {}
        self.brickT = {}
        self.sheepT = {}
        self.tradeValue  = [self.woodT, self.brickT, self.stoneT, 
                self.sheepT, self.wheatT]
        for d in self.tradeValue:
            for player in self.players:
                # ratio value (x:1) is stored in as an integer x
                d[player] = 4

    def initFirstSettlements(self):
        '''gives each player 1 free road and 1 free settlement,
        except the last player who goes twice'''
        self.freeRoads = {}
        self.freeSettlements = {}
        last = len(self.players)-1
        for player in self.players[0:last]:
            self.freeSettlements[player] = 1 
            self.freeRoads[player] = 1 
        #deals with the edge case of the last player, who goes twice
        lastPlayer = self.players[last]
        if self.turn == 0:
            self.freeSettlements[lastPlayer] = 2 
            self.freeRoads[lastPlayer] = 2 
        else:
            self.freeSettlements[lastPlayer] = 0
            self.freeRoads[lastPlayer] = 0

    def initFirstResources(self, player, row, col):
        '''Gives the players the resources around their secong setlement'''
        #don't go off the board
        rows, cols = self.settlementRows, self.settlementCols
        #if it is on the middle left a infanite the hex
        #board (magic mod math), fist condition, right side second
        if col%2 == 0: 
            dirs = [(-1,-2),(1,-2),(0,0)]
        else:
            dirs = [(-1,-1),(1,-1),(0,-3)]
        for (drow, dcol) in dirs:
            nrow, ncol = row +drow, col+dcol
            #stays on the board 
            if nrow >= 0 and ncol >= 0 and nrow<rows and ncol<cols:
                bcol = ncol/2 
                #get the index of the resource
                #stays on the booard
                if bcol < self.boardCols and nrow < self.boardRows:
                    index = self.resources[nrow][bcol]
                    if index != None and index != 5: #stays on the booard
                        #get that resource's dictionary
                        resource = self.resourceDicts[index]
                        #add 1 to that player's resource
                        resource[player] += 1

    def countBuildings(self, player):
        '''Counts the number of cities or settlements built'''
        #counts a players settlemnts
        rows, cols = self.settlementRows, self.settlementCols
        total = 0
        for row in xrange(rows):
            for col in xrange(cols):
                building = self.buildings[row][col]
                #checks if there is a building there 
                if (building == player+1 or 
                    building == player+1+self.totalPlayers):
                    total += 1 
        return total

    def initBoard(self):
        '''initilaizes the board and the resources'''
        #sets up some inital board values
        width = self.width
        height = self.height
        #Changing the rows & cols would possible break some parts of the game
        self.boardCols = 5 
        self.boardRows = 10
        #center the board in bottom right side
        self.boardX = 3.0*width/4 - self.boardCols*self.hexSideLegnth
        self.boardY = height/2.0 - .33*self.boardRows*self.hexSideLegnth
        self.boardColor = color.boardColor
        self.settlementCols = (self.boardCols +1)*2 
        self.settlementRows = self.boardRows +1
        #key: 0:wood, 1:brick, 2:stone, 3:Sheep, 4:wheat, 5:desert
        self.resourceColors=[color.forestGreen,color.red,color.gray,
            color.green,color.brown,color.yellow]
        self.makeResourceList()
        self.makeResourceSums()

    def mainLoop(self):
        '''keeps the game running'''
        while self.run == True:
            self.timerFired()

class Button(pygame.sprite.Sprite):
#class Button(object):
    def init(self):
        self.__init__()

    def __init__(self, x0=0, y0=0, width=0, height=0, 
                text="", buttonColor=(255, 228, 76)):#default color is gold
        #initaliazes settings
        self.x0 = x0 
        self.y0 = y0 
        self.x1 = x0 + width 
        self.y1 = y0 + height
        self.width = width 
        self.height = height
        self.text = text
        self.color = buttonColor
        self.colorIndex = None

    def setColorFromList(self, index):
        self.colorIndex = index 
        self.color = color.colorList[index]

    def setText(self, text):
        self.text = text

    def setCoords(self, x0, y0, width, height):
        self.x0 = x0 
        self.y0 = y0 
        self.x1 = x0 + width 
        self.y1 = y0 + height
        self.width = width 
        self.height = height   

    def __len__(self):
        return len(self.text)     

    def pressed(self, x, y): #*args):
        '''button.pressed(x, y) -> bool checks if the given 
        x and y are inside the button'''
        #returns if they are or aren't
        if x > self.x0 and y>self.y0 and x<self.x1 and y < self.y1:
            return True 
        else:
            return False

#####code for testing###

color = Colors()
newgame = KatanSplashScreen()