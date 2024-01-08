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
existingLexemesDict = {"it": ""}

# contains all usable tokens including REPETITIONS
existingLexemesList = []

# contains the variable names
variable_names = []
variableValues = {}

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
            for each_character in f"{number}":
                if each_character == ".":
                    return False
            print("True")
            return True
        except ValueError:
            
            try:
                int(number[1:-1])
                for each_character in f"{number}":
                    if each_character == ".":
                        return False
                print("True")
                return True
            except ValueError:                
                return False

# Function that converts a given stringed number to its raw numerical value
def get_numerical_value_from_string(number):
    return int(number) if is_int_convertible(number) else round(float(number), 2) if is_float_convertible(number) else number if (number[0] == "\"" and number[-1] == "\"") else number if number in ["WIN", "FAIL"] else "<uninitialized>" 

# Function that executes syntax analysis
def syntaxAnalysis(lexemesList):
    global terminal, existingLexemesDict_newline_reference, variable_names, variableValues

    # variable that stores the syntax errors list, for better printing
    syntax_error_list = []

    # checks for start of code keyword, prompts user if none found
    if lexemesList[1][0] != "HAI":
        syntax_error_list.insert(0, f"Syntax Error [line {existingLexemesDict_newline_reference[0]}]: Start of code not found.\n")

    print(f"{len(lexemesList)} vs {len(existingLexemesDict_newline_reference)}")

    print(existingLexemesDict_newline_reference)

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
                        variableValues[lexemesList[count+3][0]] = ""
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

# print
def visible(valueToPrint):
    global terminal
    terminal.configure(state = "normal")

    terminal.insert(tk.END, valueToPrint)

    terminal.configure(state = "disabled")

# get user input
def gimmeh(variable):
    global terminal

    terminal.configure(state = "normal")
    terminal.insert(tk.END, "\n ")

    input()
    variableValues[variable] = terminal.get("end-1c linestart", tk.END).strip()
    set_variable_value(variable, terminal.get("end-1c linestart", tk.END).strip())

    terminal.insert(tk.END, "\n ")
    terminal.configure(state = "disabled")

# helper function that returns the value of a specific variable
def get_variable_value(variable):
    global variables_list

    print(variables_list)
    print(variable)

    if variable in ["WIN", "FAIL"]:
        return variable 

    print(f"Variable: {variable}")

    if variable.isdigit():
        if variable.find(".") != -1:
            return float(variable)
        else:
            return int(variable)

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
            variableValues[variable] = value
            return value_pair[1]
    return ERROR

# helper function that sets the value of a specific variable
def make_variable_value(variable, value):
    global variables_list
    for value_pair in variables_list:
        if (value_pair[0] == variable):
            return ERROR
    variables_list.append([f"{variable}", value])
    variableValues[variable] = value
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
    if (is_int_convertible(value)):
        return TYPE_INTEGER
    elif (is_float_convertible(value)):
        return TYPE_FLOAT
    elif (get_numerical_value_from_string(value) == "<uninitialized>"):
        return TYPE_UNINITIALIZED
    elif (value in ["WIN", "FAIL"]):
        return TYPE_BOOL
    else:
        return TYPE_STRINGED_NUMBER
    
