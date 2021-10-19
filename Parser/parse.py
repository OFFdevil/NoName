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
    def __init__(self, name_, hash_parametrs_, body_):
        self.name = name_
        self.hash_parametrs = hash_parametrs_
        self.body = body_


class Program: 
    def __init__(self):
        self.variables = []
        self.functions = []

##############################
main_program = Program()

modul = 1000000007
simple_numeric_struct = 83
simple_numeric_variable = 883
hash_parametrs_global = 1
count = 1

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
    # проверка на то, что структура 
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
        check_various_variables_name.append(p[2])
    elif len(p) == 7 :
        hash_parametrs_global = (hash_parametrs_global * simple_numeric_struct) % modul
    count += 1

def p_main(p):
    ''' main : MAIN comment_or_empty or_and'''
    global count_vertex
    count_vertex += "1"
    graph.add_node(pydot.Node(count_vertex, label="MAIN"))
    size = len(stack)
    for i in range(0, size) :
        graph.add_edge(pydot.Edge(count_vertex, stack[-1], color="blue", dir="forward"))
        stack.pop()
        

def p_or_and(p):
    '''or_and : multispace main_functions LOGICAL_OR main_functions SEMICOLON comment_or_empty or_and
              | multispace main_functions SEMICOLON comment_or_empty or_and
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
                      | new_variable
                      | unification
                      | change_variable'''


def p_call_functions(p):
    '''call_functions : FUNCTION_NAME OPEN_CIRC_BR parametrs CLOSE_CIRC_BR'''
    global count_vertex
    count_vertex += "1"

    graph.add_node(pydot.Node(count_vertex, label=p[1]))
    for i in range(0, p[3]) :
        first = stack[-1]
        stack.pop()
        graph.add_edge(pydot.Edge(count_vertex, first, color="black"))
    stack.append(count_vertex)

def p_parametrs(p):
    '''parametrs : multispace OPEN_CIRC_BR CONSTRUCT parametrs CLOSE_CIRC_BR parametrs
                 | multispace VARIABLE parametrs
                 | ''' # смотреть сюда, если недоумеваете, почему поставили пробел после названии функции и всё поламалось!
    # кажется можно удалить следующие строчки  multispace OPEN_CIRC_BR COUNSTRUCT parametrs CLOSE_CIRC_BR
    #                                          multispace VARIABLE parametrs
    global count_vertex 
    count_vertex += "1"
    variable_is_declared = 0

    # проверка, что данная переменная уже объявлена
    if len(p) == 4 :
        for i in range(0,len(main_program.variables)):
            if p[2] == main_program.variables[i] :
                variable_is_declared = 1
                break

        if variable_is_declared == 0 :
            fuck_mission_failed()
            print("Variable",p[2]," doesn't exist")

    if len(p) == 7 :
        graph.add_node(pydot.Node(count_vertex, label="struct"))
        for i in range(0, p[4]) :
            first = stack[-1]
            stack.pop()
            graph.add_edge(pydot.Edge(count_vertex, first, color="green"))
        stack.append(count_vertex)
        p[0] = 1 + p[6]
    elif len(p) == 4 : 
        graph.add_node(pydot.Node(count_vertex, label=p[2]))
        stack.append(count_vertex)
        p[0] = 1 + p[3]
    elif len(p) == 1 :
        p[0] = 0

        

def p_new_variable(p):
    '''new_variable : TYPE_INT multispace VARIABLE OPERATOR_ASSIGNMENT NUMBER
                    | TYPE_STRING multispace VARIABLE OPERATOR_ASSIGNMENT QUOT STRING QUOT'''
    global count_vertex

    # проверка, что данная переменная уже объявлена
    variable_is_declared = 0
    for i in range(0,len(main_program.variables)):
       if p[3] == main_program.variables[i] :
            variable_is_declared = 1
            break

    if variable_is_declared == 1 :
        fuck_mission_failed()
        print("Variable",p[3]," has already existed!")

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

    # добавляем переменную
    main_program.variables.append(p[3])


def p_unification(p):
    '''unification : OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     AND         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     OR          OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     XOR         OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR
                   | OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR     COMPARISON  OPEN_CIRC_BR VARIABLE CLOSE_CIRC_BR'''
    # тут нужно проверять, что вообще есть такая переменная, а потом вызывать сравнение
    global count_vertex

    # проверка, что данная переменная уже объявлена
    variable_is_declared = 0
    for i in range(0,len(main_program.variables)):
       if p[2] == main_program.variables[i] :
            variable_is_declared = 1
            break

    if variable_is_declared == 0 :
        fuck_mission_failed()
        print("Variable",p[2]," doesn't exist")
    
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

    # проверка, что данная переменная уже объявлена
    variable_is_declared = 0
    for i in range(0,len(main_program.variables)):
       if p[2] == main_program.variables[i] :
            variable_is_declared = 1
            break

    if variable_is_declared == 0:
        fuck_mission_failed()
        print("Variable",p[2]," doesn't exist")

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


def p_comment_or_empty(p):
    '''comment_or_empty : DIVIDE DIVIDE COMMENT_ONELINE comment_or_empty
                        | DIVIDE DIVIDE comment_or_empty
                        | '''
    pass

def p_multispace(p):
    '''multispace : SPACE multispace
                  | SPACE'''
    if len(p) == 3 :
        p[0] = 1 + p[2]
    else:
        p[0] = 1

# переделать, хорошо бы, если можно было ещё пробелы перед // ставить. Идеи: ставить вместо пробелов "_" будет нормально работать, но выглядеть...хм, а кому это важно)
# def p_comment_space(p):
#     '''comment_space : SPACE comment_space
#                      | '''
#     pass

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