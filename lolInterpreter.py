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
def get_numerical_value_from_string(number):
    return int(number) if is_int_convertible(number) else round(float(number), 2) if is_float_convertible(number) else "<uninitialized>" 

# Function that executes syntax analysis
def syntaxAnalysis(lexemesList):
    global terminal, existingLexemesDict_newline_reference, variable_names

    # variable that stores the syntax errors list, for better printing
    syntax_error_list = []

    # checks for start of code keyword, prompts user if none found
    if lexemesList[1][0] != "HAI":
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
        if i[0] == "I HAS A":
            print("==============================OAIDFJOASJDASIJASDOIJD======================")
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

# TODO: recognize commas

# TODO:
# [ ] unary opeartors
# [ ] check if operator is binary or has infinite arity
#   - check arithmetic operators
# [ ] booleans:
#   unary:      NOT <x>
#   binary:     BOTH OF <x> [AN] <y>
#               EITHER OF <x> [AN] <y>
#               WON OF <x> [AN] <y>
#   infinite:   ALL OF <x> [AN] <y> ... MKAY
#               ANY OF <x> [AN] <y> ... MKAY
# [ ] comparison:
#   binary:     BOTH SAEM <x> [AN] <y>
#               DIFFRINT <x> [AN] <y>
#   special:    <expression>, DIFFRINT IT AN SMALLR OF IT AN <y>


# [ ] casting:

# global variable: list of global variables
variables_list = [["Identifier", "Value"]]

# helper function that returns the value of a specific variable
def get_variable_value(variable):
    global variables_list
    for value_pair in variables_list:
        if (value_pair[0] == variable):
            return value_pair[1]
    return ERROR

# helper function that sets the value of a specific variable
def set_variable_value(variable, value):
    global variables_list
    for value_pair in variables_list:
        if (value_pair[0] == variable):
            value_pair[1] = value
            return value_pair[1]
    return ERROR

# helper function that sets the value of a specific variable
def make_variable_value(variable, value):
    global variables_list
    for value_pair in variables_list:
        if (value_pair[0] == variable):
            return ERROR
    variables_list.append([f"{variable}", value])
    return value

###### global variables for casting ######
TYPE_INTEGER = "NUMBR"
TYPE_FLOAT = "NUMBAR"
TYPE_UNINITIALIZED = "NOOB"
TYPE_BOOL = "TROOF"
TYPE_STRINGED_NUMBER = "YARN"
ERROR = "error"

# function that determines the datatype of a variable
def get_datatype(value):
    if (is_float_convertible(value)):
        return TYPE_FLOAT
    elif (is_int_convertible(value)):
        return TYPE_INTEGER
    elif (get_numerical_value_from_string(value) == "<uninitialized>"):
        return TYPE_UNINITIALIZED
    elif (value in ["WIN", "FAIL"]):
        return TYPE_BOOL
    else:
        return TYPE_STRINGED_NUMBER
    
###### implementation for IS NOW A ######
def is_now_a(variable_name, value, type):
  if type == TYPE_INTEGER:
    return int(value)
  else:
    return float(value)

###### implementation for MAEK ######
def maek(variable, value, target_type):

    # this is the current datatype of the variable
    current_type = get_datatype(value)



    # in case the current type is an integer (NUMBR)
    if current_type == TYPE_INTEGER:

        # return appropriately according to documentation
        if target_type == TYPE_FLOAT:   return float(value)
        if target_type == TYPE_STRINGED_NUMBER:  return f"{value}"


    # in case the current type is a float (NUMBAR)
    elif current_type == TYPE_FLOAT:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER: return int(value)
        if target_type == TYPE_STRINGED_NUMBER:  return f"{round(float(value), 2)}"
    


    # in case the current type is a stringed number (YARN)
    elif current_type == TYPE_STRINGED_NUMBER:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER: 
            return get_numerical_value_from_string(value)



    # in case the value is unitialized
    elif current_type == TYPE_UNINITIALIZED:

        # return appropriately according to documentation
        if target_type == TYPE_BOOL:    return "WIN" if (get_variable_value(variable) != ERROR) else "FAIL"
        return ERROR        


    # in case the current value is boolean (TROOF)
    elif current_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (value == "WIN"):
            if target_type == TYPE_INTEGER:     return int(1)
            if target_type == TYPE_FLOAT:       return round(float(1), 1)
        else:
            return 0
        return ERROR        


    # if came up to this point, check if
    # in case the target value is boolean (TROOF)
    if target_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (value == "" or value == 0):
            return "FAIL"
        return "WIN"
    
    # if up to here, an uknown error!
    print("-------------------- UNKNOWN ERROR --------------------")
    return ERROR

# function that performs a given arithmetic operation properly and its stringed numbers
def perform_arithmetic_operation(operation, value_1, value_2):

    # variables here
    first_number = get_numerical_value_from_string(value_1)
    second_number = get_numerical_value_from_string(value_2)
        
    # switch statement
    match operation:

        # addition
        case "SUM OF":          
            return first_number + second_number
        
        # modulo
        case "MOD OF":
            return first_number%second_number
        
        # division
        case "QUOSHUNT OF":
            return first_number/second_number
        
        # minimum
        case "SMALLR OF":
            return first_number if first_number<=second_number else second_number
        
        
        # maximum
        case "BIGGR OF":        
            return first_number if first_number>=second_number else second_number
        
        # difference
        case "DIFF OF":
            return first_number-second_number
        
        
        # multiplication
        case "PRODUKT OF":
            return first_number*second_number
        
        # default
        case _:
            pass      