###### implementation for IS NOW A ######
def is_now_a(variable, target_type):

    # get the value
    variable_value = get_variable_value(variable)
    print(f"\nvariable_value:\t{variable_value}.")

    # this is the current datatype of the variable
    current_type = get_datatype(variable_value)

    # print notifications for now
    print(f"current_type:\t{current_type}")
    print(f"target_type:\t{target_type}\n")

    # in case the same, just end the function
    if current_type == target_type: return

    # in case the current type is an integer (NUMBR)
    if current_type == TYPE_INTEGER:

        # return appropriately according to documentation
        if target_type == TYPE_FLOAT:   
            set_variable_value(variable, float(variable_value))
            return
        if target_type == TYPE_STRINGED_NUMBER:  
            set_variable_value(variable, f"\"{int(variable_value)}\"")
            return
        
    # in case the current type is a float (NUMBAR)
    elif current_type == TYPE_FLOAT:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER: 
            set_variable_value(variable, int(get_numerical_value_from_string(variable_value)))
            return
        if target_type == TYPE_STRINGED_NUMBER:   
            set_variable_value(variable, f"\"{'{:.2f}'.format(get_numerical_value_from_string(variable_value))}\"")
            return

    # in case the current type is a stringed number (YARN)
    elif current_type == TYPE_STRINGED_NUMBER:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER:  
            set_variable_value(variable, int(get_numerical_value_from_string(variable_value[1:-1])))
            return
        if target_type == TYPE_FLOAT:  
            set_variable_value(variable, round(get_numerical_value_from_string(variable_value[1:-1]), 2))
            return

    # in case the value is unitialized
    elif current_type == TYPE_UNINITIALIZED:

        # return appropriately according to documentation
        if target_type == TYPE_BOOL:     
            set_variable_value(variable, "WIN" if (get_variable_value(variable) != ERROR) else "FAIL")
            return
        print("ERROR: Uninitialized can only casted to a TROOF!")
        return       


    # in case the current value is boolean (TROOF)
    elif current_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (variable_value == "WIN"):
            if target_type == TYPE_INTEGER:      
                set_variable_value(variable, int(1))
                return 
            if target_type == TYPE_FLOAT:        
                set_variable_value(variable, round(float(1), 1))
                return 
        else: 
            set_variable_value(variable, 0)
            return 


    # if came up to this point, check if
    # in case the target value is boolean (TROOF)
    if target_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (variable_value == "" or variable_value == 0): 
            set_variable_value(variable, "FAIL")
            return 
        set_variable_value(variable, "WIN")            
        return 
    
    # if up to here, an uknown error!
    print("-------------------- UNKNOWN ERROR --------------------")
    return



###### implementation for MAEK ######
def maek(variable, target_type):

    # get the value
    variable_value = get_variable_value(variable)
    print(f"\nvariable_value:\t{variable_value}.")

    # this is the current datatype of the variable
    current_type = get_datatype(variable_value)

    # print notifications for now
    print(f"current_type:\t{current_type}")
    print(f"target_type:\t{target_type}\n")

    # in case the same, just return the same value
    if current_type == target_type: return variable_value

    # in case the current type is an integer (NUMBR)
    if current_type == TYPE_INTEGER:

        # return appropriately according to documentation
        if target_type == TYPE_FLOAT:   return float(variable_value)
        if target_type == TYPE_STRINGED_NUMBER:  return f"\"{int(variable_value)}\""


    # in case the current type is a float (NUMBAR)
    elif current_type == TYPE_FLOAT:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER: return int(get_numerical_value_from_string(variable_value))
        if target_type == TYPE_STRINGED_NUMBER:  return f"\"{'{:.2f}'.format(get_numerical_value_from_string(variable_value))}\""
    


    # in case the current type is a stringed number (YARN)
    elif current_type == TYPE_STRINGED_NUMBER:

        # return appropriately according to documentation
        if target_type == TYPE_INTEGER: 
            return int(get_numerical_value_from_string(variable_value[1:-1]))
        if target_type == TYPE_FLOAT: 
            return round(get_numerical_value_from_string(variable_value[1:-1]), 2)



    # in case the value is unitialized
    elif current_type == TYPE_UNINITIALIZED:

        # return appropriately according to documentation
        if target_type == TYPE_BOOL:    return "WIN" if (get_variable_value(variable) != ERROR) else "FAIL"
        return ERROR        


    # in case the current value is boolean (TROOF)
    elif current_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (variable_value == "WIN"):
            if target_type == TYPE_INTEGER:     return int(1)
            if target_type == TYPE_FLOAT:       return round(float(1), 1)
        else:
            return 0
        return ERROR        


    # if came up to this point, check if
    # in case the target value is boolean (TROOF)
    if target_type == TYPE_BOOL:

        # return appropriately according to documentation
        if (variable_value == "" or variable_value == 0):
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
        
    # addition
    if operation == "SUM OF":          
        return first_number + second_number
        
    # modulo
    elif operation == "MOD OF":
        return first_number%second_number
        
    # division
    elif operation ==  "QUOSHUNT OF":
        return first_number/second_number
    
    # minimum
    elif operation ==  "SMALLR OF":
        return first_number if first_number<=second_number else second_number
    
    # maximum
    elif operation ==  "BIGGR OF":        
        return first_number if first_number>=second_number else second_number
    
    # difference
    elif operation ==  "DIFF OF":
        return first_number-second_number
    
    # multiplication
    elif operation ==  "PRODUKT OF":
        return first_number*second_number
    
    # default
    else:
        pass      

