import ply.lex as lex
import sys


reserved = {
    'main': 'MAIN',
    'int': 'TYPE_INT',
    'string': 'TYPE_STRING',
    'def': 'FUNCTION_DEFINITION',
    'struct': 'CONSTRUCT'  
}

tokens = [
             'BODY',
             'COMMENT_ONELINE',
             'NUMBER',
             'STRING',
             'FUNCTION',
             'FUNCTION_NAME',
             'VARIABLE',
             'RESERVED_NAME',
             
             'OPERATOR_ASSIGNMENT',
             'DIVIDE',
             'OPEN_CIRC_BR',
             'CLOSE_CIRC_BR',
             'OPEN_SHAPED_BR',
             'CLOSE_SHAPED_BR',
             'COMPARISON',
             'NOT',
             'AND',
             'OR',
             'XOR',
             'COLON',
             'SPACE',
             'EQUAL',
             'QUOT',
             'SEMICOLON',
             'LOGICAL_OR',
             'COMMENT_ONE_LINE',
             'DOLLAR'
         ] + list(reserved.values())

t_OPERATOR_ASSIGNMENT = r'\:='
t_DIVIDE = r'\/'
t_OPEN_CIRC_BR = r'\('
t_CLOSE_CIRC_BR = r'\)'
t_OPEN_SHAPED_BR = r'\{'
t_CLOSE_SHAPED_BR = r'\}'   
t_COMPARISON = r'\=\='
t_NOT = r'\!'
t_AND = r'\&&'
t_OR = r'\|\|'
t_XOR = r'\^'
t_COLON = r'\:'
t_SPACE = r'\s' 
t_EQUAL = r'\='
t_QUOT = r'\"'
t_SEMICOLON = r'\;'
t_LOGICAL_OR = r'\,'
t_DOLLAR = r'\$'

states = (
   ('body','exclusive'),
)

def t_body(t):
    r'(?<=\n\{)'
    t.lexer.code_start = t.lexer.lexpos        
    t.lexer.level = 1                          
    t.lexer.begin('body')
 
def t_body_lbrace(t):     
    r'\{'
    t.lexer.level +=1                

def t_body_rbrace(t):
    r'(?=\})'
    t.lexer.level -=1
 
    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
        t.type = "BODY"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')           
        return t

def t_body_all(t):
    r'[^(\{|\})]+'
 
t_body_ignore = "\t"
 
def t_body_error(t):
    t.lexer.skip(1)


def t_COMMENT_ONELINE(t):
    r'(?<=//)([^(\n)]|\\.)+(?=\n)'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'(?<=\")[A-Za-z0-9]+(?=\")'
    return t

def t_FUNCTION_NAME(t):
    r'FUNC([a-z]+)'
    t.type = reserved.get(t.value, "FUNCTION_NAME")
    return t

def t_VARIABLE(t):
    r'[A-Z]([a-z]*)'
    t.type = reserved.get(t.value, "VARIABLE")
    return t

def t_RESERVED_NAME(t):
    r'(main|int|string|def|struct)'
    t.type = reserved.get(t.value, 'WTF')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex() # https://stackoverflow.com/questions/25712334/ply-lex-and-yacc-issues

def run_lex(file_name):

    lexer.input(open(file_name, 'r').read())
    sys.stdout = open(file_name + '.o', 'w')

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

run_lex(sys.argv[1])