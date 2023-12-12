# SAMPLE TEST; TO BE DELETED
test_case = [['HAI', 'Start of Code'], ['\n', 'Line Break'], ['I HAS A', 'Variable Declaration'], ['var', 'Variable Identifier'], ['ITZ', 'Assignment Operator'], ['12', 'Integer Literal'], ['\n', 'Line Break'], ['I HAS A', 'Variable Declaration'], ['var', 'Variable Identifier'], ['ITZ', 'Assignment Operator'], ['12', 'Integer Literal'], ['BTW', 'Single Line Comment'], ['test', 'Comment'], ['\n', 'Line Break'], ['var', 'Variable Identifier'], ['R', 'R Keyword'], ['11', 'Integer Literal'], ['\n', 'Line Break'], ['VISIBLE', 'Print Statement'], ['"', 'String Delimeter'], ['noot    noot', 'String Literal'], ['"', 'String Delimeter'], ['var', 'Variable Identifier'], ['\n', 'Line Break'], ['OBTW', 'Multi Line Comment Start'], ['\n', 'Line Break'], ['test', 'Comment'], ['\n', 'Line Break'], ['test', 'Comment'], ['test', 'Comment'], ['test', 'Comment'], ['test', 'Comment'], ['\n', 'Line Break'], ['TLDR', 'Multi Line Comment End'], ['\n', 'Line Break'], ['BIGGR OF', 'Bigger Of'], ['10', 'Integer Literal'], ['AN', 'An Keyword'], ['100', 'Integer Literal'], ['\n', 'Line Break'], ['HOW IZ I', 'Function Start'], ['MAINUMBA', 'Variable Identifier'], ['\n', 'Line Break'], ['I HAS A', 'Variable Declaration'], ['var', 'Variable Identifier'], ['\n', 'Line Break'], ['BTW', 'Single Line Comment'], ['test', 'Comment'], ['\n', 'Line Break'], ['FOUND YR', 'Return Expression'], ['var2', 'Variable Identifier'], ['\n', 'Line Break'], ['IF U SAY SO', 'Function End'], ['\n', 'Line Break'], ['KTHXBYE', 'End of Code']]

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
# [X] Assigment statements:
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

class Node:
    def __init__(self, value, lchild, rchild):
        self.value = value
        self.lchild = lchild
        self.rchild = rchild

    def print_info(self):
        if self.value == "Line Break": return

        # print value
        print(f"<TYPE: {self.value}> ", end="")
              
        # print lchild
        if type(self.lchild) == list:
            print("<lchild: [ \n", end="")
            [(print("".ljust(4), end=""), x.print_info()) for x in self.lchild if x.value != "Line Break"]
            print("\t]> ", end = "")
        else:
            print(f"<lchild: {self.lchild}> ", end= "")

        # print rchild
        if type(self.rchild) == list: 
            print(f"<rchild: [ \n", end = "")
            [(print("".ljust(4), end=""), x.print_info()) for x in self.rchild if x.value != "Line Break"]
            print("\t]>")
        else: 
            print(f"<rchild: {self.rchild}> ")


# TOKEN CLASS
TOK_START_OF_CODE = "Start of Code"
TOK_END_OF_CODE = "End of Code"

TOK_VARIABLE_IDENTIFIER = "Variable Identifier"
TOK_ASSIGMENT_OPERATOR = "Assignment Operator"
TOK_VARIABLE_DECLARATION = "Variable Declaration"
TOK_PRINT_STATEMENT = "Print Statement"
TOK_RETURN_EXPRESSION = "Return Expression"
TOK_FUNCTION_START = "Function Start"
TOK_FUNCTION_END = "Function End"
TOK_R_KEYWORD = "R Keyword"
TOK_AN_KEYWORD = "An Keyword"
TOK_YR_KEYWORD = "YR Loop Keyword"
TOK_STRING_DELIMETER = "String Delimeter"

TOK_SINGLE_LINE_COMMENT = "Single Line Comment"
TOK_MULTI_LINE_COMMENT_START = "Multi Line Comment Start"
TOK_MULTI_LINE_COMMENT_END = "Multi Line Comment End"
TOK_COMMENT_START = [TOK_SINGLE_LINE_COMMENT, TOK_MULTI_LINE_COMMENT_START]

