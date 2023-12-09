# SAMPLE TEST; TO BE DELETED
test_case = [['HAI', 'Start of Code'], ['\n', 'Line Break'], ['I HAS A', 'Variable Declaration'], ['stuff', 'Variable Identifier'], ['ITZ', 'Assignment Operator'], ['12', 'Integer Literal'], ['\n', 'Line Break'], ['VISIBLE', 'Print Statement'], ['"', 'String Delimeter'], ['noot    noot', 'String Literal'], ['"', 'String Delimeter'], ['var', 'Variable Identifier'], ['\n', 'Line Break'], ['BIGGR OF', 'Bigger Of'], ['dsfd', 'Variable Identifier'], ['AN', 'And Operator'], ['dsfdf', 'Variable Identifier'], ['\n', 'Line Break'], ['KTHXBYE', 'End of Code']]

# GRAMMAR TRANSITIONS
PROGRAM                 = ["Start of Code"]
STATEMENT               = ["Variable Declaration", "Print Statement", "Assignment Operator"]
ARITHMETIC_OPERATOR     = ["Addition Operator", "Modulo Operator", "Division Operator", "Smaller Of", "Subtraction Operator", "Multiplication Operator", "Bigger Of"]
VARIABLE_IDENTIFIER     = ["Variable Identifier"]
LITERAL                 = ["Integer Literal", "Float Literal", "String Literal"]
EXPRESSION              = ["True Expression", "False Expresion", "Variable Identifier"]
STRING_DELIMETER        = ["String Delimeter"]
LINE_BREAK              = ["Line Break"]
AND_OPERATOR            = ["And Operator"]
END_OF_CODE             = ["End of Code"]
COMMENT                 = ["Comment"]
COMMENT_START           = ["Single Line Comment", "Multi Line Comment Start"]
COMMENT_END             = ["Multi Line Comment End"]
R_KEYWORD               = ["R Keyword"]
FUNCTION_START          = ["Function Start"]
YR_LOOP_KEYWORD         = ["YR Loop Keyword"]
RETURN_EXPRESSION       = ["Return Expression"]
FUNCTION_END            = ["Function End"]

class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.lchild = None
        self.rchild = None

    def print_node(node):
        # print value of node
        print(f"\nValue: {node.value}")

        # print node details
        if node.value != "Parser": print(f"Parent: {node.parent.value}")
        if node.lchild is not None: print(f"LChild: {node.lchild.value}")
        if node.rchild is not None: print(f"RChild: {node.rchild.value}")

        # print children of node
        if node.lchild is not None: Node.print_node(node.lchild)
        if node.rchild is not None: Node.print_node(node.rchild)