# global variable na for accessibility
lexemesList = []
current_lexeme_index = 0

# function that executes syntax analysis given lexemes list.
def symbolTableAnalyzer(_lexemesList):
    '''Function that executes syntax analysis given the list of lexemes.
    This function returns a list of identifiers and their values.'''

    # access the global variable
    global variables_list, lexemesList, current_lexeme_index

    # place lexemesList to global variable cuz why not
    lexemesList = _lexemesList

    # reset variables list
    variables_list = [["Identifier", "Value"]]

    # variables
    lexeme_skip_counter = 0
    current_lexeme_index = -1
    indexJump = 0
    loopDict = {}
    functionDict = {}
    arithmetic_operations = []
    arithmetic_operations_counter = []
    arithmetic_values_container = []
    operandList = []
    identifierPerLine = []
    paramList = []
    printList = ""
    booleanOp = ""
    loopOp = ""
    answer = ""
    currentVariable = ""
    currentFunction = ""
    stringFlag = False
    was_arithmetic = False
    was_boolean = False
    was_boolean_inf = False
    anFlag = False
    visibleFlag = False
    printOpFlag = False
    negateFlag = False
    rFlag = False
    oRlyFlag = False
    yaRlyFlag = False
    noWaiFlag = False
    oICFlag = False
    switchFlag = False
    omgFlag = False
    skipOmgFlag = False
    loopFlag = False
    loopLineFlag = False
    loopOpFlag = False
    loopChecker = False
    functionDeclarationFlag = False
    functionCallFlag = False

    # do for every lexeme
    while current_lexeme_index < len(lexemesList)-1:
        current_lexeme_index += 1

        each_item = lexemesList[current_lexeme_index]

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

        # ============= CASE OF: FUNCTION STATEMENTS =============

        # # function call
        # if identifier == "I IZ":
        #     functionCallFlag = True
        #     currentFunction = lexemesList[current_lexeme_index+1][0]

        # if functionCallFlag:
        #     if identifier == "\n":
        #         indexJump = current_lexeme_index + 1

        # # function declaration
        # if identifier == "HOW IZ I":
        #     functionDeclarationFlag = True
        #     current_lexeme_index += 1
        #     functionDict[lexemesList[current_lexeme_index][0]] = []
        
        # elif functionDeclarationFlag:
        #     if identifier == "\n":
        #         functionDict[each_item[0]].append(current_lexeme_index+1)
        #         functionDict[each_item[0]].append(paramList)
        #         paramList = []

        #     if identifier == "YR":
        #         current_lexeme_index += 1
        #         paramList.append(each_item[0])

        #     if identifier == "MKAY":
        #         current_lexeme_index = indexJump

        # ============= CASE OF: LOOP STATEMENTS =============

        if identifier == "IM IN YR":
            loopLineFlag = True
            loopDict[lexemesList[current_lexeme_index+1][0]] = ""
            loopOpFlag = True
            current_lexeme_index += 1

            print(loopDict)
        elif loopLineFlag:

            if loopOpFlag and not loopFlag:
                loopOp = identifier
                loopDict[list(loopDict.keys())[-1]] = [lexemesList[current_lexeme_index+1][0]]
                loopOpFlag = False

            if identifier == "TIL":
                loopChecker = "FAIL"
                loopDict[list(loopDict.keys())[-1]].append(current_lexeme_index)
            elif identifier == "WILE":
                loopChecker = "WIN"
                loopDict[list(loopDict.keys())[-1]].append(current_lexeme_index)

            if identifier == "\n":
                if variableValues["it"] == loopChecker:
                    loopFlag = True
                else:
                    loopFlag = False
                loopLineFlag = False

        elif identifier == "IM OUTTA YR":

            if loopFlag:
                if loopOp == "UPPIN YR":
                    variableValues[loopDict[list(loopDict.keys())[-1]][0]] = int(variableValues[loopDict[list(loopDict.keys())[-1]][0]]) + 1
                    set_variable_value(loopDict[list(loopDict.keys())[-1]][0], int(variableValues[loopDict[list(loopDict.keys())[-1]][0]]))
                    print(variableValues)
                elif loopOp == "NERFIN YR":
                    variableValues[loopDict[list(loopDict.keys())[-1]][0]] = int(variableValues[loopDict[list(loopDict.keys())[-1]][0]]) - 1
                    set_variable_value(loopDict[list(loopDict.keys())[-1]][0], int(variableValues[loopDict[list(loopDict.keys())[-1]][0]]))
                current_lexeme_index = loopDict[list(loopDict.keys())[-1]][1]
                loopLineFlag = True

            else:
                del loopDict[list(loopDict.keys())[-1]]
                print(loopDict)


        # ============= CASE OF: SWITCH-CASE STATEMENTS =============

        # check for a line with only one identifier
        if identifier == "\n":
            if len(identifierPerLine) == 1:
                # if a line has only one identifier, IT = value of identifier
                if identifierPerLine[0][1] == "Variable Identifier":
                    variableValues["it"] = variableValues[identifierPerLine[0][0]]
                elif identifierPerLine[0][0] in ["WIN", "FAIL"] or identifierPerLine[0][1] in ["Integer Literal", "Float Literal"]:
                    variableValues["it"] = identifierPerLine[0][0]
            identifierPerLine = []
        else:
            identifierPerLine.append(each_item)

        # if oic and in switch statement, turn off switchFlag
        if identifier == "OIC" and switchFlag:
            switchFlag = False

        # if skipomgflag = True (omg literal != it value), skip block
        if skipOmgFlag:
            # if literal == omg or omgwtf, skipomgflag = False
            if identifier == "OMG" or identifier == "OMGWTF":
                skipOmgFlag = False
            else:
                continue

        # if literal == wtf, its inside a switch cases
        if identifier == "WTF?":
            switchFlag = True
        elif switchFlag:
            # check for default, turn of switch case
            if identifier == "OMGWTF":
                switchFlag = False
                continue

            # check if gtfo, skip other cases
            elif identifier == "GTFO":
                switchFlag = False
                oICFlag = True
                continue

            # if omg, omgflag = True
            elif identifier == "OMG":
                omgFlag = True

            # if omgflag = true, check if value of it == omg literal
            elif omgFlag:
                # skip code block inside omg if IT value != omg literal
                if each_item[1] == "Variable Identifier":
                    if variableValues["it"] != variableValues[identifier]:
                        skipOmgFlag = True
                
                else:
                    if variableValues["it"] != identifier:
                        skipOmgFlag = True

                omgFlag = False


        # ============= CASE OF: IF-ELSE STATEMENTS =============
        
        # if YA RLY case is true, skip until "NO WAI"
        if noWaiFlag:
            if identifier == "NO WAI":
                noWaiFlag = False
            continue

        # skip until oic was met
        if oICFlag:
            if identifier == "OIC":
                oICFlag = False
            else:
                continue

        # if YA RLY cases is true, run until NO WAI then skip 
        if yaRlyFlag:
            if identifier == "NO WAI":
                yaRlyFlag = False
                oICFlag = True

        # inside an if-else statement
        if identifier == "O RLY?":
            oRlyFlag = True

        # if statement of condition is true, run the block under it and skip the other
        elif oRlyFlag:
            oRlyFlag = False

            if variableValues["it"] == "WIN":
                yaRlyFlag = True
            else:
                noWaiFlag = True

            continue
            
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
                        variables_list.append([lexemesList[current_lexeme_index+1][0], f"\"{lexemesList[current_lexeme_index+3][0]}{lexemesList[current_lexeme_index+4][0]}{lexemesList[current_lexeme_index+5][0]}\""])
                        variableValues[lexemesList[current_lexeme_index+1][0]] = f"\"{lexemesList[current_lexeme_index+3][0]}{lexemesList[current_lexeme_index+4][0]}{lexemesList[current_lexeme_index+5][0]}\""
                    # add properly if number or uninitialized
                    else:
                        print(variables_list)
                        variables_list.append([lexemesList[current_lexeme_index+1][0], f"{get_numerical_value_from_string(lexemesList[current_lexeme_index+3][0])}"])
                        variableValues[lexemesList[current_lexeme_index+1][0]] = f"{get_numerical_value_from_string(lexemesList[current_lexeme_index+3][0])}"
                        print(f"Placed {get_numerical_value_from_string(lexemesList[current_lexeme_index+3][0])}")
                # should skip 3 more items after this iteration
                lexeme_skip_counter = 3

            # if failed, listIndexError means syntactical error
            except IndexError:
                print("Syntactical error was found.")

        # CASE OF: R
        
        if rFlag:
            if identifier in identifier in ["WIN", "FAIL"] or each_item[1] in ["Integer Literal", "Float Literal"]:
                variableValues[currentVariable] = identifier
                set_variable_value(currentVariable, identifier)
                rFlag = False

        if identifier == "R":
            currentVariable = lexemesList[current_lexeme_index-1][0]
            rFlag = True
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
                        each_item[1] = lexemesList[current_lexeme_index+1][0]

        # CASE OF: GIMMEH          
        if identifier == "GIMMEH":
            gimmeh(lexemesList[current_lexeme_index+1][0])
        
        # CASE OF: VISIBLE
        if visibleFlag:
            if each_item[0] == "\n":
                if printOpFlag:
                    printList += str(variableValues["it"])
                    printList += " "
                    printOpFlag = False

                visible(printList+"\n")
                visibleFlag = False
                printList = ""
                continue
            
            if each_item[0] == "\"":
                if stringFlag:
                    stringFlag = False
                else:
                    stringFlag = True
            
            if stringFlag and each_item[0] != "\"":
                printList += each_item[0]
                printList += " "

            elif each_item[1] == "Variable Identifier":
                
                if each_item[0] in variableValues.keys() and not printOpFlag:
                    
                    printList += str(variableValues[identifier])
                printList += " "

            elif identifier in ["WIN", "FAIL"] or each_item[1] in ["Integer Literal", "Float Literal"]:
                printList += each_item[0]
                printList += " "
        
        if identifier == "VISIBLE":
            visibleFlag = True

        # ============= CASE OF: BOOLEAN OPERATIONS ============= 
        if identifier in la.boolean_operations_inf:
            booleanOp = identifier
            was_boolean_inf = True
            if visibleFlag:
                printOpFlag = True
        
        elif was_boolean_inf:
            if identifier == "\n":
                if booleanOp == "ALL OF":
                    answer = True
                elif booleanOp == "ANY OF":
                    answer = False

                for boolean in operandList:
                    if booleanOp == "ALL OF":
                        answer = answer and boolean
                    elif booleanOp == "ANY OF":
                        answer = answer or boolean

                if rFlag:
                    variableValues[currentVariable] = answer
                    if answer:
                        set_variable_value(currentVariable, "WIN")
                    else:
                        set_variable_value(currentVariable, "FAIL")
                    rFlag = False
                else:
                    variableValues["it"] = "WIN" if answer else "FAIL"
                    
                operandList = []
                was_boolean_inf = False

            elif each_item[1] == "Variable Identifier":
                if variableValues[identifier] == "WIN":
                    operandList.append(True)
                elif variableValues[identifier] == "FAIL":
                    operandList.append(False)
            elif identifier == "WIN":
                operandList.append(True)
            elif identifier == "FAIL":
                operandList.append(False)
        
        if identifier in la.boolean_operations:
            booleanOp = identifier
            was_boolean = True
            if visibleFlag:
                printOpFlag = True
        
        elif was_boolean:
            if anFlag:
                if variableValues[identifier] == "WIN":
                    value_2 = True
                else:
                    value_2 = False

                if booleanOp == "BOTH OF":
                    answer = value_1 and value_2
                elif booleanOp == "EITHER OF":
                    answer = value_1 or value_2
                elif booleanOp == "WON OF":
                    answer = value_1 != value_2

                if rFlag:
                    if answer:
                        variableValues[currentVariable] = "WIN"
                        set_variable_value(currentVariable, "WIN")
                    else:
                        variableValues[currentVariable] = "FAIL"
                        set_variable_value(currentVariable, "FAIL")
                    rFlag = False
                else:
                    if answer:
                        variableValues["it"] = "WIN"
                    else:
                        variableValues["it"] = "FAIL"
                
                anFlag = False
                was_boolean = False

            elif identifier == "AN":
                anFlag = True

            else:
                if variableValues[identifier] == "WIN":
                    value_1 = True
                else:
                    value_1 = False

        if identifier == "NOT":
            negateFlag = True
            if visibleFlag:
                printOpFlag = True

        elif negateFlag:
            if variableValues[identifier] == "WIN":
                variableValues["it"] = "FAIL"
            elif variableValues[identifier] == "FAIL":
                variableValues["it"] = "WIN"
            
            negateFlag = False

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
                lexeme_skip_counter = i-2
                was_arithmetic = False
                arithmetic_operations = []
                arithmetic_values_container = []

                # afterwards, procced next item
                continue

            # if not previously arithmetic, check other cases

        #  ============= CASE OF: MAEK ============= 
        if identifier == "MAEK":

            # if pagkatapos nung variable is "A", type is after nun
            if lexemesList[current_lexeme_index+2][0] == "A":

                # maek takes in variable name and target datatype
                result = maek(lexemesList[current_lexeme_index+1][0], lexemesList[current_lexeme_index+3][0])
                lexeme_skip_counter = 3
                
                # if (result != ERROR):
                print(f"Result for MAEK {lexemesList[current_lexeme_index+1][0]} A {lexemesList[current_lexeme_index+3][0]}: {result}")

            # if in case YARN
            else:
                
                 # maek takes in variable name and target datatype
                result = maek(lexemesList[current_lexeme_index+1][0], lexemesList[current_lexeme_index+2][0])
                lexeme_skip_counter = 2
                
                # if (result != ERROR):
                print(f"Result for MAEK {lexemesList[current_lexeme_index+1][0]} {lexemesList[current_lexeme_index+2][0]}: {result}")


        #  ============= CASE OF: IS NOW A ============= 
        if identifier == "IS NOW A":

            # is_now_a takes in variable name and target datatype
            result = is_now_a(lexemesList[current_lexeme_index-1][0], lexemesList[current_lexeme_index+1][0])
            lexeme_skip_counter = 1
            print(f"IS_NOW_A successfully implemented.")
            
        #  ============= CASE OF: SMOOSH ============= 
        if identifier == "SMOOSH":
            
            # collect the strings
            result = " "

            # append appropriately iteratively
            i=0
            while(True):    
                if (lexemesList[current_lexeme_index+i+1][0] == "\""):
                    result += lexemesList[current_lexeme_index+i+2][0]
                    i += 4
                elif (lexemesList[current_lexeme_index+i][0] == "AN"):
                    result += lexemesList[current_lexeme_index+i+1][0]
                    i += 2
                else:
                    break
            
            # result is now complete
            print(f"Result for SMOOSH: {result}")

            # skip properly
            lexeme_skip_counter = i
            

        # The Theoreticals: 
        
        #  ============= CASE OF: BOTH SAEM ============= 
        if identifier == "BOTH SAEM":

            # check if there are BIGGR OF or SMALLR OF keywords
            has_relational_keyword = False
            relational_keyword = ""
            keyword_index = 0
            for index in range(6):
                if lexemesList[current_lexeme_index+index][0] in la.partial_relational_operators:
                    has_relational_keyword = True
                    keyword_index = index
                    relational_keyword = lexemesList[current_lexeme_index+index][0]
                    break

            # CASE OF:
            #    BOTH SAEM <x> AN BIGGR OF <x> AN <y>
            #    BOTH SAEM <x> AN SMALLR OF <x> AN <y>
            if has_relational_keyword:
                        
                # if invalid placement
                if keyword_index != 3 or lexemesList[current_lexeme_index+1][0] != lexemesList[current_lexeme_index+4][0]:
                    print("Error: Invalid syntax found.")
                    if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                        visible(f"Error: Improper syntax found: {lexemesList[current_lexeme_index][0]} {lexemesList[current_lexeme_index+1][0]} {lexemesList[current_lexeme_index+2][0]} {lexemesList[current_lexeme_index+3][0]} {lexemesList[current_lexeme_index+4][0]} {lexemesList[current_lexeme_index+5][0]} {lexemesList[current_lexeme_index+6][0]}.\n")
                
                else:
                    print("Proper placement, trying...")
                    
                    # collect the strings
                    value_1 = lexemesList[current_lexeme_index+1][0]
                    value_2 = lexemesList[current_lexeme_index+6][0]
                    result = ""

                    if relational_keyword == "BIGGR OF":
                        if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}") and get_datatype(get_variable_value(value_1)) >= get_datatype(get_variable_value(value_2)):
                            result = "WIN"
                        else:
                            result = "FAIL"
                        print(f"Result from BOTH SAEM (with BIGGR OF): {result}")            

                    else:
                        if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}") and get_datatype(get_variable_value(value_1)) <= get_datatype(get_variable_value(value_2)):
                            result = "WIN"
                        else:
                            result = "FAIL"
                        print(f"Result from BOTH SAEM (with SMALLR OF): {result}")            
                    
                    # print result to terminal
                    if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                        visible(f"{result}\n")


                # skip properly
                lexeme_skip_counter = 6
                continue

            # CASE OF: BOTH SAEM <x> AN <y>
            # collect the strings
            value_1 = lexemesList[current_lexeme_index+1][0]
            value_2 = lexemesList[current_lexeme_index+3][0]
            result = ""

            if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}"):
                
                result = "WIN"
            else:
                result = "FAIL"
                print(get_variable_value(value_1), get_variable_value(value_2))


            print("Result: ", result)
            variableValues["it"] = result
            print(result)
            print(f"Result from BOTH SAEM: {result}")            

            # print result to terminal
            if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                visible(f"{result}\n")
                    
            # skip properly
            lexeme_skip_counter = 3
            


        #  ============= CASE OF: DIFFRINT ============= 
        if identifier == "DIFFRINT":
            
            # check if there are BIGGR OF or SMALLR OF keywords
            has_relational_keyword = False
            relational_keyword = ""
            keyword_index = 0
            for index in range(6):
                if lexemesList[current_lexeme_index+index][0] in la.partial_relational_operators:
                    has_relational_keyword = True
                    keyword_index = index
                    relational_keyword = lexemesList[current_lexeme_index+index][0]
                    break

            # CASE OF:
            #    DIFFRINT <x> AN BIGGR OF <x> AN <y>
            #    DIFFRINT <x> AN SMALLR OF <x> AN <y>
            if has_relational_keyword:
                        
                # if invalid placement
                if keyword_index != 3 or lexemesList[current_lexeme_index+1][0] != lexemesList[current_lexeme_index+4][0]:
                    print("Error: Invalid syntax found.")
                    if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                        visible(f"Error: Improper syntax found: {lexemesList[current_lexeme_index][0]} {lexemesList[current_lexeme_index+1][0]} {lexemesList[current_lexeme_index+2][0]} {lexemesList[current_lexeme_index+3][0]} {lexemesList[current_lexeme_index+4][0]} {lexemesList[current_lexeme_index+5][0]} {lexemesList[current_lexeme_index+6][0]}.\n")
                
                else:
                    print("Proper placement, trying...")
                    
                    # collect the strings
                    value_1 = lexemesList[current_lexeme_index+1][0]
                    value_2 = lexemesList[current_lexeme_index+6][0]
                    result = ""

                    if relational_keyword == "BIGGR OF":
                        if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}") and get_datatype(get_variable_value(value_1)) > get_datatype(get_variable_value(value_2)):
                            result = "WIN"
                        else:
                            result = "FAIL"
                        print(f"Result from DIFFRINT (with BIGGR OF): {result}")            

                    else:
                        if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}") and get_datatype(get_variable_value(value_1)) < get_datatype(get_variable_value(value_2)):
                            result = "WIN"
                        else:
                            result = "FAIL"
                        print(f"Result from DIFFRINT (with SMALLR OF): {result}")            

                    # print result to terminal
                    if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                        visible(f"{result}\n")
                    
                # skip properly
                lexeme_skip_counter = 6
                continue

            # collect the strings
            print(lexemesList)
            value_1 = lexemesList[current_lexeme_index+1][0]
            value_2 = lexemesList[current_lexeme_index+3][0]
            result = ""

            if (f"{get_variable_value(value_1)}" == f"{get_variable_value(value_2)}"):
                result = "FAIL"
            else:
                result = "WIN"

            variableValues["it"] = result
            print(f"Result from DIFFRINT: {result}")            

            # print result to terminal
            if (lexemesList[current_lexeme_index-1][0] == "VISIBLE"):
                visible(f"{result}\n")
                    
            # skip properly
            lexeme_skip_counter = 3


    return variables_list