TOK_LINE_BREAK = "Line Break"
TOK_COMMENT = "Comment"
TOK_LINE_ENDING = [TOK_SINGLE_LINE_COMMENT, TOK_MULTI_LINE_COMMENT_START, TOK_LINE_BREAK]

TOK_INTEGER_LITERAL = "Integer Literal"
TOK_FLOAT_LITERAL = "Float Literal"
TOK_STRING_LITERAL = "String Literal"
TOK_NON_STRING_LITERAL = [TOK_INTEGER_LITERAL, TOK_FLOAT_LITERAL] 
TOK_LITERAL = [TOK_INTEGER_LITERAL, TOK_FLOAT_LITERAL, TOK_STRING_LITERAL]

TOK_ADDITION        = "Addition Operator"
TOK_SUBTRACTION     = "Subtraction Operator" 
TOK_MULTIPLICATION  = "Multiplication Operator"
TOK_DIVISION        = "Division Operator"
TOK_MODULO          = "Modulo Operator"
TOK_SMALLER_OF      = "Smaller Of"
TOK_BIGGER_OF       = "Bigger Of"

TOK_ARITHMETIC = [TOK_ADDITION, TOK_SUBTRACTION, TOK_MULTIPLICATION, TOK_DIVISION, TOK_MODULO, TOK_SMALLER_OF, TOK_BIGGER_OF]

TOK_BANNED_FUNCTION = [TOK_FUNCTION_START, TOK_START_OF_CODE]

# TODO: Simplify
# example:
# I HAS A <var> ITZ <expr> = Node(Variable Declaration, self.var(), self.expr)

# GRAMMAR
G_START_OF_CODE         = [TOK_START_OF_CODE]
G_VARIABLE_DECLARATION  = [[TOK_VARIABLE_DECLARATION, TOK_VARIABLE_IDENTIFIER, TOK_ASSIGMENT_OPERATOR, TOK_LITERAL],
                            [TOK_VARIABLE_DECLARATION, TOK_VARIABLE_IDENTIFIER]]
G_VARIABLE_ASSIGNMENT   = [TOK_VARIABLE_IDENTIFIER, TOK_R_KEYWORD, TOK_LITERAL]
G_LINE_ENDING           = [[TOK_LINE_BREAK],
                            [TOK_SINGLE_LINE_COMMENT, TOK_COMMENT],
                            [TOK_MULTI_LINE_COMMENT_START, TOK_COMMENT]]
G_END_OF_CODE           = [TOK_END_OF_CODE]
G_ARITHMETIC            = [TOK_ARITHMETIC, [*TOK_NON_STRING_LITERAL, TOK_VARIABLE_IDENTIFIER], TOK_AN_KEYWORD, [*TOK_NON_STRING_LITERAL, TOK_VARIABLE_IDENTIFIER]]
G_RETURN_EXPRESSION     = [TOK_RETURN_EXPRESSION, [*TOK_LITERAL, TOK_VARIABLE_IDENTIFIER]]

