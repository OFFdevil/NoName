from re import L
import ply.yacc as yacc
import ply.lex as lex
import sys
import pydot
from random import randint
from lex1 import tokens, run_lex

graph = pydot.Dot("my_graph", graph_type="graph", bgcolor = "white")
draw_picture = 1

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
stack = []
count = 1
count_vertex = "1"
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
    # вот в этой функции нужно перепроверить, что она нормально всё делает!!!


def p_main(p):
    ''' main : MAIN or_and'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label="MAIN"))
    size = len(stack)
    for i in range(0, size) :
        graph.add_edge(pydot.Edge(count_vertex, stack[-1], color="blue"))
        stack.pop()
        

def p_or_and(p):
    '''or_and : multispace main_functions LOGICAL_OR main_functions SEMICOLON or_and
              | multispace main_functions SEMICOLON or_and
              | '''
    # тут походу нужно вызывать одну из двух фукнци, если logacal_or -> точнее сохранять только одну
    global count_vertex
    count_vertex += "1"
    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label="LOGICAL_OR"))
        print("len stack = ",len(stack))
        print("-p[6] -1 = ",-p[6]-1)
        first = stack[-p[6] - 1]
        del stack[-p[6] - 1]
        print("len stack = ",len(stack))
        print("-p[6] -1 = ",-p[6]-1)
        second = stack[-p[6] - 1]
        del stack[-p[6] - 1]
        # if randint(0,9) % 2 == 0 :
        graph.add_edge(pydot.Edge(count_vertex, first, color="red"))
        # if randint(0,9) % 2 == 0 :
        graph.add_edge(pydot.Edge(count_vertex, second, color="red"))
        stack.append(count_vertex)
    
    if len(p) == 1 :
        p[0] = 0
    elif len(p) == 5 :
        p[0] = 1 + p[4]
    else :
        p[0] = 1 + p[6]
    print("len p[0] = ",p[0])
    

def p_main_functions(p):
    '''main_functions : call_functions
                      | new_variable
                      | unification
                      | change_variable'''


def p_call_functions(p):
    '''call_functions : FUNCTION_NAME OPEN_CIRC_BR parametrs CLOSE_CIRC_BR'''
    global count_vertex
    count_vertex += "1"

    print(count_vertex)
    print("123123",stack)
    graph.add_node(pydot.Node(count_vertex, label=p[1]))
    for i in range(0, p[3]) :
        print("hello ", count_vertex)
        first = stack[-1]
        stack.pop()
        graph.add_edge(pydot.Edge(count_vertex, first, color="black"))
    stack.append(count_vertex)

def p_parametrs(p):
    '''parametrs : multispace OPEN_CIRC_BR CONSTRUCT parametrs CLOSE_CIRC_BR parametrs
                 | multispace OPEN_CIRC_BR CONSTRUCT parametrs CLOSE_CIRC_BR 
                 | multispace VARIABLE parametrs
                 | multispace VARIABLE 
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!
    # кажется можно удалить следующие строчки  multispace OPEN_CIRC_BR COUNSTRUCT parametrs CLOSE_CIRC_BR
    #                                          multispace VARIABLE parametrs
    global count_vertex 
    count_vertex += "1"
    print(stack)
    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        for i in range(0, p[4]) :
            first = stack[-1]
            stack.pop()
            graph.add_edge(pydot.Edge(count_vertex, first, color="green"))
        stack.append(count_vertex)
        p[0] = 1 + p[6]
    elif len(p) == 6 :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        for i in range(0, p[4]) :
            first = stack[-1]
            stack.pop()
            graph.add_edge(pydot.Edge(count_vertex, first, color="green"))
        stack.append(count_vertex)
        p[0] = 1
    elif len(p) == 4 : 
        graph.add_node(pydot.Node(count_vertex, label=p[2]))
        stack.append(count_vertex)
        p[0] = 1 + p[3]
    elif len(p) == 3 :
        graph.add_node(pydot.Node(count_vertex, label=p[2]))
        stack.append(count_vertex)
        p[0] = 1
    elif len(p) == 1 :
        p[0] = 0
    
    print(stack)


        

def p_new_variable(p):
    '''new_variable : TYPE_INT multispace VARIABLE OPERATOR_ASSIGNMENT NUMBER
                    | TYPE_STRING multispace VARIABLE OPERATOR_ASSIGNMENT QUOT STRING QUOT'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[3]))
    count_vertex += "1"
    if len(p) == 6 :
        graph.add_node(pydot.Node(count_vertex, label=p[5]))
    else :
        graph.add_node(pydot.Node(count_vertex, label=p[6]))
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[4]))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-1],color="orange"))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-2],color="orange"))
    stack.append(count_vertex)


def p_unification(p):
    '''unification : OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     AND         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     OR          OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     XOR         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     COMPARISON  OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR'''
    # тут нужно проверять, что вообще есть такая переменная, а потом вызывать сравнение
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[2]))
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[6]))
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[4]))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-1],color="purple"))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-2],color="purple"))
    stack.append(count_vertex)


def p_change_variable(p):
    '''change_variable : DOLLAR VARIABLE EQUAL NUMBER
                       | DOLLAR VARIABLE EQUAL QUOT STRING QUOT
                       | DOLLAR VARIABLE EQUAL VARIABLE'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[2]))
    count_vertex += "1"
    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label=p[5]))
    else :
        graph.add_node(pydot.Node(count_vertex, label=p[4]))
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[3]))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-1],color="brown"))
    graph.add_edge(pydot.Edge(count_vertex, count_vertex[0:-2],color="brown"))
    stack.append(count_vertex)

def p_multispace(p):
    '''multispace : SPACE multispace
                  | SPACE'''
    if len(p) == 3 :
        p[0] = 1 + p[2]
    else:
        p[0] = 1

def p_error(p):
  print("Syntax error", p)
  fuck_mission_failed()


def fuck_mission_failed(): # уже ошибка есть, значит синтаксическое дерево не нужно строить
    global draw_picture
    draw_picture = 0

def main(file_in):
    parser = yacc.yacc()
    file_in = open(sys.argv[1], 'r')
    sys.stdout = open(sys.argv[1] + ".out", "w")
    print(parser.parse(file_in.read()))

    file_out = sys.argv[1] + ".png"
    if draw_picture == 1 :
        graph.write_png(file_out) # рисуем картинку

main(sys.argv[1])