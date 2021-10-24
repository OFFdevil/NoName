from re import L
import ply.yacc as yacc
import ply.lex as lex
import sys
import pydot
from random import randint
from lex import tokens, run_lex

graph = pydot.Dot("my_graph", graph_type="graph", bgcolor = "white")
draw_picture = 1

class Function:
    def __init__(self, name_, hash_parametrs_, body_):
        self.name = name_
        self.hash_parametrs = hash_parametrs_
        self.body = body_

class CallFunction:
    def __init__(self, space_, name_vertex_):
        self.space = space_
        self.name_vertex = name_vertex_

class Program: 
    def __init__(self):
        self.functions = []

##############################
main_program = Program()

modul = 1000000007
simple_numeric_struct = 83
simple_numeric_variable = 883
spaces = 0

stack = []
stack_calls = []
count_vertex = "1"
##############################

precedence = (
     ('left', 'FUNCTION_DEFINITION', 'SPACE', "FUNCTION_NAME", "OPEN_SHAPED_BR", "BODY", "CLOSE_SHAPED_BR"),
)

start = 'functions'

def p_functions(p):
    '''functions : comment_or_empty main
                 | comment_or_empty functions_helper comment_or_empty functions'''

def p_functions_helper(p):
    '''functions_helper : FUNCTION_DEFINITION multispace FUNCTION_NAME variables comment_or_empty OPEN_SHAPED_BR BODY CLOSE_SHAPED_BR'''
    function = Function(p[3], 0, 0)
    main_program.functions.append(function)  


def p_variables(p):
    '''variables : multispace OPEN_CIRC_BR CONSTRUCT variables CLOSE_CIRC_BR variables
                 | multispace VARIABLE variables
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!

def p_main(p):
    ''' main : MAIN comment_or_empty or_and'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label="MAIN"))
    stack_calls.reverse() # развернули список
    for i in range(0,len(stack_calls)) :
        print(stack_calls[i].space)
    while len(stack_calls) > 0 :
        deleted = []
        id = 1
        if len(stack_calls) == 1 :
            print("1запускаем отношение в строке с количеством пробелов = ", stack_calls[0].space)
            graph.add_edge(pydot.Edge(count_vertex, stack_calls[0].name_vertex, color="blue", dir="forward"))
            stack_calls.pop()
            break
        while id < len(stack_calls):
            if stack_calls[id - 1].space >= stack_calls[id].space :
                deleted.append(id - 1)
                break
            id += 1
            if id == len(stack_calls) :
                print("2запускаем отношение в строке с количеством пробелов = ", stack_calls[id - 1].space)
                graph.add_edge(pydot.Edge(count_vertex, stack_calls[id - 1].name_vertex, color="blue", dir="forward"))
                stack_calls.pop()
                break

        while id < len(stack_calls) :
            if stack_calls[id - 1].space == stack_calls[id].space :
                if id + 1 < len(stack_calls) :
                    if stack_calls[id].space >= stack_calls[id + 1].space :
                        deleted.append(id)
                else :
                    deleted.append(id)
                id += 1
            else :
                break

        deleted.reverse()
        for i in range(0, len(deleted)) :
            print("3запускаем отношение в строке с количеством пробелов = ", stack_calls[deleted[i]].space)
            graph.add_edge(pydot.Edge(count_vertex, stack_calls[deleted[i]].name_vertex, color="blue", dir="forward"))
            del stack_calls[deleted[i]] # удалили элемент
        

def p_or_and(p):
    '''or_and : space_for_functions main_functions LOGICAL_OR main_functions SEMICOLON comment_or_empty or_and
              | space_for_functions main_functions SEMICOLON comment_or_empty or_and
              | comment_or_empty'''
    # тут походу нужно вызывать одну из двух фукнци, если logacal_or -> точнее сохранять только одну
    global count_vertex
    count_vertex += "1"
    if len(p) == 8 :
        graph.add_node(pydot.Node(count_vertex, label="LOGICAL_OR"))
        first = stack[-p[7] - 1]
        del stack[-p[7] - 1]
        second = stack[-p[7] - 1]
        del stack[-p[7] - 1]
        rand1 = randint(0,9) % 2
        rand2 = randint(0,9) % 2
        # вот тут я немножко рандомчика добавил)
        if ((rand1 == 0) & (rand2 == 0)) :
            rand3 = randint(0,9) % 2
            if rand3 == 0:
                graph.add_edge(pydot.Edge(count_vertex, first.name_vertex, color="red"))
                graph.add_edge(pydot.Edge(count_vertex, second.name_vertex, color="red", style="dotted"))
            else :
                graph.add_edge(pydot.Edge(count_vertex, first.name_vertex, color="red", style="dotted"))
                graph.add_edge(pydot.Edge(count_vertex, second.name_vertex, color="red"))
        elif ((rand1 == 1) & (rand2 == 0)) :
            graph.add_edge(pydot.Edge(count_vertex, first.name_vertex, color="red"))
            graph.add_edge(pydot.Edge(count_vertex, second.name_vertex, color="red", style="dotted"))
        elif ((rand1 == 0) & (rand2 == 1)) :
            graph.add_edge(pydot.Edge(count_vertex, first.name_vertex, color="red", style="dotted"))
            graph.add_edge(pydot.Edge(count_vertex, second.name_vertex, color="red"))
        elif ((rand1 == 1) & (rand2 == 1)) :
            graph.add_edge(pydot.Edge(count_vertex, first.name_vertex, color="red"))
            graph.add_edge(pydot.Edge(count_vertex, second.name_vertex, color="red"))
        stack.append(CallFunction(p[1], count_vertex))
        stack_calls.append(CallFunction(p[1], count_vertex))
    
    if len(p) == 6 :
        stack_calls.append(CallFunction(p[1], p[2]))

    if len(p) == 2 :
        p[0] = 0
    elif len(p) == 6 :
        p[0] = 1 + p[5]
    else :
        p[0] = 1 + p[7]