def execute():
    tempList = []
    stringTemp = ""
    stringFlag = False
    btwFlag = False
    obtwFlag = False
    editorContent = textEditor.get("0.0", tk.END).split("\n")

    # reset existing lexemes dictionary
    global existingLexemesDict, lexemesList, terminal, existingLexemesDict_newline_reference
    existingLexemesDict = {}
    existingLexemesList = []
    existingLexemesDict_newline_reference = []
    lexemesList = INITIAL_LEXEMES_LIST

    terminal.configure(state = "normal")
    terminal.delete('1.0', tk.END)
    terminal.configure(state = "disabled")

    for line in editorContent:
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
        if token == "OBTW": 
            obtwFlag = True
        elif obtwFlag == True:
            print(f"OBTW flag is on, on current item '{token}'.")
            if token == "TLDR":     
                obtwFlag = False
            else:
                # existingLexemesDict[token] = "Comment"
                # existingLexemesList.append([token, "Comment"])          
                # existingLexemesDict_newline_reference.append(current_newline_count)         
                # print(f"Current existing Lexemes: {existing}")
                continue

        # if token not in keywords
        if token not in la.allKeywords.keys() or current_iterator != la.iterator:
            if re.search("[0-9]\.[0-9]", token) != None and token[0] == "\"" and token[-1] == "\"":
                existingLexemesDict[token] = "Stringed Number Literal"
                existingLexemesList.append([token, "Stringed Number Literal"])
                existingLexemesDict_newline_reference.append(current_newline_count)
                continue
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

            if token[0] == "\"" and not stringFlag:
                existingLexemesDict["\""] = "String Delimeter"   # mark it as a string literal
                existingLexemesList.append(["\"", "String Delimeter"])
                existingLexemesDict_newline_reference.append(current_newline_count)
                stringTemp += token     # append the token
                stringTemp += " "       # add a space
                stringFlag = True       # next token will be part of the string
            # if the previous token is an unpaired '\"'
                       
                if token[-1] == "\"" and token != "\"":
                    existingLexemesDict[f"{token[1:-1]}"] = "String Literal"   # mark it as a string literal
                    existingLexemesList.append([f"{token[1:-1]}", "String Literal"])
                    existingLexemesDict["\""] = "String Delimeter"   # mark it as a string literal
                    existingLexemesList.append(["\"", "String Delimeter"])
                    stringFlag = False
                    stringTemp = ""
            
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
                print(f"Current token is {token} and is {'found' if token in current_iterator else 'not found'} in current_iterator {current_iterator}.")
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
    
    print(lexemesList)

    for widget in lexemesFrame.winfo_children(): widget.destroy()

    lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
    lexemesLabel.pack(expand=True, fill="both", padx=5)

    # do not added Line Breaks or Comments to the lexemesTable
    filtered_lexeme_list = [x for x in lexemesList if not(x[1]== "Line Break" or x[1]=="Comment")]
    lexemesTable = CTkTable(lexemesFrame, row = len(filtered_lexeme_list), column = 2, values = filtered_lexeme_list)
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


