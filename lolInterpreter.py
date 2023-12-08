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
import syntacticalAnalyzer as grammar
import re

# define static variables
INITIAL_LEXEMES_LIST = [["Lexemes", "Classification"]]

#--- initializing global variables ---#
fileDirectory = ""
lexemesList = [["Lexemes", "Classification"]]

# contains all current dictionary descriptions
existingLexemesDict = {}

# contains all usable tokens including REPETITIONS
existingLexemesList = []

SKIPPING_KEYWORDS = [
    "HAI", "KTHXBYE"
]

# displays the error inside the terminal
def displayOnTerminal(errorMessage):
    terminal.configure(state = "normal", text_color = "pink")
    terminal.insert("0.0", errorMessage)
    terminal.configure(state = "disabled")

# Function that checks if string can be converted to float
def is_float_convertible(number):
        try:
            float(number)
            return True
        except ValueError:
            return False

# Function that checks if string can be converted to integer
def is_int_convertible(number):
        try:
            int(number)
            return True
        except ValueError:
            return False

# Function that converts a given stringed number to its raw numerical value
def get_stringed_number_value(number):
    return float(number) if is_float_convertible(number) else int(number) if is_int_convertible(number) else "<uninitialized>"            

# Function that executes syntax analysis
def syntaxAnalysis(lexemesList):
    global terminal
    variableNames = []

    # checks for start of code keyword, prompts user if none found
    if lexemesList[1][0] != "HAI":
        print("wow")
        displayOnTerminal("Syntax Error: Start of code not found.\n")

    # checks for end of code keyword, prompts user if none found
    if lexemesList[-1][0] != "KTHXBYE":
        displayOnTerminal("Syntax Error: End of code not found.\n")
    
    count = 0
    for i in lexemesList:
        # checks for a variable name after I HAS A
        if i[0] == "I HAS A":
            if lexemesList[count+1][0] in la.allKeywords.keys() or lexemesList[count+1][0] in la.arithmetic_operations or not lexemesList[count+1][0][0].isalpha():
                displayOnTerminal("Syntax Error: Expecting variable name.\n")
            else:
                variableNames.append(lexemesList[count+1][0])
        
        # checks if comparison operation has two arithmetic literals (int, float)
        if i[0] in la.arithmetic_operations:
            if lexemesList[count+1][1] not in ["Integer Literal", "Float Literal"] or lexemesList[count+3][1] not in ["Integer Literal", "Float Literal"]:
                displayOnTerminal("Syntax Error: Expecting integer or float literals.\n")

        # checks if a variable is declared before being referenced
        if i[1] == "Variable Identifier" and lexemesList[count-1][0] != "I HAS A":
            if i[0] not in variableNames:
                displayOnTerminal("Syntax Error: Variable referenced before definition: " + i[0] + ".\n")
        count += 1


