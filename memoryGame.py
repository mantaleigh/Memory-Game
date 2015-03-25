# Brenna Carver and Samantha Voigt  
# CS111 PSET 10/PROJECT
# Memory Game

from Tkinter import *
import random
import os

#Classes: Actual Memory Game and Starter Window that asks how many images to play with
        
class MemoryGame(Toplevel):
    def __init__(self, numOfImages):
        Toplevel.__init__(self)
        self.title('Memory Game')
        self.grid()
        self.imgList1 = []
        for files in os.listdir(os.getcwd()):
            #check for all files that end in 'gif', excluding 'blank.gif'
            if os.path.isfile(files) and files[(files.rfind('.')+1):] == 'gif' \
            and 'blank' not in files:
                #add each file to list twice for pairs
                self.imgList1.append(files)
                self.imgList1.append(files)
        self.imgList = self.imgList1[0:numOfImages] #Make list of size numImages, which we get from the user in the StarterApp
        self.shuffled = sorted(self.imgList, key=lambda k: random.random()) #shuffe the list randomly
        self.clicks = 0 
        self.matches = 0  
        self.numberOfCells = len(self.imgList) #The number of buttons (cells) to be made, based on the size of the shuffled list
        self.numberOfRows = self.numberOfCells/4 #the number of rows adjusts given the number of cells 
        self.numberOfColumns = 4 #We set number of columns to always be 4, but this can be changed
        self.isFirst = True #Boolean to see if this is the second or first image being clicked
        self.currentImg = StringVar() #Used to save which image was clicked
        self.lastButtonClicked = IntVar() #Used to save what the index of the last button clicked was
        
        #if a high score file for the current level exists, save the previous high score as self.highScore
        if os.path.exists(str(self.numberOfCells*.5)+'ImgHighScore.txt'): 
            highScoreFile = open(str(self.numberOfCells*.5)+'ImgHighScore.txt')
            self.highScore = highScoreFile.read()
            self.highScore = int(self.highScore)
            highScoreFile.close()
        #if a high score file for the current level does not exist, set self.highScore to 'none'
        else: 
            self.highScore = 'None'
        
        self.createWidgets()
    
    def createWidgets(self):
        # variables used to figure out where the buttons should be placed
        rowV = 0 
        columnV = 0 
        # list that will store what buttons are created and so that we can use index values to access them later
        self.buttonList = []
        
        #For loop that creates buttons with images inside
        for i in range(0, self.numberOfCells):
            photo = PhotoImage(file='blank.gif')
            self.button = Button(self, image=photo, command=lambda i=i:self.onButtonClick(i)) #passing the i, which is also the 
                                                                #index of the button created into onButtonClick
            self.button.image = photo
            self.buttonList.append(self.button)
            #conditional statements that use a pattern to place the buttons in the right columns and rows
            if i%self.numberOfColumns==0:
                if i==0:
                    rowV = 0
                    columnV = 0
                else:
                    rowV+=1
                    columnV=0
            else:
                columnV += 1
            self.button.grid(row=rowV, column=columnV)
            
        #Creating labels for number of clicks and matches and high score    
        self.clickResults = StringVar()
        self.matchResults = StringVar()
        self.highScoreResults = StringVar()
        self.clickLabel = Label(self, fg='blue', font='Verdana 14 italic', textvariable=self.clickResults)
        self.clickLabel.grid(row = self.numberOfRows+1, column = self.numberOfColumns-1)
        self.matchLabel = Label(self, fg='blue', font='Verdana 14 italic', textvariable=self.matchResults)
        self.matchLabel.grid(row = self.numberOfRows+2, column=self.numberOfColumns-1)
        self.highScoreLabel = Label(self, fg='darkgreen', font='Verdana 16 bold', textvariable=self.highScoreResults)
        self.highScoreLabel.grid(rows=self.numberOfRows+3, column = 1, columnspan = 2)
        self.clickResults.set('Clicks = ' + str(self.clicks))
        self.matchResults.set('Matches = ' + str(self.matches))
        self.highScoreResults.set('BEST SCORE: ' + str(self.highScore))
        
        #Creating the "New Game" Button and the "Quit" button
        self.newGameButton = Button(self, text='New Game', command=self.onNewGameButtonClick)
        self.newGameButton.grid(row = self.numberOfRows+1, column = 0)
        quitButton = Button(self, text='Quit', command=self.onQuitButtonClick)
        quitButton.grid(row=self.numberOfRows+2, column=0)
        
    def onButtonClick(self, i): #passing in i to use with the button list
        self.clicks += 1 #increment the click counter and update the click label
        self.clickLabel = Label(self, fg='blue', font='Verdana 14 italic', textvariable=self.clickResults)
        self.clickLabel.grid(row = self.numberOfRows+1, column = self.numberOfColumns-1)
        self.clickResults.set('Clicks = '+str(self.clicks))
            
        # If the button is the first clicked...    
        if self.isFirst == True:
            photo = PhotoImage(file=self.shuffled[i]) #change the blank image to the appropriate one
            self.buttonList[i].configure(image=photo)
            self.buttonList[i].image = photo
            self.currentImg.set(self.shuffled[i]) #Update the currentImg var with the name of the first image
            self.lastButtonClicked.set(i) #update the lastButtonClicked var with the index of this image
            self.buttonList[i].configure(state=DISABLED) #Disable the button so that it cannot be clicked again
            self.isFirst = False #self explanatory
         
        # If the button is the second clicked...   
        else:
            photo = PhotoImage(file=self.shuffled[i]) #change the blank image to the appopriate one
            self.buttonList[i].configure(image=photo)
            self.buttonList[i].image = photo
            #If the img for this button is the same as the img for the first button clicked...
            if self.currentImg.get() == self.shuffled[i]:
                self.buttonList[i].configure(state=DISABLED) #disable the second button
                self.matches += 1 #increment the match counter and update the label
                self.matchResults.set('Matches = '+str(self.matches))
                
                #If the game has been won...
                if self.matches == .5*self.numberOfCells:
                    #Display a win label
                    self.winLabel = Label(self, fg='red', font='Verdana 14 italic',\
                    text = 'You won in ' + str(self.clicks) + ' clicks. To play again, click "New Game."')
                    self.winLabel.grid(rows=self.numberOfRows+3, columnspan=self.numberOfColumns)
                   
                    #High Scores
                    #Use the HighScores class to read and write the high score file based on the num of clicks
                    readAndWriteHighScores = HighScores(self.numberOfCells*.5, self.clicks)
                    #If the score for this game is better than the one in the file..
                    if (self.clicks < self.highScore) or (self.highScore == 'None'): 
                        #update self.highScore to the new high score (self.clicks)-- in case the user hits the "newGame" button
                        self.highScore = self.clicks
                        #Update the high score label 
                        self.highScoreResults.set('NEW BEST SCORE: ' + str(self.clicks)+'!')

                    
            # If the two images are not a match... 
            else:
               self.after(300, self.noMatch, i) #after 300 milliseconds, call the noMatch function, again, with i 
            self.isFirst = True #set isFirst back to True
        
        #When the two images are not a match: 
    def noMatch(self, i):
        #Change the first image back to blank.gif
        photo = PhotoImage(file='blank.gif')
        self.buttonList[i].configure(image=photo)
        self.buttonList[i].image = photo
        num = self.lastButtonClicked.get() #Get the index of the last button clicked
        #Use that index to enable the button and make its img blank.gif
        self.buttonList[num].configure(state=NORMAL)
        photo = PhotoImage(file='blank.gif')
        self.buttonList[num].configure(image=photo)
        self.buttonList[num].image = photo
    
    # When the user clicks the "New Game" button... 
    def onNewGameButtonClick(self):
        #If the game was won, get rid of the win label
        if self.matches == .5*self.numberOfCells:
            self.winLabel.destroy()
        self.highScoreResults.set('BEST SCORE: ' + str(self.highScore))
        #Re-shuffle the list for a new game
        self.shuffled = sorted(self.imgList, key=lambda k: random.random())
        #Set clicks and matches back to zero and update the labels
        self.clicks = 0
        self.matches = 0
        self.clickResults.set('Clicks = '+str(self.clicks))
        self.matchResults.set('Matches = '+str(self.matches))
        self.isFirst = True
        #Loop that makes all of the buttons enabled, with their img as blank.gif
        for i in range(0, len(self.imgList)):
            self.buttonList[i].configure(state=NORMAL)
            photo = PhotoImage(file='blank.gif')
            self.buttonList[i].configure(image=photo)
            self.buttonList[i].image = photo
        

    def onQuitButtonClick(self):
        self.destroy()
        

