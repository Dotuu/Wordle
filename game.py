import tkinter
from customtkinter import *
import random

#stop user from entering guess after correct word is guessed
#allow for clicking enter to input guess and if the game is over start a new one
#make arrow keys etc change position for input
#check that input is a word

class main:
    def __init__(self):
        # setup main window
        self.root = CTk(fg_color="#1f1f1f")
        self.root.geometry("340x523")
        self.root._set_appearance_mode("dark")
        self.root.title("Not Wordle")
        self.labels = []
        self.frames = []
        self.root.resizable(False, False)
        self.root.bind("<KeyPress>", self.onKeyPress)
        self.wordsPath = "words.txt"
        self.row = 0
        self.gameRunning = True

        # set up head frame
        self.headFrame = CTkFrame(self.root, height=50, width=420, fg_color="#1f1f1f")
        self.headFrame.grid(row=0, column=0, sticky="nsew", pady=(5, 5))
        self.headFrame.columnconfigure(0, weight=1)
        self.headFrame.rowconfigure(0, weight=1)
        self.label = CTkLabel(self.headFrame, text="Not Wordle!", font=("sans", 52), text_color="#d9d4d4", anchor="center")
        self.label.grid(row=0, column=0, sticky="nsew")

        # make 5 rows with 5 evenly spaced frames per row
        for row in range(1, 6):  # 5 rows for guesses
            self.createGuessRow(row)

        #generate our random word
        self.word = self.getRandomWord()
        print(self.word)

        # set up footer frame
        self.footFrame = CTkFrame(self.root, height=60, width=420, fg_color="#1f1f1f")
        self.footFrame.grid(row=6, column=0, sticky="nsew", pady=(5, 5))
        self.footFrame.columnconfigure(tuple(range(5)), weight=1, uniform="guess")

        self.entry1 = CTkEntry(self.footFrame, height=60, width=60, fg_color="#333232", font=("sans", 42), justify="center", corner_radius=0, border_width=0, placeholder_text="G")
        self.entry1.grid(row=0, column=0, padx=(4, 4), pady=(4, 4))

        self.entry2 = CTkEntry(self.footFrame, height=60, width=60, fg_color="#333232", font=("sans", 42), justify="center", corner_radius=0, border_width=0, placeholder_text="U")
        self.entry2.grid(row=0, column=1, padx=(4, 4), pady=(4, 4))

        self.entry3 = CTkEntry(self.footFrame, height=60, width=60, fg_color="#333232", font=("sans", 42), justify="center", corner_radius=0, border_width=0, placeholder_text="E")
        self.entry3.grid(row=0, column=2, padx=(4, 4), pady=(4, 4))

        self.entry4 = CTkEntry(self.footFrame, height=60, width=60, fg_color="#333232", font=("sans", 42), justify="center", corner_radius=0, border_width=0, placeholder_text="S")
        self.entry4.grid(row=0, column=3, padx=(4, 4), pady=(4, 4))

        self.entry5 = CTkEntry(self.footFrame, height=60, width=60, fg_color="#333232", font=("sans", 42), justify="center", corner_radius=0, border_width=0, placeholder_text="S")
        self.entry5.grid(row=0, column=4, padx=(4, 4), pady=(4, 4))

        #bind the entrybox to the keyrelease event and run onKeyPress function
        self.entry1.bind("<KeyPress>", self.onKeyPress)
        self.entry2.bind("<KeyPress>", self.onKeyPress)
        self.entry3.bind("<KeyPress>", self.onKeyPress)
        self.entry4.bind("<KeyPress>", self.onKeyPress)
        self.entry5.bind("<KeyPress>", self.onKeyPress)

        #validate each entry on key press to check if they exceed character length of 1
        self.validate_input = self.root.register(self.checkMaxLength)
        self.entry1.configure(validate="key", validatecommand=(self.validate_input, "%P"))
        self.entry2.configure(validate="key", validatecommand=(self.validate_input, "%P"))
        self.entry3.configure(validate="key", validatecommand=(self.validate_input, "%P"))
        self.entry4.configure(validate="key", validatecommand=(self.validate_input, "%P"))
        self.entry5.configure(validate="key", validatecommand=(self.validate_input, "%P"))

        #run main game loop and active the exit logic
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root.mainloop()

    def createGuessRow(self, row):
        # create frame to hold guess row
        guessRow = CTkFrame(self.root, fg_color="transparent")
        guessRow.grid(row=row, column=0, sticky="nsew", pady=(4, 4))

        # make 5 evenly spaced columns for the row
        guessRow.columnconfigure(tuple(range(5)), weight=1, uniform="guess")

        row_labels = []
        row_frames = []

        # add 5 frames in the row
        for col in range(5):
            frame = CTkFrame(guessRow, height=60, width=60, fg_color="#333232", corner_radius=20)
            frame.grid(row=0, column=col, padx=(4, 4), pady=(4, 4))

            label = CTkLabel(frame, width=60, height=60, text="", font=("sans", 42), text_color="#d9d4d4")
            label.grid(row=0, column=col)

            row_labels.append(label)
            row_frames.append(frame)

        self.frames.append(row_frames)
        self.labels.append(row_labels)

        # self.labels[0][2].configure(text="A")
        # self.frames[0][2].configure(fg_color="blue")

    #keypress event for key to shift entry over to the next letter
    def onKeyPress(self, event):
        if event.keysym.isalpha():
            event.widget.tk_focusNext().focus_set()
            if self.guessComplete():
                if self.gameRunning:
                    self.guess(self.word, self.getGuess())

    def getGuess(self):
        list = []
        list.append(self.entry1.get())
        list.append(self.entry2.get())
        list.append(self.entry3.get())
        list.append(self.entry4.get())
        list.append(self.entry5.get())
        return list

    def guess(self, word, guess):
        returnList = ["","","","",""]
        wordList = list(word)
        guessList = list(guess)
        wordDict = {}
        
        for letter in wordList:
            if letter not in wordDict:
                wordDict[letter] = 1
            else:
                value = wordDict.get(letter)
                wordDict[letter] = value + 1

        for guessIndex in range(len(guessList)):
            guessLetter = guessList[guessIndex]
            #check exact match
            if wordList[guessIndex] == guessLetter:
                value = wordDict.get(guessLetter)
                if value != 0:
                    wordDict[guessLetter] = value - 1
                    returnList[guessIndex] = "g"

        #second pass for "y"
        for guessIndex in range(len(guessList)):
            guessLetter = guessList[guessIndex]
            if returnList[guessIndex] != "g":
                if guessLetter in wordDict and wordDict[guessLetter] > 0:
                    wordDict[guessLetter] -= 1
                    returnList[guessIndex] = "y"
        self.displayGuessResults(returnList, guessList)

    def displayGuessResults(self, displayValues, guessList):
        for index, value in enumerate(displayValues):
            if value == "y":
                self.labels[self.row][index].configure(text=guessList[index].upper())
                self.frames[self.row][index].configure(fg_color="yellow")
            elif value == "g":
                self.labels[self.row][index].configure(text=guessList[index].upper())
                self.frames[self.row][index].configure(fg_color="green")
            else:
                self.labels[self.row][index].configure(text=guessList[index].upper())
                self.frames[self.row][index].configure(fg_color="#333232")
        #clear our entries
        self.entry1.delete(0, tkinter.END)
        self.entry2.delete(0, tkinter.END)
        self.entry3.delete(0, tkinter.END)
        self.entry4.delete(0, tkinter.END)
        self.entry5.delete(0, tkinter.END)

        if (self.row == 4):
            self.endGame()
        else:
            self.row += 1

    def getRandomWord(self):
        with open(self.wordsPath, "r") as file:
            words = file.readlines()
        
        word = random.choice(words).strip().lower()
        return word
    

    #function to check if the limit of 1 has been reached for each entry
    def checkMaxLength(self, limit):
        if len(limit) > 1:
            return False
        return True

    #function to check if the entries have all been filled out and a guess can be done 
    def guessComplete(self):
        if (self.entry1.get() != "" and self.entry2.get() != "" and self.entry3.get() != "" and self.entry4.get() != "" and self.entry5.get() != ""):
            return True

    def endGame(self):
        wordList = list(self.word)
        print(wordList)
        self.entry1.insert(0, str(wordList[0]))
        self.entry2.insert(0, str(wordList[1]))
        self.entry3.insert(0, str(wordList[2]))
        self.entry4.insert(0, str(wordList[3]))
        self.entry5.insert(0, str(wordList[4]))
        self.entry1.configure(state="disabled")
        self.entry2.configure(state="disabled")
        self.entry3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        self.entry5.configure(state="disabled")
        self.gameRunning = False

    #run when program exits
    def onClose(self):
        self.root.destroy()

if __name__ == "__main__":
    game = main()