def symbolTableAnalyzer(lexemesList):
    '''Function that executes syntax analysis given the list of lexemes.
    This function returns a list of identifiers and their values.'''

    # return value
    ret_list = [["Identifier", "Value"]]

    # variables
    lexeme_skip_counter = 0
    current_lexeme_index = -1

    # do for every lexeme
    for each_item in lexemesList:
        # update iterating variable
        current_lexeme_index += 1

        # this is the identifier 
        identifier = each_item[0]

        # skip until lexeme skip counter is not 0
        if lexeme_skip_counter != 0:
            print(f"Skipping '{identifier}'")
            lexeme_skip_counter -= 1
            continue

        # just print out cuz why not
        print(f"'{identifier}'".ljust(25) + f": {each_item[1]}")
    
        # skip HAI and BYE
        if identifier in ["HAI", "KTHXBYE"]: continue

        # CASE OF: variable equalization
        if identifier == "I HAS A":
            # variable name is next item, also its value is current index + 3
            ret_list.append([lexemesList[current_lexeme_index+1][0], f"{get_stringed_number_value(lexemesList[current_lexeme_index+3][0])}"])

            # should skip 3 more items after this iteration
            lexeme_skip_counter = 3

        # CASE OF: arithmetic operations
        if identifier in la.arithmetic_operations:
            # variables here
            first_number = get_stringed_number_value(lexemesList[current_lexeme_index+1][0])
            second_number = get_stringed_number_value(lexemesList[current_lexeme_index+3][0])

            # label to put in table
            arithmetic_label = f"{lexemesList[current_lexeme_index][0]} "
            arithmetic_label += f"{lexemesList[current_lexeme_index+1][0]} "
            arithmetic_label += f"{lexemesList[current_lexeme_index+2][0]} "
            arithmetic_label += f"{lexemesList[current_lexeme_index+3][0]}"

            # addition
            if identifier == "SUM OF":
                ret_list.append([arithmetic_label, f"{first_number+second_number}"])

            # modulo
            elif identifier == "MOD OF":
                ret_list.append([arithmetic_label, f"{first_number%second_number}"])

            # division
            elif identifier == "QUOSHUNT OF":
                ret_list.append([arithmetic_label, f"{first_number/second_number}"])

            # minimum
            elif identifier == "SMALLR OF":
                ret_list.append([arithmetic_label, f"{first_number if first_number<=second_number else second_number }"])

            # maximum
            elif identifier == "BIGGR OF":
                ret_list.append([arithmetic_label, f"{first_number if first_number>=second_number else second_number }"])

            # subtraction
            elif identifier == "DIFF OF":
                ret_list.append([arithmetic_label, f"{first_number-second_number}"])

            # multiplication
            elif identifier == "PRODUKT OF":
                ret_list.append([arithmetic_label, f"{first_number*second_number}"])

    print(f"Results: {ret_list}")
    return ret_list



