# Authors: 
    # Member 1: Frederick Emmanuel S. Estares 
    # Member 2: John Yves A. Baltazar 
    # Member 3: Andi Lynson O. Torres

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
import re

# define static variables
INITIAL_LEXEMES_LIST = [["Lexemes", "Classification"]]

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
    stringFlag = False
    btwFlag = False
    obtwFlag = False
    fileDirectory = filedialog.askopenfilename()

    # reset existing lexemes dictionary
    global existingLexemesDict, lexemesList
    existingLexemesDict = {}
    lexemesList = INITIAL_LEXEMES_LIST

    # early exit if no file directory selected
    if fileDirectory == "":
        return 0
    
    # early exit if chosen file's extension is not lol
    if fileDirectory.split(".")[1] != "lol":
        fileDirLabel.configure(text="Selected file is not a LOL CODE.")
        return 0

    # open file
    inputFile = open(fileDirectory, "r")

    # get directory of file
    fileDirLabel.configure(text=fileDirectory.split("/")[-1])

    # iterate through file
    for line in inputFile:
        codeString += line                  # store all lines in codeString        
        tempList += line[:-1].split(" ")    # split on spaces then add each to the tempList
        tempList += "\n"

    # display tempList
    print(f"Templist: {tempList}\n")

    # variable that stores the current string for strings with two or more values
    # this will be empty if placed in dictionary, else not empty
    # [!] used for keywords with multiple tokens
    stack_string_variable = ""

    # variable that stores the current iterator
    current_iterator = la.iterator
    
    # iterate through each token in the tempList
    for token in tempList:
        
        # if BTW is encountered, ignore tokens until the end of the line
        if token == "BTW": btwFlag = True
        elif btwFlag == True:
            if token == "\n":       btwFlag = False
            else:                   continue

        # if OBTW is encounted, ignore tokens until TLDR has been reached
        if token == "OBTW": obtwFlag = True
        elif obtwFlag == True:
            if token == "TLDR":     obtwFlag = False
            else:                   continue

        # ignore new lines 
        if token == "\n": continue

        # if token not in keywords
        if token not in la.allKeywords.keys() or current_iterator != la.iterator:
            if re.search("[0-9]\.[0-9]", token) != None:
                existingLexemesDict[token] = "Float Literal"
                continue
            if re.search("^[0-9]+$", token) != None:
                existingLexemesDict[token] = "Integer Literal"
                continue

            # if token is "", add a space then continue iterating
            if token == "":
                stringTemp += " "
                continue            

            # if the first character of the token is '\"', then it is part of a string literal 
            if token[0] == "\"":
                stringTemp += token     # append the token
                stringTemp += " "       # add a space
                stringFlag = True       # next token will be part of the string
            # if the previous token is an unpaired '\"'
            elif stringFlag == True:
                # if the last part of the token is '\"', then it closes the string literal
                if token[-1] == "\"":
                    stringTemp += token # append the token
                    stringTemp += " "   # add a space
                    stringTemp = re.search(r'"([^"]*)"', stringTemp).group(1)   # clean the string
                    existingLexemesDict[f'"{stringTemp}"'] = "String Literal"   # mark it as a string literal
                    stringFlag = False  # next token is no longer part of the string
                    stringTemp = ""     # reset
                # the string is still unclosed, add it to stringTemp
                else:
                    stringTemp += token # append the token
            # not a string literal
            else:
                # update the stack variable for string
                stack_string_variable = stack_string_variable + f"{token}" if stack_string_variable == "" else stack_string_variable + f" {token}" 
                
                # check if item is in the iterator
                if token in current_iterator:
                    key_value = current_iterator[token] # acquire the next value from iterator

                    # if there's no more afterwards
                    if key_value == "done":
                        existingLexemesDict[stack_string_variable] = la.allKeywords[stack_string_variable]  # update using the stack_string_variable
                        current_iterator = la.iterator                                                      # also update the current_iterator back
                        stack_string_variable = ""                                                          # clear the current string
                    # if there's more afterwards
                    else: 
                        current_iterator = key_value # update the current iterator to the next dictionary
                # if it is not in the iterator
                else:
                    stack_string_variable = ""                          # reset
                    existingLexemesDict[token] = "Variable Identifier"  # treat as variable identifier
        
        # if token is in the lexemes dictionary
        else:
            existingLexemesDict[token] = la.allKeywords[token]

    # reset the lexemesList
    lexemesList = [["Lexemes", "Classification"]]

    # append all tokens and their classifications to the lexemesList
    for token in existingLexemesDict: lexemesList.append([token, existingLexemesDict[token]])

    # reset the text field
    textEditor.delete('1.0', tk.END)

    # display code in the text field
    textEditor.insert("0.0", codeString)

    # print properly
    print(f"Acquired Lexemes:\n")
    for eachKey, eachValue in existingLexemesDict.items(): print(f"'{eachKey}': '{eachValue}'")
    print("")
    
    for widget in lexemesFrame.winfo_children(): widget.destroy()

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)
    print(f"Third: {lexemesList}\n")
    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = lexemesList)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

# draw the main window
def draw():
    '''Function that draws the main window.'''

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
    draw() # draw the actual window


# start the main program
if __name__ == "__main__":
    main()