#--- chooseFile [select button] ---#
# - opens filedialog; open file from directory
# - tokenize each lexemes
# - appends the file to the text editor
# - classifies each lexeme; display to the lexeme table
def chooseFile(fileDirLabel, textEditor, lexemesFrame, symbolTableFrame):
    codeString = ""
    fileDirectory = filedialog.askopenfilename()

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
    # line_count = 0
    for line in inputFile:
        # line_count += 1
        # codeString += f'{"{:02d}".format(line_count)}   |     ' + line                  # store all lines in codeString  
        codeString += line

    # reset the text field
    textEditor.delete('1.0', tk.END)

    # display code in the text field
    textEditor.insert("0.0", codeString)

# draw the main window
def draw():
    '''Function that draws the main window.'''

    # access the global variables
    global fileDirectory, lexemesList, existingLexemesDict, terminal, textEditor, lexemesFrame, symbolTableFrame

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

    textEditor = tk.CTkTextbox(fileExpFrame, width = 600, height=265)
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
    executeButton = tk.CTkButton(terminalFrame, text = "EXECUTE", command = execute)
    executeButton.pack(expand=True, fill="both", padx=5, pady=5)

    terminal = tk.CTkTextbox(terminalFrame, width = 1270, height=265, state = "disabled")
    terminal.pack(expand=True, fill="both", padx=5, pady=5)

    root.mainloop()


# main function
def main():
    draw() # draw the actual window


# start the main program
if __name__ == "__main__":
    main()