import ply.yacc as yacc
import ply.lex as lex
import sys
from lex1 import tokens, run_lex

def p_multispace(p):
    '''multispace : SPACE
                  | SPACE multispace'''
    if len(p) == 3 :
        p[0] = 1 + p[2]
    else:
        p[0] = 1


def p_error(p):
  print("Syntax error", p)

parser = yacc.yacc()

def main(file_in):
    file_in = open(sys.argv[1], 'r')
    sys.stdout = open(sys.argv[1] + ".out", "w")
    print(parser.parse(file_in.read()))


main(sys.argv[1])