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

# TODO: finalize this; test
import syntacticalAnalyzerTest as parser

# define static variables
INITIAL_LEXEMES_LIST = [["Lexemes", "Classification"]]

#--- initializing global variables ---#
fileDirectory = ""
lexemesList = [["Lexemes", "Classification"]]

# contains all current dictionary descriptions
existingLexemesDict = {}

# contains all usable tokens including REPETITIONS
existingLexemesList = []

# contains the variable names
variable_names = []

SKIPPING_KEYWORDS = [
    "HAI", "KTHXBYE"
]

# variable that stores how many new lines have passed since the lexemes dictionary
existingLexemesDict_newline_reference = []

# displays the error inside the terminal
def displayOnTerminal(errorMessage):
    '''Function that displays a particular string at the terminal part of the GUI.'''

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
    global terminal, existingLexemesDict_newline_reference, variable_names

    # variable that stores the syntax errors list, for better printing
    syntax_error_list = []

    # checks for start of code keyword, prompts user if none found
    if lexemesList[1][0] != "HAI":
        # TODO: for testing; should be removed
        # print("wow")

        syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[0]}]: Start of code not found.\n")

    print(f"{len(lexemesList)} vs {len(existingLexemesDict_newline_reference)}")

    # go through the other items
    count = -1
    variables_initialized, initializing, should_skip = False, False, False
    current_new_line = 2

    for i in lexemesList[2:-1]:

        count += 1    

        # if variables are not yet initialized
        if not variables_initialized:

            # start of variable initialization
            if i[0] == "WAZZUP":
                initializing = True
                current_new_line += 1
                continue

            # end the variable initialization
            if i[0] == "BUHBYE":
                variables_initialized = True
                current_new_line += 1
                continue

            # variable initialization starts here
            if initializing:    

                print(f"'{i[0]}'  nl: {current_new_line};  ref: {existingLexemesDict_newline_reference[count]}")

                # check for variable name after I HAS A
                if i[0] == "I HAS A":
                    current_new_line += 1

                    # if improper I HAS A
                    print(f"lexemesList[{count+1+1}][{0}] = {lexemesList[count+1+1][0]}")
                    if lexemesList[count+2+1][0] in la.allKeywords.keys() or lexemesList[count+2+1][0] in la.arithmetic_operations:
                       syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[count+1]}]: Expecting variable name.\n")
                       continue
                    
                    # if proper, add to variable names
                    else:
                        syntax_error_list.insert(0, f"Syntax Correct [line {existingLexemesDict_newline_reference[count+1]}]. Added '{lexemesList[count+3][0]}' variable.\n")
                        variable_names.append(lexemesList[count+3][0])
                        continue


                # always go to next line properly
                elif current_new_line == existingLexemesDict_newline_reference[count]:
                    continue

                # if no "I HAS A", skip to next new line
                else:
                    current_new_line += 1
                    print(f"token {i[0]} current_new_line that is {current_new_line} == {existingLexemesDict_newline_reference[count]}")
                    syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[count+1]}]: Expecting variable declaration or 'BUHBYE' here.\n")

                                
                # should continue search til "BUHBYE"
                continue

            # if nothing happened, proceed next


        # checks for a variable name after I HAS A, this is illegal now!

        # TODO: for testing; should be removed
        # print(f"OKAY GOT: '{i}'")

        # checks for a variable name after I HAS A

        if i[0] == "I HAS A":
            syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[count+1]}]: Cannot instantiate variable outside of declarations clause.\n")
            
        
        # checks if comparison operation has two arithmetic literals (int, float)
        if i[0] in la.arithmetic_operations:
            if lexemesList[count+1][1] not in ["Integer Literal", "Float Literal"] or lexemesList[count+3][1] not in ["Integer Literal", "Float Literal"]:
                syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[count]}]: Expecting integer or float literals.\n")

        # checks if a variable is declared before being referenced
        if i[1] == "Variable Identifier" and lexemesList[count-1][0] != "I HAS A":
            if i[0] not in variable_names:
                print(f"Current count is {count}")
                syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[count]}]: Variable referenced before definition: '" + i[0] + "'.\n")
        

    # checks for end of code keyword, prompts user if none found
    print(f"lexemesList[-1][0]: {lexemesList[-1][0]}")
    if lexemesList[-1][0] != "KTHXBYE":
        syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[len(existingLexemesDict_newline_reference)-1]}]: End of code not found.\n")
    
    # print out the syntax errors now
    for each_error in syntax_error_list:
        displayOnTerminal(each_error)

