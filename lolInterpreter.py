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
def chooseFile(fileDirLabel, textEditor, lexemesFrame):
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

    print(f"Templist: {tempList}\n")

    # variable that stores the current string for strings with two or more values
    # this will be empty if placed in dictionary, else not empty
    stack_string_variable = ""

    # variable that stores the current iterator
    current_iterator = la.iterator
    for token in tempList:


        # if token not in keywords
        if token not in la.allKeywords.keys() or current_iterator != la.iterator:

            # # clean out the stack string variable and continue
            # stack_string_variable = ""

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

                # update the stack variable for string
                stack_string_variable = stack_string_variable + f"{token}" if stack_string_variable == "" else stack_string_variable + f" {token}" 
                

                # check if item is in the iterator
                if token in current_iterator:

                    # acquire the next value from iterator
                    key_value = current_iterator[token]

                    # if there's no more afterwards
                    if key_value == "done":

                        # update using the stack_string_variable
                        existingLexemesDict[stack_string_variable] = la.allKeywords[stack_string_variable]

                        # also update the current_iterator back
                        current_iterator = la.iterator

                        # clear the current string
                        stack_string_variable = ""

                    # if there's more afterwards
                    else: 

                        # update the current iterator to the next dictionary
                        current_iterator = key_value

                # if it is not in the iterator
                else:
                    stack_string_variable = ""
                    existingLexemesDict[token] = "Variable Identifier"

        # if token is in the lexemes dictionary
        else:

            existingLexemesDict[token] = la.allKeywords[token]

    for token in existingLexemesDict:
        lexemesList.append([token, existingLexemesDict[token]])

    textEditor.insert("0.0", codeString)

    # print properly
    print(f"Acquired Lexemes:\n")
    for eachKey, eachValue in existingLexemesDict.items():
        print(f"'{eachKey}': '{eachValue}'")
    print("")
    
    for widget in lexemesFrame.winfo_children():
        widget.destroy()

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)

    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = lexemesList)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

# draw the main window
def draw():
    # '''Function that draws the main window.'''

    # access the global variables
    global fileDirectory, lexemesList, existingLexemesDict 

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
    selectFileButton = tk.CTkButton(fileExpFrame, text = "SELECT FILE", command=lambda: chooseFile(fileDirLabel, textEditor, lexemesFrame))
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


# main function
def main():

    # draw the actual window
    draw()


# start the main program
if __name__ == "__main__":
    main()