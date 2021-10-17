import ply.yacc as yacc
import ply.lex as lex
import sys
from lex1 import tokens, run_lex

class Variable:
    def __init__(self, type_, name_, visibility_):
        self.type = type_
        self.name = name_
        self.visibility = visibility_

class Structurs:
    def __init__(self, variables_):
        self.variables = []

class Function:
    def __init__(self, name_, count_variable_, body_):
        self.name = name_
        self.count_variable = count_variable_
        self.body = body_


class Program:
    def __init__(self):
        self.variables = []
        self.functions = []

##############################
main_program = Program()

function_variables = []
count = 1
##############################

precedence = (
     ('left', 'FUNCTION_DEFINITION', 'SPACE', "FUNCTION_NAME", "OPEN_SHAPED_BR", "BODY", "CLOSE_SHAPED_BR"),
)

start = 'functions'

def p_functions(p):
    '''functions : main
                 | FUNCTION_DEFINITION multispace FUNCTION_NAME variables OPEN_SHAPED_BR BODY CLOSE_SHAPED_BR functions'''
    if len(p) != 2 :
        function = Function(p[3], function_variables, p[6])
        function_variables.clear()
        main_program.functions.append(function)
        print(main_program)



def p_variables(p):
    '''variables : multispace OPEN_CIRC_BR CONSTRUCT variables CLOSE_CIRC_BR variables
                 | multispace OPEN_CIRC_BR CONSTRUCT variables CLOSE_CIRC_BR 
                 | multispace VARIABLE variables
                 | multispace VARIABLE 
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!
    global count
    if len(p) ==  3:
        function_variables.append(Variable(int, p[2], 0)) # пока int, потом нужно немного поменять
        count = 1
        p[0] = count
    elif len(p) == 4 : 
        function_variables.append(Variable(int, p[2], 0)) # пока int, потом нужно немного поменять
        count += 1
        p[0] = count
    else :
        variables_ = []
        for i in range(1, count) : 
            variables_.append(function_variables[-1])
            function_variables.pop()
        function_variables.append(Structurs(variables_))


def p_main(p):
    ''' main : MAIN main_functions'''
    print("main hihihaha")

def p_main_functions(p):
    '''main_functions : multispace call_functions LOGICAL_OR call_functions SEMICOLON main_functions
                      | multispace call_functions SEMICOLON main_functions
                      | multispace new_variable SEMICOLON main_functions
                      | multispace unification SEMICOLON main_functions
                      | multispace change_variable SEMICOLON main_functions
                      | '''
    if len(p) > 1 :
        print(p[1]) 


def p_call_functions(p):
    '''call_functions : FUNCTION_NAME OPEN_CIRC_BR variables CLOSE_CIRC_BR'''

def p_new_variable(p):
    '''new_variable : TYPE_INT multispace VARIABLE OPERATOR_ASSIGNMENT NUMBER
                    | TYPE_STRING multispace VARIABLE OPERATOR_ASSIGNMENT QUOT STRING QUOT'''
    if len(p) == 6 :
        print(p[5])
    else :
        print(p[5:8])


def p_unification(p):
    '''unification : OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     AND         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     OR          OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     XOR         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     COMPARISON  OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR'''
    print("hello")
    # тут нужно проверять, что вообще есть такая переменная, а потом вызывать

def p_change_variable(p):
    '''change_variable : DOLLAR VARIABLE EQUAL NUMBER
                       | DOLLAR VARIABLE EQUAL QUOT STRING QUOT
                       | DOLLAR VARIABLE EQUAL VARIABLE'''

def p_multispace(p):
    '''multispace : SPACE multispace
                  | SPACE'''
    if len(p) == 3 :
        p[0] = 1 + p[2]
    else:
        p[0] = 1

def p_error(p):
  print("Syntax error", p)


def main(file_in):
    parser = yacc.yacc()
    file_in = open(sys.argv[1], 'r')
    sys.stdout = open(sys.argv[1] + ".out", "w")
    print(parser.parse(file_in.read()))

main(sys.argv[1])