def symbolTableAnalyzer(lexemesList):
    '''Function that executes syntax analysis given the list of lexemes.
    This function returns a list of identifiers and their values.'''

    # return value
    ret_list = [["Identifier", "Value"]]

    # ================= This is to be done for next milestone ================

    # # variables
    # lexeme_skip_counter = 0
    # current_lexeme_index = -1


    # # do for every lexeme
    # for each_item in lexemesList:
    #     # update iterating variable
    #     current_lexeme_index += 1

    #     # this is the identifier 
    #     identifier = each_item[0]

        # skip until lexeme skip counter is not 0
        if lexeme_skip_counter != 0:
            # TODO: for testing; should be removed
            # print(f"Skipping '{identifier}'")

            lexeme_skip_counter -= 1
            continue

        # TODO: for testing; should be removed
        # just print out cuz why not
        # print(f"'{identifier}'".ljust(25) + f": {each_item[1]}")
    
        # skip HAI and BYE
        if identifier in ["HAI", "KTHXBYE"]: continue


    #     # skip until lexeme skip counter is not 0
    #     if lexeme_skip_counter != 0:
    #         print(f"Skipping '{identifier}'")
    #         lexeme_skip_counter -= 1
    #         continue

    #     # just print out cuz why not
    #     print(f"'{identifier}'".ljust(25) + f": {each_item[1]}")
    
    #     # skip HAI and BYE
    #     if identifier in ["HAI", "KTHXBYE"]: continue

    #     # CASE OF: variable equalization
    #     if identifier == "I HAS A":
            
    #         # if failed, listIndexError means syntactical error
    #         try:

    #             # variable name is next item, also its value is current index + 3
    #             ret_list.append([lexemesList[current_lexeme_index+1][0], f"{get_stringed_number_value(lexemesList[current_lexeme_index+3][0])}"])

    #             # should skip 3 more items after this iteration
    #             lexeme_skip_counter = 3

    #         # if failed, listIndexError means syntactical error
    #         except IndexError:
    #             print("Syntactical error was found.")


    #     # CASE OF: arithmetic operations
    #     if identifier in la.arithmetic_operations:

    #         # variables here
    #         first_number = get_stringed_number_value(lexemesList[current_lexeme_index+1][0])
    #         second_number = get_stringed_number_value(lexemesList[current_lexeme_index+3][0])
                
    #         # label to put in table
    #         arithmetic_label = f"{lexemesList[current_lexeme_index][0]} "
    #         arithmetic_label += f"{lexemesList[current_lexeme_index+1][0]} "
    #         arithmetic_label += f"{lexemesList[current_lexeme_index+2][0]} "
    #         arithmetic_label += f"{lexemesList[current_lexeme_index+3][0]}"

    #         match identifier:
    #             case "SUM OF":          # addition
    #                 ret_list.append([arithmetic_label, f"{first_number+second_number}"])
    #             case "MOD OF":          # modulo
    #                 ret_list.append([arithmetic_label, f"{first_number%second_number}"])
    #             case "QUOSHUNT OF":     # division
    #                 ret_list.append([arithmetic_label, f"{first_number/second_number}"])
    #             case "SMALLR OF":       # minimum
    #                 ret_list.append([arithmetic_label, f"{first_number if first_number<=second_number else second_number }"])
    #             case "BIGGR OF":        # maximum
    #                 ret_list.append([arithmetic_label, f"{first_number if first_number>=second_number else second_number }"])
    #             case "DIFF OF":
    #                 ret_list.append([arithmetic_label, f"{first_number-second_number}"])
    #             case "PRODUKT OF":
    #                 ret_list.append([arithmetic_label, f"{first_number*second_number}"])
    #             case _:
    #                 pass            



    print(f"\nResults: {ret_list}")
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
    global existingLexemesDict, lexemesList, terminal, existingLexemesDict_newline_reference
    existingLexemesDict = {}
    existingLexemesList = []
    existingLexemesDict_newline_reference = []
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
    line_count = 0
    for line in inputFile:
        line_count += 1
        codeString += f'{"{:02d}".format(line_count)}   |     ' + line                  # store all lines in codeString  

        if tempList != []:
            tempList += "\n"

        tempList += line.strip().split(" ")    # split on spaces then add each to the tempList

    # TODO: for testing; should be removed
    # display tempList
    # print(f"Templist: {tempList}\n")

    # variable that stores the current string for strings with two or more values
    # this will be empty if placed in dictionary, else not empty
    # [!] used for keywords with multiple tokens
    stack_string_variable = ""

    # variable that stores the current iterator
    current_iterator = la.iterator
    
    # iterate through each token in the tempList
    current_newline_count = 1

    # TODO: for testing; should be removed
    # print("SLDFKJSKLFJKSDJFKLSDJKLFSDJ")
    # print(tempList)
    # print("SLDFKJSKLFJKSDJFKLSDJKLFSDJ")
    
    for token in tempList:
        

        # # ignore new lines
        # print(token) 
        # if token == "\n":
        #     print("YESSSSSSSSSSSED") 
        #     current_newline_count += 1
        #     continue

        # TODO: tokens after BTW or OBTW still need to show in the lexical analysis
        # if token == "\n":
        #     existingLexemesDict[token] = "Line Break"
        #     existingLexemesList.append([token, "Line Break"])


        # if BTW is encountered, ignore tokens until the end of the line
        if token == "BTW": 
            btwFlag = True
            current_newline_count += 1

        # if BTW keyterm
        elif btwFlag == True:
            if token == "\n":       
                btwFlag = False
                current_newline_count += 1
            else:
                existingLexemesDict[token] = "Comment"
                existingLexemesList.append([token, "Comment"])
                existingLexemesDict_newline_reference.append(current_newline_count)
                continue

        # if OBTW is encounted, ignore tokens until TLDR has been reached
        if token == "OBTW": obtwFlag = True
        elif obtwFlag == True:
            if token == "TLDR":     
                obtwFlag = False
            else:
                existingLexemesDict[token] = "Comment"
                existingLexemesList.append([token, "Comment"])          
                existingLexemesDict_newline_reference.append(current_newline_count)         
                continue

        # if token not in keywords
        if token not in la.allKeywords.keys() or current_iterator != la.iterator:
            if re.search("[0-9]\.[0-9]", token) != None:
                existingLexemesDict[token] = "Float Literal"
                existingLexemesList.append([token, "Float Literal"])
                existingLexemesDict_newline_reference.append(current_newline_count)
                continue
            if re.search("^[0-9]+$", token) != None:
                existingLexemesDict[token] = "Integer Literal"
                existingLexemesList.append([token, "Integer Literal"])
                existingLexemesDict_newline_reference.append(current_newline_count)
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
                existingLexemesDict_newline_reference.append(current_newline_count)
                stringTemp += token     # append the token
                stringTemp += " "       # add a space
                stringFlag = True       # next token will be part of the string
            # if the previous token is an unpaired '\"'
            elif stringFlag == True:
                # if the last part of the token is '\"', then it closes the string literal
                if token[-1] == "\"":
                    stringTemp += token # append the token
                    stringTemp += " "   # add a space
                    stringTemp = re.search(r'[^"]*"([^"]*)"[^"]*', stringTemp).group(1)   # clean the 

                    existingLexemesDict[f"{stringTemp}"] = "String Literal"   # mark it as a string literal
                    existingLexemesList.append([f"{stringTemp}", "String Literal"])

                    existingLexemesDict["\""] = "String Delimeter"   # mark it as a string literal
                    existingLexemesList.append(["\"", "String Delimeter"])
                    
                    existingLexemesDict_newline_reference.append(current_newline_count)

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
                        existingLexemesDict_newline_reference.append(current_newline_count)
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
                    existingLexemesDict_newline_reference.append(current_newline_count)
        # if token is in the lexemes dictionary
        else:
            # TODO: for testing; should be removed
            # if token == "AN": print(f"OKAY I GOT AN")

            stack_string_variable = "" 
            existingLexemesDict[token] = la.allKeywords[token]
            existingLexemesList.append([token, la.allKeywords[token]])
            existingLexemesDict_newline_reference.append(current_newline_count)

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

    # TODO: for testing; should be removed
    # print(f"Lexemes List: {lexemesList}\n")
    
    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = lexemesList)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

    # TODO: for testing; should be removed
    # print("Lexemes: \n")
    # [print(x) for x in lexemesList]

    # TODO: for testing; should be removed
    print("[!] DO TRAVERSAL")
    new_parser = parser.Parser(lexemesList[1:])
    new_parser.traverse_tokens()

    # execute analysis on the lexemes
    returnStatus = syntaxAnalysis(lexemesList)
    # grammar.analyze(existingLexemesList)
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