# function that executes syntax analysis given lexemes list.
def symbolTableAnalyzer(lexemesList):
    '''Function that executes syntax analysis given the list of lexemes.
    This function returns a list of identifiers and their values.'''

    # reset variables list
    variables_list = [["Identifier", "Value"]]

    # variables
    lexeme_skip_counter = 0
    current_lexeme_index = -1
    arithmetic_operations = []
    arithmetic_operations_counter = []
    arithmetic_values_container = []
    was_arithmetic = False

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
            
            # if failed, listIndexError means syntactical error
            try:

                # check if not yet duplicate
                is_duplicate = False
                for item in variables_list:

                    # add item only if not duplicate
                    if item[0] == lexemesList[current_lexeme_index+1][0]:
                        is_duplicate = True
                        break
                
                # variable name is next item, also its value is current index + 3
                if not is_duplicate:

                    # add properly if string
                    if lexemesList[current_lexeme_index+4][1] == "String Literal":
                        variables_list.append([lexemesList[current_lexeme_index+1][0], f"{lexemesList[current_lexeme_index+3][0]}{lexemesList[current_lexeme_index+4][0]}{lexemesList[current_lexeme_index+5][0]}"])

                    # add properly if number or uninitialized
                    else:
                        variables_list.append([lexemesList[current_lexeme_index+1][0], f"{get_numerical_value_from_string(lexemesList[current_lexeme_index+3][0])}"])

                # should skip 3 more items after this iteration
                lexeme_skip_counter = 3

            # if failed, listIndexError means syntactical error
            except IndexError:
                print("Syntactical error was found.")

        # CASE OF: R
        if identifier == "R":
            print("==================================================")
            value = get_numerical_value_from_string(lexemesList[current_lexeme_index+1][0])
            
            # find the value and update value
            index = -1
            for each_item in variables_list:
                index += 1
                if each_item[0] == lexemesList[current_lexeme_index-1][0]:

                    # update if string
                    if lexemesList[current_lexeme_index+2][1] == "String Literal":
                        each_item[1] = f"{lexemesList[current_lexeme_index+1][0]}{lexemesList[current_lexeme_index+2][0]}{lexemesList[current_lexeme_index+3][0]}"
                    
                    # update if number or float
                    else:
                        # update if found
                        print(f"Currently on {lexemesList[current_lexeme_index-1]}")
                        each_item[1] = lexemesList[current_lexeme_index+1][0]



        # ============= CASE OF: ARITHMETIC OPERATIONS ============= 
        if identifier in la.arithmetic_operations:

            # add to arithmetic operations
            arithmetic_operations.append(identifier)
            arithmetic_operations_counter.append(identifier)

            # make the switch true
            was_arithmetic = True

        # if term is hindi na arithmetic
        else:

            # check if it was previously arithmetic
            if (was_arithmetic):

                # access na yung ibang values
                arithmetic_values_container.append(identifier)
                i=2
                for item in reversed(arithmetic_operations): 
                    arithmetic_values_container.append(lexemesList[current_lexeme_index+i][0])
                    i = i+2

                # compute the value
                    print("\nStarting arithmetic operations\n")
                for each_operation in reversed(arithmetic_operations): 
                    print(f"On queue for operation {each_operation}:")
                    value_1 = arithmetic_values_container.pop(0)
                    print(f"accumulator[0]: {value_1}")
                    value_2 = arithmetic_values_container.pop(0)
                    print(f"accumulator[1]: {value_2}\n")
                    arithmetic_values_container.insert(0, perform_arithmetic_operation(each_operation, value_1, value_2))
                print(f"Final value: {arithmetic_values_container[0]}\n")

                # skip the number of times according sa i
                lexeme_skip_counter = i
                was_arithmetic = False
                arithmetic_operations = []
                arithmetic_values_container = []

                # afterwards, procced next item
                continue

            # if not previously arithmetic, check other cases


    return variables_list



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


    # variable that stores the current string for strings with two or more values
    # this will be empty if placed in dictionary, else not empty
    # [!] used for keywords with multiple tokens
    stack_string_variable = ""

    # variable that stores the current iterator
    current_iterator = la.iterator
    
    # iterate through each token in the tempList
    current_newline_count = 1
    
    for token in tempList:
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
                    # print(stringTemp)
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

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)

    # do not added Line Breaks or Comments to the lexemesTable
    filtered_lexeme_list = [x for x in lexemesList if not(x[1]== "Line Break" or x[1]=="Comment")]
    lexemesTable = CTkTable(lexemesFrame, row = len(lexemesList), column = 2, values = filtered_lexeme_list)
    lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

    # TODO: for testing; should be removed
    print("\n\n#--------------------------- [!] DO TRAVERSAL [!] --------------------------- #")
    new_parser = parser.Parser(lexemesList[1:])
    new_parser.traverse_tokens()

    # execute analysis on the lexemes

    # [!] ENABLE IF NEEDED:
    # returnStatus = syntaxAnalysis(lexemesList)
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