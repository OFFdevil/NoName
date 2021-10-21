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


class Program: 
    def __init__(self):
        self.functions = []

##############################
main_program = Program()

modul = 1000000007
simple_numeric_struct = 83
simple_numeric_variable = 883
hash_parametrs_global = 1
count = 1
spaces = 0

check_various_variables_name = []
stack = []
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
    global hash_parametrs_global, count
    # тут проверяем, что все параметры имеют разное имя
    check_various_variables_name.sort()
    for i in range(1, len(check_various_variables_name)) :
        if(check_various_variables_name[i-1] == check_various_variables_name[i]) :
            fuck_mission_failed()
            print("Function: name=",p[3],"has already had parametr with this name!")
            break
    check_various_variables_name.clear()
    # проверка на то, что ещё нет такой функции с таким набором параметров
    for i in range(0, len(main_program.functions)) :
        if ((main_program.functions[i].name == p[3]) & (main_program.functions[i].hash_parametrs == hash_parametrs_global)) :
            fuck_mission_failed()
            print("Function: name=",p[3],"has already created with such parametrs!")
            break
    # пытаемся добавить функцию (если уже какая-то ошибка была, то новую функцию не будем добавлять)
    if draw_picture :
        function = Function(p[3], hash_parametrs_global, p[6])
        main_program.functions.append(function)  
    hash_parametrs_global = 1
    count = 1


def p_variables(p):
    '''variables : multispace OPEN_CIRC_BR CONSTRUCT variables CLOSE_CIRC_BR variables
                 | multispace VARIABLE variables
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!
    global hash_parametrs_global, count
    if len(p) == 4 : 
        hash_parametrs_global = (hash_parametrs_global + count * simple_numeric_variable) % modul
    elif len(p) == 7 :
        hash_parametrs_global = (hash_parametrs_global * simple_numeric_struct) % modul
    count += 1

    if len(p) == 4 :
        check_various_variables_name.append(p[2])




def p_main(p):
    ''' main : MAIN comment_or_empty or_and'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label="MAIN"))
    for i in range(0, len(stack)) :
        graph.add_edge(pydot.Edge(count_vertex, stack[-1], color="blue", dir="forward"))
        stack.pop()
        

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
                graph.add_edge(pydot.Edge(count_vertex, first, color="red"))
                graph.add_edge(pydot.Edge(count_vertex, second, color="red", style="dotted"))
            else :
                graph.add_edge(pydot.Edge(count_vertex, first, color="red", style="dotted"))
                graph.add_edge(pydot.Edge(count_vertex, second, color="red"))
        elif ((rand1 == 1) & (rand2 == 0)) :
            graph.add_edge(pydot.Edge(count_vertex, first, color="red"))
            graph.add_edge(pydot.Edge(count_vertex, second, color="red", style="dotted"))
        elif ((rand1 == 0) & (rand2 == 1)) :
            graph.add_edge(pydot.Edge(count_vertex, first, color="red", style="dotted"))
            graph.add_edge(pydot.Edge(count_vertex, second, color="red"))
        elif ((rand1 == 1) & (rand2 == 1)) :
            graph.add_edge(pydot.Edge(count_vertex, first, color="red"))
            graph.add_edge(pydot.Edge(count_vertex, second, color="red"))
        stack.append(count_vertex)
    
    if len(p) == 2 :
        p[0] = 0
    elif len(p) == 6 :
        p[0] = 1 + p[5]
    else :
        p[0] = 1 + p[7]


def p_main_functions(p):
    '''main_functions : call_functions
                      | unification'''

def p_call_functions(p):
    '''call_functions : FUNCTION_NAME OPEN_CIRC_BR parametrs CLOSE_CIRC_BR'''
    
    global count_vertex, hash_parametrs_global, count
    count_vertex += "1"

    graph.add_node(pydot.Node(count_vertex, label=p[1]))
    strstr = ""
    for i in range(0, len(p[3])) :
        if (p[3][i] == "|"):
            graph.add_edge(pydot.Edge(count_vertex, strstr, color="green"))
            strstr = ""
        else :
            strstr += p[3][i]
    stack.append(count_vertex)
    
    check = 0
    for i in range(0, len(main_program.functions)) :
        if((main_program.functions[i].name == p[1]) & (main_program.functions[i].hash_parametrs == hash_parametrs_global)) :
            check = 1   
            break       
    if check == 0 :
        fuck_mission_failed()
        print("Function: name=",p[1],"didn't call with this parametrs!")
    hash_parametrs_global = 1
    count = 1      

def p_parametrs(p):
    '''parametrs : multispace OPEN_CIRC_BR CONSTRUCT parametrs CLOSE_CIRC_BR parametrs
                 | multispace VARIABLE parametrs
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!    
    global count_vertex 
    count_vertex += "1"

    global hash_parametrs_global, count
    if len(p) == 4 : 
        hash_parametrs_global = (hash_parametrs_global + count * simple_numeric_variable) % modul
    elif len(p) == 7 :
        hash_parametrs_global = (hash_parametrs_global * simple_numeric_struct) % modul
    count += 1

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
    '''unification : OPEN_CIRC_BR atom CLOSE_CIRC_BR     AND         OPEN_CIRC_BR atom CLOSE_CIRC_BR
                   | OPEN_CIRC_BR atom CLOSE_CIRC_BR     OR          OPEN_CIRC_BR atom CLOSE_CIRC_BR
                   | OPEN_CIRC_BR atom CLOSE_CIRC_BR     XOR         OPEN_CIRC_BR atom CLOSE_CIRC_BR
                   | OPEN_CIRC_BR atom CLOSE_CIRC_BR     COMPARISON  OPEN_CIRC_BR atom CLOSE_CIRC_BR'''
    
    global count_vertex
    
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label=p[4]))
    graph.add_edge(pydot.Edge(count_vertex, p[2],color="purple"))
    graph.add_edge(pydot.Edge(count_vertex, p[6],color="purple"))
    stack.append(count_vertex)

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
    p[0] = count_vertex
    

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