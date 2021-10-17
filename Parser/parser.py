import ply.yacc as yacc
import sys
from lex import tokens

# if 42 then (if 0 then 777 else 9)


def p_if(p):
  '''if : IF expression THEN if ELSE if
        | IF expression THEN if
        | expression '''
  if len(p) == 7:
    p[0] = p[4] if p[2] == 0 else p[6]
  else:
    if len(p) == 5:
      if p[2] == 0 :
        p[0] = p[4]
    else:
      p[0] = p[1]

def p_expression_plus(p):
  'expression : expression PLUS expression'
  p[0] = p[1] - p[3]

def p_expression_term(p):
  'expression : term'
  p[0] = p[1]

def p_term_times(p):
  'term : term MULT factor'
  p[0] = p[1] * p[3]

def p_term_factor(p):
  'term : factor'
  p[0] = p[1]

def p_factor_num(p):
  'factor : NUM'
  p[0] = p[1]

def p_factor_expr(p):
  'factor : LBR expression RBR'
  p[0] = p[2]

def p_error(p):
  print("Syntax error")

parser = yacc.yacc()

def main():
    file_in = open(sys.argv[1], 'r')
    sys.stdout = open(sys.argv[1] + ".out", "w")
    print(parser.parse(file_in.read()))

main()