class Parser:
    def __init__(self, lexemesList):
        # initial values
        self.lexemesList = lexemesList
        self.length = len(self.lexemesList)
        self.cursor = 0
        self.line_count = 1
        self.program_start_node = Node("Parser")
        self.expectation = PROGRAM

        # Flags for checking
        self.MODE_I_HAS_A = False
        self.MODE_VISIBLE = False
        self.MODE_ARITHMETIC = False
        self.MODE_SINGLE_LINE_COMMENT = False
        self.MODE_MULTI_LINE_COMMENT = False
        self.MODE_FUNCTION = False

    # Reset most flags
    def reset_modes(self):
        self.MODE_I_HAS_A = False
        self.MODE_VISIBLE = False
        self.MODE_ARITHMETIC = False
        self.MODE_SINGLE_LINE_COMMENT = False
        # self.MODE_MULTI_LINE_COMMENT -> Cannot be reset
        self.MODE_FUNCTION = False

    # cursor keeps track of which token is currently being analyzed; important for some tokens
    # increments cursor
    def increment_cursor(self):
        self.cursor += 1

    # line_count keeps track of which current line the analyzer is in
    # increments line count
    def increment_line_count(self):
        self.line_count += 1

    # TODO: fix
    def start_of_code(self):
        new_node = Node("Start of Code")
        new_node.parent = self.program_start_node
        self.program_start_node.lchild = new_node

    # functions that deal with each token
    # HAI 
    # | LINE_BREAK
    def handle_start_of_code(self):
        self.expectation = [*LINE_BREAK]

    # KTHXBYE
    # | ;
    def handle_end_of_code(self):
        self.expectation = None 

    # TODO: FIX THIS; should be a terminal
    # LINE BREAK
    # | LINE_BREAK, COMMENT, COMMENT END                                                                       -> for multi line comments
    # | STATEMENT, ARITHMETIC_OPERATOR, COMMENT_START, VARIABLE_IDENTIFIER, RETURN_EXPRESSION, FUNCTION_END    -> for functions
    # | STATEMENT, ARITHMETIC_OPERATOR, COMMENT_START, VARIABLE_IDENTIFIER, FUNCTION_START, END_OF_CODE
    def handle_line_break(self):
        if self.MODE_MULTI_LINE_COMMENT:            self.expectation = [*LINE_BREAK, *COMMENT, *COMMENT_END]; return
        elif self.MODE_FUNCTION:                    self.expectation = [*STATEMENT, *ARITHMETIC_OPERATOR, *COMMENT_START, *VARIABLE_IDENTIFIER, *RETURN_EXPRESSION, *FUNCTION_END]; return
        else:                                       self.expectation = [*STATEMENT, *ARITHMETIC_OPERATOR, *COMMENT_START, *VARIABLE_IDENTIFIER, *FUNCTION_START, *END_OF_CODE] 

        self.reset_modes()
            
    # STATEMENT
    # | VARIABLE_IDENTIFIER     -> for I HAS A          MODE_I_HAS_A = True
    # | STRING_DELIMETER        -> for MODE VISIBLE     MODE_VISIBLE = True
    # | LITERAL
    def handle_statement(self, token_class):
        if token_class == "Variable Declaration":   self.expectation = VARIABLE_IDENTIFIER; self.MODE_I_HAS_A = True
        elif token_class == "Print Statement":      self.expectation = STRING_DELIMETER; self.MODE_VISIBLE = True
        elif token_class == "Assignment Operator":  self.expectation = LITERAL

    # VARIABLE IDENTIFIER
    # | "Assignment Operator", LINE_BREAK, COMMENT_START    -> for I HAS A
    # | LITERAL, LINE_BREAK, COMMENT_START                  -> for VISIBLE
    # | LINE_BREAK, YR_LOOP_KEYWORD                         -> for FUNCTION
    # | LINE_BREAK, COMMENT_START                           -> for ARITHMETIC, prev2_token = VARIABLE_IDENTIFIER
    # | AND_OPERATOR                                        -> for ARITHMETIC
    # | R_KEYWORD                                           -> for prev_token = LINE_BREAK
    # | "Assignment Operator"
    def handle_variable_identifier(self):
        prev_token = self.lexemesList[self.cursor-1][1]
        prev2_token = self.lexemesList[self.cursor-2][1]

        if self.MODE_I_HAS_A:                       self.expectation = ["Assignment Operator", *LINE_BREAK, *COMMENT_START]
        elif self.MODE_VISIBLE:                     self.expectation = [*LITERAL, *LINE_BREAK, *COMMENT_START]
        elif self.MODE_FUNCTION:                    self.expectation = [*LINE_BREAK, *YR_LOOP_KEYWORD]                               
        elif self.MODE_ARITHMETIC:
            if prev2_token in VARIABLE_IDENTIFIER:  self.expectation = [*LINE_BREAK, *COMMENT_START]
            else:                                   self.expectation = AND_OPERATOR
        elif prev_token in LINE_BREAK:              self.expectation = R_KEYWORD     
        else:                                       self.expectation = ["Assignment Operator"]
    
    # LITERAL
    # | STRING_DELIMETER
    # | AND_OPERATOR, LINE_BREAK
    # | AND_OPERATOR
    # | LINE_BREAK, COMMENT_START   -> self.MODE_I_HAS_A = False
    # | STATEMENT
    def handle_literal(self, token_class):
        prev_token = self.lexemesList[self.cursor-1][1]
        if token_class == "String Literal":         self.expectation = STRING_DELIMETER
        elif self.MODE_ARITHMETIC:
            if prev_token in AND_OPERATOR:          self.expectation = [*AND_OPERATOR, *LINE_BREAK]
            elif token_class in LITERAL[:1]:        self.expectation = AND_OPERATOR
        elif self.MODE_I_HAS_A:                     self.expectation = [*LINE_BREAK, *COMMENT_START]; self.MODE_I_HAS_A = False
        else:                                       self.expectation = STATEMENT 

    # STRING DELIMETER
    # | VARIABLE_IDENTIFIER, LINE_BREAK, COMMENT_START -> for String Literal, in mode VISIBLE
    # | STATEMENT
    # | LITERAL
    def handle_string_delimeter(self):
        if self.lexemesList[self.cursor-1][1] == "String Literal":
            if self.MODE_VISIBLE:                   self.expectation = [*VARIABLE_IDENTIFIER, *LINE_BREAK, *COMMENT_START]
            else:                                   self.expectation = STATEMENT
        else:                                       self.expectation = LITERAL

    # ARITHMETIC OPERATOR -> MODE_ARITHMETIC = True
    # | VARIABLE_IDENTIFIER, ARITHMETIC_OPERATOR, LITERAL[:1], AND_OPERATOR
    def handle_arithmetic_operator(self):
        self.MODE_ARITHMETIC = True
        self.expectation = [*VARIABLE_IDENTIFIER, *ARITHMETIC_OPERATOR, *LITERAL[:1], *AND_OPERATOR]

    # AND OPERATOR
    # | VARIABLE_IDENTIFER, LITERAL[:1]
    def handle_and_operator(self):
        self.expectation = [*VARIABLE_IDENTIFIER, *LITERAL[:1]]

    # COMMENT START
    # | LINE_BREAK, COMMENT                 -> for Single Line Comment; MODE_SINGLE_LINE_COMMENT = True
    # | LINE_BREAK, COMMENT, COMMENT_END    -> for Multi Line Comment; MODE_MULTI_LINE_COMMENT = True
    def handle_comment_start(self, token_class):
        if token_class == "Single Line Comment":    self.expectation = [*LINE_BREAK, *COMMENT]; self.MODE_SINGLE_LINE_COMMENT = True
        else:                                       self.expectation = [*LINE_BREAK, *COMMENT, *COMMENT_END]; self.MODE_MULTI_LINE_COMMENT = True

    # COMMENT END
    # | LINE_BREAK
    def handle_comment_end(self):
        self.expectation = LINE_BREAK

    # R KEYWORD -> MODE_I_HAS_A = True
    # | LITERAL
    def handle_r_keyword(self):
        self.MODE_I_HAS_A = True
        self.expectation = LITERAL

    # FUNCTION START -> MODE_FUNCTION
    # | VARIABLE_IDENTIFIER
    def handle_function_start(self):
        self.MODE_FUNCTION = True
        self.expectation = VARIABLE_IDENTIFIER

    # YR LOOP KEYWORD
    # | VARIABLE_IDENTIFIER 
    def handle_yr_loop_keyword(self):
        self.expectation = VARIABLE_IDENTIFIER

    # RETURN EXPRESSION
    # | EXPRESSION, LITERAL, ARITHMETIC_OPERATOR
    def handle_return_expression(self):
        self.expectation = [*EXPRESSION, *LITERAL, *ARITHMETIC_OPERATOR]

    # FUNCTION END -> MODE_FUNCTION = False
    # | LINE_BREAK, COMMENT_START
    def handle_function_end(self):
        self.MODE_FUNCTION = False
        self.expectation = [*LINE_BREAK, *COMMENT_START]

    def evaluate(self, token_class):
        # return flag used for error checking
        success = True
        
        if self.MODE_SINGLE_LINE_COMMENT and token_class in LINE_BREAK: self.MODE_SINGLE_LINE_COMMENT = False   # if a single line comment has been detected PRIOR, disable self.MODE_SINGLE_LINE_COMMENT if a new line is detected 
        elif self.MODE_MULTI_LINE_COMMENT and token_class in COMMENT_END: self.MODE_MULTI_LINE_COMMENT = False  # if a multi line comment has been detected PRIOR, disable self.MODE_SINGLE_LINE_COMMENT if TLDR has been detected

        # print error message if the current token is not in the expected list
        if token_class not in self.expectation or (token_class in RETURN_EXPRESSION and not self.MODE_FUNCTION):
            print(f"\n[!] ERROR: Unknown token of type <{token_class}> detected, expected <" + ', '.join(str(x).replace("\n", "\+n") for x in self.expectation) + ">")
            return False

        # Modify self.expectation depending on what the token is
        if token_class in PROGRAM:                  self.handle_start_of_code()
        elif token_class in END_OF_CODE:            self.handle_end_of_code()
        elif token_class in LINE_BREAK:             self.handle_line_break()
        elif token_class in STATEMENT:              self.handle_statement(token_class)
        elif token_class in VARIABLE_IDENTIFIER:    self.handle_variable_identifier()
        elif token_class in LITERAL:                self.handle_literal(token_class)
        elif token_class in STRING_DELIMETER:       self.handle_string_delimeter()
        elif token_class in ARITHMETIC_OPERATOR:    self.handle_arithmetic_operator()
        elif token_class in AND_OPERATOR:           self.handle_and_operator()
        elif token_class in COMMENT_START:          self.handle_comment_start(token_class)
        elif token_class in COMMENT_END:            self.handle_comment_end()
        elif token_class in R_KEYWORD:              self.handle_r_keyword()
        elif token_class in FUNCTION_START:         self.handle_function_start()
        elif token_class in YR_LOOP_KEYWORD:        self.handle_yr_loop_keyword()
        elif token_class in RETURN_EXPRESSION:      self.handle_return_expression()
        elif token_class in FUNCTION_END:           self.handle_function_end()

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
        #   MAEK <expression> [A] <type>
        #   <variable> IS NOW A <type>
        #   <variable> R MAEK <variable> [A] <type>
        # [ ] IO:
        #   VISIBLE: recognize "!" character
        #   GIMMEH: implement
        #       GIMMEH <variable>
        # [ ] IT variable:
        #   expressions unassigned will be put in a variable called "IT"
        #   gets overwritten for each expresion that was not assigned to a variable
        # [ ] Assigment statements:
        #   double check implementation, should be of the form: <variable> <assignment operator> <expression>
        # [ ] FLOW CONTROL:
        #   if-then:
        #       <expression>
        #       O RLY?
        #       YA RLY
        #           <code block>
        #       NO WAI
        #           <code block>
        #       OIC
        #   case:
        #   loops:

        # TODO: VERY IMPORTANT
        # - turn production into parse tree format
        # - turn line breaks into terminals for each node
        # - define format for each node

        return success
    
    def traverse_nodes(self):
        Node.print_node(self.program_start_node)

    def traverse_tokens(self):
        # reset cursor
        self.cursor = 0
        
        # keep iterating until end of lexeme list
        while(self.cursor != self.length):
            # get the token
            current_token = self.lexemesList[self.cursor]
             
            # stop the loop if an error has been encounted, can be changed to find all errors
            if not self.evaluate(current_token[1]): break

            # print recognized tokens that are not linebreaks or comments
            # TODO: delete the print lines below if output is not needed
            if (current_token[1] == "Start of Code" or (self.cursor > 1 and self.lexemesList[self.cursor-1][1] == "Line Break")):
                if current_token[1] == "Comment": 
                    self.increment_line_count()
                else:
                    print(f"\nLine #{self.line_count}".ljust(15) + f"[!] {current_token[1]}".ljust(30), "->", current_token[0].replace("\n", r"\n"))
                    self.increment_line_count()
            elif not (current_token[1] == "Line Break" or current_token[1] == "Comment"):
                print("".ljust(14) + f"[!] {current_token[1]}".ljust(30), "->", current_token[0].replace("\n", r"\n"))

            # go to next token
            self.increment_cursor()

    def print_tokens(self):
        self.cursor = 0
        while(self.cursor != self.length):
            print(self.lexemesList[self.cursor][0].replace("\n", "\+n"), self.lexemesList[self.cursor][1])
            self.increment_cursor()
        print()
                     
def main():
    parser_obj = Parser(test_case)
    parser_obj.traverse_tokens()

if __name__ == "__main__":
    main()