#--- chooseFile [select button] ---#
# - opens filedialog; open file from directory
# - tokenize each lexemes
# - appends the file to the text editor
# - classifies each lexeme; display to the lexeme table
def chooseFile(fileDirLabel, textEditor, lexemesFrame, symbolTableFrame):
    tempList = []
    stringTemp = ""
    codeString = ""
    stringFlag = False
    btwFlag = False
    obtwFlag = False
    fileDirectory = filedialog.askopenfilename()

    # reset existing lexemes dictionary
    global existingLexemesDict, lexemesList, terminal
    existingLexemesDict = {}
    existingLexemesList = []
    lexemesList = INITIAL_LEXEMES_LIST

    terminal.configure(state = "normal")
    terminal.delete('1.0', tk.END)
    terminal.configure(state = "disabled")

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

        if tempList != []:
            tempList += "\n"

        tempList += line.strip().split(" ")    # split on spaces then add each to the tempList

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
        
        # TODO: tokens after BTW or OBTW still need to show in the lexical analysis
        if token == "\n":
            existingLexemesDict[token] = "Line Break"
            existingLexemesList.append([token, "Line Break"])

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

        if token == "AN":
            print(f"Got AN lol")

        # if token not in keywords
        if token not in la.allKeywords.keys() or current_iterator != la.iterator:
            if re.search("[0-9]\.[0-9]", token) != None:
                existingLexemesDict[token] = "Float Literal"
                existingLexemesList.append([token, "Float Literal"])
                continue
            if re.search("^[0-9]+$", token) != None:
                existingLexemesDict[token] = "Integer Literal"
                existingLexemesList.append([token, "Integer Literal"])
                continue

            # if token is "", add a space then continue iterating
            if token == "":
                stringTemp += " "
                continue            
            
            # TODO: string delimiters show up as seperate entites in the lexemes table;
            # TODO: that is, "-string delimiter, <text>-string literal, "-string delimiter

            # if the first character of the token is '\"', then it is part of a string literal 
            if token[0] == "\"" and not stringFlag:
                existingLexemesDict["\""] = "String Delimeter"   # mark it as a string literal
                existingLexemesList.append(["\"", "String Delimeter"])
                stringTemp += token     # append the token
                stringTemp += " "       # add a space
                stringFlag = True       # next token will be part of the string
            # if the previous token is an unpaired '\"'
            elif stringFlag == True:
                # if the last part of the token is '\"', then it closes the string literal
                if token[-1] == "\"":
                    stringTemp += token # append the token
                    stringTemp += " "   # add a space
                    stringTemp = re.search(r'"([^"]*)"', stringTemp).group(1)   # clean the 

                    existingLexemesDict[f"{stringTemp}"] = "String Literal"   # mark it as a string literal
                    existingLexemesList.append([f"{stringTemp}", "String Literal"])

                    existingLexemesDict["\""] = "String Delimeter"   # mark it as a string literal
                    existingLexemesList.append(["\"", "String Delimeter"])

                    stringFlag = False  # next token is no longer part of the string
                    stringTemp = ""     # reset
                # the string is still unclosed, add it to stringTemp
                else:
                    stringTemp += token # append the token
                    print(stringTemp)
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
                        existingLexemesList.append([stack_string_variable, la.allKeywords[stack_string_variable]])
                        current_iterator = la.iterator                                                      # also update the current_iterator back
                        stack_string_variable = ""                                                          # clear the current string
                    # if there's more afterwards
                    else: 
                        current_iterator = key_value # update the current iterator to the next dictionary
                # if it is not in the iterator
                else:
                    stack_string_variable = ""                          # reset
                    existingLexemesDict[token] = "Variable Identifier"  # treat as variable identifier
                    existingLexemesList.append([token, "Variable Identifier"])
        # if token is in the lexemes dictionary
        else:
            if token == "AN": print(f"OKAY I GOT AN")
            stack_string_variable = "" 
            existingLexemesDict[token] = la.allKeywords[token]
            existingLexemesList.append([token, la.allKeywords[token]])
        


    # reset the lexemesList
    lexemesList = [["Lexemes", "Classification"]]

    # append all tokens and their classifications to the lexemesList
    # for token in existingLexemesDict: lexemesList.append([token, existingLexemesDict[token]])
    for token in existingLexemesList: lexemesList.append([token[0], existingLexemesDict[token[0]]])
    
    # reset the text field
    textEditor.delete('1.0', tk.END)

    # display code in the text field
    textEditor.insert("0.0", codeString)
    
    for widget in lexemesFrame.winfo_children(): widget.destroy()

    # TODO: I think dapat lahat ng lexemes ipriprint in order, hindi mga unique occurences lang

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)
    print(f"Lexemes List: {lexemesList}\n")
    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = lexemesList)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

    # execute analysis on the lexemes
    returnStatus = syntaxAnalysis(lexemesList)
    grammar.analyze(existingLexemesList)
    symbol_table_results = symbolTableAnalyzer(lexemesList)

    for widget in symbolTableFrame.winfo_children(): widget.destroy()

    symbolLabel = tk.CTkLabel(symbolTableFrame,text= "Symbol Table")
    symbolLabel.pack(expand=True, fill="both", padx=5)
    symbolTable = CTkTable(symbolTableFrame, row = len(symbol_table_results), column = 2, values = symbol_table_results)
    symbolTable.pack(expand=True, fill="both", padx=5, pady=5)


# draw the main window
def draw():
    '''Function that draws the main window.'''

    # access the global variables
    global fileDirectory, lexemesList, existingLexemesDict, terminal

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
    selectFileButton = tk.CTkButton(fileExpFrame, text = "SELECT FILE", command=lambda: chooseFile(fileDirLabel, textEditor, lexemesFrame, symbolTableFrame))
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

    symbolTable = CTkTable(symbolTableFrame, row = 1, column = 0, values = [["Identifier", "Value"]])
    symbolTable.pack(expand=True, fill="both", padx=5, pady=5)

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