#SECOND CLASS -- Smaller app that lets the user choose how many images they want to play with

class StarterApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.memorygame_app = None #Used to see if there is already an instance of the memory game running
        self.title('Memory Game')
        self.grid()
        self.createWidgets()
    
    def createWidgets(self):
        #Create and grid the 3 different buttons
        fourButton = Button(self, text='Play with FOUR image pairs', command=self.onFourButtonClick)
        sixButton = Button(self, text='Play with SIX image pairs', command=self.onSixButtonClick)
        eightButton = Button(self, text='Play with EIGHT image pairs', command=self.onEightButtonClick)
        fourButton.grid(row=0, sticky=N+E+W+S)
        sixButton.grid(row=1, sticky=N+E+W+S)
        eightButton.grid(row=2, sticky=N+E+W+S)
    
        #When the "four images" button is clicked...    
    def onFourButtonClick(self):
        if self.memorygame_app!=None: self.memorygame_app.destroy() #if there is already a memory game running, destroy it
        self.memorygame_app = MemoryGame(8) #Create the Memory Game with 8 cells
        self.memorygame_app.mainloop()
        
        #When the "six images" button is clicked...
    def onSixButtonClick(self):
        if self.memorygame_app!=None: self.memorygame_app.destroy() #if there is already a memory game running, destroy it
        self.memorygame_app = MemoryGame(12) #Create the Memory Game with 12 cells
        self.memorygame_app.mainloop()
        
        #When the "eight images" button is clicked...
    def onEightButtonClick(self):
        if self.memorygame_app!=None: self.memorygame_app.destroy() #if there is already a memory game running, destroy it
        self.memorygame_app = MemoryGame(16) #Create the Memory Game with 16 cells
        self.memorygame_app.mainloop()
        

class HighScores(): 
    def __init__(self, numOfImages, numOfClicks): 
        self.writeFile(numOfImages, numOfClicks)
        
    def writeFile(self, numOfImages, numOfClicks): 
        #if a high score file already exists for the given difficulty...
        if os.path.exists(str(numOfImages)+'ImgHighScore.txt'): 
            #open the file and read it, saving the value as prevHighScore
            highScoreFile = open(str(numOfImages)+'ImgHighScore.txt')
            prevHighScore = highScoreFile.read()
            prevHighScore = int(prevHighScore) #must convert to integer
            highScoreFile.close()
            #if the numOfClicks for the game is better than the prevHighScore, update the file
            if numOfClicks < prevHighScore: 
                highScoreFile = open(str(numOfImages)+'ImgHighScore.txt','w')
                highScoreFile.write(str(numOfClicks))
                highScoreFile.close()
        #if the file does not already exist, make a new one with numOfClicks as the high score to beat    
        else: 
            highScoreFile = open(str(numOfImages)+'ImgHighScore.txt','w')
            highScoreFile.write(str(numOfClicks))
            highScoreFile.close()

app = StarterApp()
app.mainloop()     