class Parser:
    def __init__(self, lexemesList):
        # initial values
        self.lexemesList = lexemesList
        self.length = len(self.lexemesList)

        self.cursor = 0
        self.line_count = 1

        self.buf = []
        self.error = False
        self.supress_error = False

    # cursor keeps track of which token is currently being analyzed; important for some tokens; increments cursor
    def increment_cursor(self): self.cursor += 1

    # line_count keeps track of which current line the analyzer is in; increments line count
    def increment_line_count(self): self.line_count += 1   

    # print error message
    def throw_error(self, got, expected): print(f"[!] Error: Got {got}, Expected {expected}.")

    # buf used for certain token recognitions
    def reset_buf(self): self.buf = []

    # return a token
    def get_token(self): return self.lexemesList[self.cursor]

    # return a token class
    def get_token_class(self): return self.lexemesList[self.cursor][1]

    # return the nexgt token class
    def get_next_token_class(self): return self.lexemesList[self.cursor+1][1] if self.cursor+1 != self.length else "Error"

    # handle error
    def return_error(self):
        self.error = True
        return Node("ERROR", ";", ";")

    # check if sequence of tokens fit the grammar
    def check_valid(self, grammar):
        self.reset_buf()

        for x in grammar:
            self.buf.append(self.get_token())
            if (self.buf[len(self.buf)-1][1] not in x):      
                if not self.supress_error: self.throw_error(self.get_token_class(), x)
                return False
            else:
                self.increment_cursor()

        return True

    # TODO: REWRITE TO ONE FUNCTION
    # handle start of code
    def start_of_code(self):
        if self.check_valid(G_START_OF_CODE):       return Node(f"Statement: {TOK_START_OF_CODE}", ";", ";")
        return self.return_error()    
        
    # handle end of code
    def end_of_code(self):
        if self.check_valid(G_END_OF_CODE):         return Node(f"Statement: {TOK_END_OF_CODE}", ";", ";")
        return self.return_error()

    # handle variable assignment
    def variable_assignment(self): 
        if self.check_valid(G_VARIABLE_ASSIGNMENT): return Node("Statement: Variable Assignment", self.buf[0][0], self.buf[2][0])
        return self.return_error()
    
    # handle arithmetic operations; all operations are binary
    def arithmetic(self): 
        if self.check_valid(G_ARITHMETIC):          return Node(f"Statement: Arithmetic Operation - {self.buf[0][1]}", self.buf[1][0], self.buf[3][0])
        return self.return_error()
        
    # handle return expression
    def return_expression(self):
        if self.check_valid(G_RETURN_EXPRESSION):   return Node(f"Statement: Return Expression", self.buf[1][0], ";")
        return self.return_error()

    # handle function end
    def function_end(self):
        self.increment_cursor()
        return Node("Statement: Function End", ";", ";")

    # handle new line
    def new_line(self):
        self.increment_cursor()
        return Node(f"Line Break", ";", ";")

    # handle variable declaration
    def variable_declaration(self):
        # True for grammar with multiple values
        self.supress_error = True

        # iterate through the grammar list
        for grammar in G_VARIABLE_DECLARATION:
            if self.check_valid(grammar):
                if G_VARIABLE_DECLARATION.index(grammar) == 0:      return Node(f"Statement: {TOK_VARIABLE_DECLARATION}", self.buf[1][0], self.buf[3][0])   # I HAS A <VARIABLE_IDENTIFIER> ITZ <LITERAL> <LINE_BREAK>
                elif G_VARIABLE_DECLARATION.index(grammar) == 1:    return Node(f"Statement: {TOK_VARIABLE_DECLARATION}", self.buf[1][0], ";")              # I HAS A <VARIABLE_IDENTIFIER> <LINE_BREAK>
            else:
                self.cursor = self.cursor - len(self.buf) + 1       # reset cursor         
                if G_VARIABLE_DECLARATION.index(grammar)+1 == len(G_VARIABLE_DECLARATION): self.supress_error = False   # stop supressing errors if the next grammar is the last in the grammar list
                continue # continue iteration
        
        # return error
        self.throw_error(self.get_token_class(), G_VARIABLE_DECLARATION)
        return self.return_error()

    # handle print statement
    def print_statement(self):
        print_buf = []
        self.increment_cursor()

        # keep iterating until error or new line
        while(True):
            next_token = self.get_token()
            self.increment_cursor()

            if next_token[1] == TOK_LINE_BREAK:                             return Node(f"Statement: {TOK_PRINT_STATEMENT}", print_buf, ";")    # end print 
            elif next_token[1] in [*TOK_LITERAL, TOK_VARIABLE_IDENTIFIER]:  print_buf.append(Node("Argument: ", next_token[1], next_token[0]))  # continue print
            elif next_token[1] == TOK_STRING_DELIMETER:                     continue                                                            # ignore \"
            else:                                                           break                                                               # error
                
        # return error
        self.throw_error(next_token[1], [*TOK_LITERAL, TOK_VARIABLE_IDENTIFIER])
        return self.return_error()

    # handle comments
    def comment_start(self):
        root_class = self.get_token_class()
        self.increment_cursor()

        # single line 
        if root_class == TOK_SINGLE_LINE_COMMENT:   
            while(True):
                next_token_class = self.get_token_class()
                self.increment_cursor()
                if next_token_class == TOK_LINE_BREAK: return Node("Statement: Single Comment", ";", ";")
        # multi line
        else:
            while(True):
                next_token_class = self.get_token_class()
                self.increment_cursor()
                if next_token_class == TOK_MULTI_LINE_COMMENT_END: return Node("Statement: Multi Comment", ";", ";")
                if self.cursor == self.length: break
                    
        # return error
        self.return_error()
        self.throw_error(next_token_class, TOK_END_OF_CODE)

    # handle function
    def function_start(self):
        function_buf = []

        self.increment_cursor()
        if self.get_token_class() != TOK_VARIABLE_IDENTIFIER: return self.return_error()

        function_buf.append(Node("Argument:", TOK_VARIABLE_IDENTIFIER, self.get_token()[0]))
        self.increment_cursor()

        # catch all TOK_YR_KEYWORD TOK_VARIABLE_IDENTIFIER
        while(True):
            token_class = self.get_token_class()
            if token_class != TOK_YR_KEYWORD: break
            else:
                self.increment_cursor()
                token_class = self.get_token_class()
                if token_class == TOK_VARIABLE_IDENTIFIER:
                    function_buf.append(Node("Argument:", TOK_VARIABLE_IDENTIFIER, self.get_token()[0]))
                    self.increment_cursor()
                else:
                    self.throw_error(token_class, TOK_VARIABLE_IDENTIFIER)
                    return self.return_error()

        # catch all statements inside function
        while(True):
            token_class = self.get_token_class()
            if token_class in TOK_BANNED_FUNCTION:      return self.return_error()
            elif token_class == TOK_END_OF_CODE:        break

            new_node = self.evaluate()

            if new_node.value == "Error":               return self.return_error()
            elif new_node.value == TOK_FUNCTION_END:    break
            
            function_buf.append(new_node)

        return Node(f"Statement: {TOK_FUNCTION_START}", function_buf, ";")

    # match token/series of tokens 
    def evaluate(self):
        token_class = self.get_token_class()

        # decide
        if token_class == TOK_START_OF_CODE and self.cursor == 0:                                       return self.start_of_code()
        elif token_class == TOK_END_OF_CODE and self.cursor == self.length - 1:                         return self.end_of_code()
        elif token_class == TOK_VARIABLE_DECLARATION:                                                   return self.variable_declaration()
        elif token_class == TOK_PRINT_STATEMENT:                                                        return self.print_statement()
        elif token_class == TOK_RETURN_EXPRESSION:                                                      return self.return_expression()
        elif token_class == TOK_FUNCTION_START:                                                         return self.function_start()
        elif token_class == TOK_FUNCTION_END:                                                           return self.function_end()
        elif token_class in TOK_ARITHMETIC:                                                             return self.arithmetic()
        elif token_class in TOK_COMMENT_START:                                                          return self.comment_start()
        elif [token_class, self.get_next_token_class()] == [TOK_VARIABLE_IDENTIFIER, TOK_R_KEYWORD]:    return self.variable_assignment()
        elif token_class in TOK_LINE_ENDING:                                                            return self.new_line()
        else:                                                                                           self.error = True; return Node("Error", "Unknown Token", token_class)

    # solve each tokenn
    def solve(self):
        self.cursor = 0

        # keep iterating until end of lexeme list
        while(self.cursor != self.length):
            Node.print_info(self.evaluate())
            if self.error: break        

    # execute solve
    def traverse_tokens(self): self.solve()
                     
def main():
    parser_obj = Parser(test_case)
    # for i in parser_obj.lexemesList:
    #     if i[1] == "Line Break": print(i)
    #     else: print(i, end="")
    # print()
    parser_obj.traverse_tokens()
    print()
    # parser_obj.traverse_nodes(parser_obj.program_node)

if __name__ == "__main__":
    main()
