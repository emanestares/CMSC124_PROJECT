# Authors: 
# an interpreter for LOLCODE using python
# GUI created using CustomTkinter

#--- packages and modules to be used ---#
# - tkinter filedialog for choosing a file
# - ctktable for tokens and symbol table
# - customtkinter for GUI
# - lexical analyzer for ... lexical analyzing
from tkinter import filedialog
from CTkTable import *
import customtkinter as tk
import lexicalAnalyzer as la

#--- initializing global variables ---#
fileDirectory = ""
lexemesList = [["Lexemes", "Classification"]]
existingLexemesDict = {}

#--- chooseFile [select button] ---#
# - opens filedialog; open file from directory
# - tokenize each lexemes
# - appends the file to the text editor
# - classifies each lexeme; display to the lexeme table
def chooseFile():
    tempList = []
    stringTemp = ""
    codeString = ""
    tempLine = ""
    stringFlag = False
    fileDirectory = filedialog.askopenfilename()

    if fileDirectory == "":
        return 0
    
    if fileDirectory.split(".")[1] != "lol":
        fileDirLabel.configure(text="Selected file is not a LOL CODE.")
        return 0

    inputFile = open(fileDirectory, "r")

    fileDirLabel.configure(text=fileDirectory.split("/")[-1])

    for line in inputFile:
        codeString+=line
        tempLine = line[:-1]

        while tempLine.find(" ") == 0 and tempLine.find(" ") != -1:
            tempLine = tempLine[1:-1]

        tempList += line[:-1].split(" ")

    for token in tempList:
        if token not in la.allKeywords.keys():
            if token == "":
                stringTemp += " "
                continue

            if token[0] == "\"":
                stringTemp += token
                stringTemp += " "
                stringFlag = True
            elif stringFlag == True:
                if token[-1] == "\"":
                    stringTemp += token
                    stringTemp += " "
                    existingLexemesDict[stringTemp] = "String Literal"
                    stringFlag = False
                    stringTemp = ""
                else:
                    stringTemp += token
            else:
                existingLexemesDict[token] = "Variable Identifier"
        else:
            existingLexemesDict[token] = la.allKeywords[token]

    for token in existingLexemesDict:
        lexemesList.append([token, existingLexemesDict[token]])

    textEditor.insert("0.0", codeString)

    print(existingLexemesDict)

    for widget in lexemesFrame.winfo_children():
        widget.destroy()

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)

    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = lexemesList)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

#--- initializing customtkinter ---#
root = tk.CTk()
root.title("LOL Code Interpreter")
# root.iconbitmap("./wine.ico")



#--- Setting up GUI ---#
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

#--- title label ---#
titleLabel = tk.CTkLabel(root, text="LOLCODE INTERPRETER", text_color = "white", font = ("Helvetica", 35))
titleLabel.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

#--- fdivision frames ---#
fileExpFrame = tk.CTkFrame(root, height=300, width=300)
fileExpFrame.grid(row = 1, column = 0, padx = 2.5, pady = 2)

lexemesFrame = tk.CTkScrollableFrame(root, height=300, width=300)
lexemesFrame.grid(row = 1, column = 1, padx = 2.5, pady = 2)

symbolTableFrame = tk.CTkScrollableFrame(root, height=300, width=300)
symbolTableFrame.grid(row = 1, column = 2, padx = 2.5, pady = 2)

terminalFrame = tk.CTkFrame(root, height=200, width=950)
terminalFrame.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 2)

#--- file explorer ---#
fileDirLabel = tk.CTkLabel(fileExpFrame,text= "No File Selected")
fileDirLabel.grid(row = 0, column = 0, padx=5, pady=2)

selectFileButton = tk.CTkButton(fileExpFrame, text = "SELECT FILE", command=chooseFile)
selectFileButton.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "e")

textEditor = tk.CTkTextbox(fileExpFrame, width = 280, height=265)
textEditor.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#--- List of tokens ---#
lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
lexemesLabel.pack(expand=True, fill="both", padx=5)

lexemesTable = CTkTable(lexemesFrame, row = 1, column = 0, values = [["Lexemes", "Classification"]])
lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

#--- Symbol Table ---#
symbolLabel = tk.CTkLabel(symbolTableFrame,text= "Symbol Table")
symbolLabel.pack(expand=True, fill="both", padx=5)

lexemesTable = CTkTable(symbolTableFrame, row = 1, column = 0, values = [["Identifier", "Value"]])
lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

#--- Execute/Rub Button and Console ---#
executeButton = tk.CTkButton(terminalFrame, text = "EXECUTE")
executeButton.pack(expand=True, fill="both", padx=5, pady=5)

terminal = tk.CTkTextbox(terminalFrame, width = 950, height=265, state = "disabled")
terminal.pack(expand=True, fill="both", padx=5, pady=5)
root.mainloop()