def p_main_functions(p):
    '''main_functions : call_functions
                      | unification'''
    p[0] = p[1]

def p_call_functions(p):
    '''call_functions : FUNCTION_NAME OPEN_CIRC_BR parametrs CLOSE_CIRC_BR'''
    
    global count_vertex
    count_vertex += "1"

    graph.add_node(pydot.Node(count_vertex, label=p[1]))
    strstr = ""
    for i in range(0, len(p[3])) :
        if (p[3][i] == "|"):
            graph.add_edge(pydot.Edge(count_vertex, strstr, color="green"))
            strstr = ""
        else :
            strstr += p[3][i]
    stack.append(CallFunction(spaces, count_vertex)) # добавляем функцию в стек вызовов
    
    p[0] = count_vertex   

def p_parametrs(p):
    '''parametrs : multispace OPEN_CIRC_BR CONSTRUCT parametrs CLOSE_CIRC_BR parametrs
                 | multispace VARIABLE parametrs
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!    
    global count_vertex 
    count_vertex += "1"
    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        strstr = ""
        for i in range(0, len(p[4])) :
            if (p[4][i] == "|"):
                graph.add_edge(pydot.Edge(count_vertex, strstr, color="green"))
                strstr = ""
            else :
                strstr += p[4][i]
        p[0] = count_vertex + "|" + str(p[6])
    elif len(p) == 4 : 
        graph.add_node(pydot.Node(count_vertex, label=p[2]))
        p[0] = count_vertex + "|" + str(p[3])
    elif len(p) == 1 :
        p[0] = ""    
    


def p_unification(p):
    '''unification : OPEN_CIRC_BR atom CLOSE_CIRC_BR     COMPARISON  OPEN_CIRC_BR atom CLOSE_CIRC_BR'''
    
    global count_vertex
    
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[4]))
    graph.add_edge(pydot.Edge(count_vertex, p[2],color="purple"))
    graph.add_edge(pydot.Edge(count_vertex, p[6],color="purple"))
    stack.append(CallFunction(spaces, count_vertex))
    p[0] = count_vertex
    

def p_atom(p):
    '''atom : OPEN_CIRC_BR CONSTRUCT atom_struct CLOSE_CIRC_BR
            | VARIABLE'''
    global count_vertex
    count_vertex += "1"
    if len(p) == 2 :
        graph.add_node(pydot.Node(count_vertex, label=p[1]))
    else :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        strstr = ""
        for i in range(0, len(p[3])) :
            if (p[3][i] == "|"):
                graph.add_edge(pydot.Edge(count_vertex, strstr, color="green"))
                strstr = ""
            else :
                strstr += p[3][i]    

    p[0] = count_vertex # название вершины передаю

def p_atom_struct(p):
    '''atom_struct : multispace OPEN_CIRC_BR CONSTRUCT atom_struct CLOSE_CIRC_BR atom_struct
                   | multispace VARIABLE atom_struct
                   |'''
    global count_vertex 
    count_vertex += "1"
    
    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        strstr = ""
        for i in range(0, len(p[4])) :
            if (p[4][i] == "|"):
                graph.add_edge(pydot.Edge(count_vertex, strstr, color="green"))
                strstr = ""
            else :
                strstr += p[4][i]
        p[0] = count_vertex + "|" + str(p[6])
    elif len(p) == 4 : 
        graph.add_node(pydot.Node(count_vertex, label=p[2]))
        p[0] = count_vertex + "|" + str(p[3])
    elif len(p) == 1 :
        p[0] = ""  

def p_comment_or_empty(p):
    '''comment_or_empty : DIVIDE DIVIDE COMMENT_ONE_LINE comment_or_empty
                        | DIVIDE DIVIDE comment_or_empty
                        | '''
    pass

def p_space_for_functions(p):
    '''space_for_functions : SPACE multispace
                           | SPACE'''
    global spaces
    if len(p) == 3 :
        p[0] = 1 + p[2]
    else:
        p[0] = 1
    spaces = p[0]

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
    parser.parse(file_in.read())

    file_out = sys.argv[1] + ".png"
    if draw_picture == 1 :
        graph.write_png(file_out) # рисуем картинку

main(sys.argv[1])