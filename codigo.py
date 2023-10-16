import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EXP',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EXP     = r'\^'
t_NUMBER  = r'\d+'

t_ignore  = ' \t'

lexer = lex.lex()

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_exp(p):
    'factor : factor EXP unary'
    p[0] = p[1] ** p[3]

def p_factor_unary(p):
    'factor : unary'
    p[0] = p[1]

def p_unary(p):
    'unary : MINUS unary'
    p[0] = -p[2]

def p_unary_number(p):
    'unary : NUMBER'
    p[0] = int(p[1])

def p_unary_expr(p):
    'unary : LPAREN expression RPAREN'
    p[0] = p[2]

def p_unary_implicit_mult(p):
    'unary : NUMBER LPAREN expression RPAREN'
    p[0] = int(p[1]) * p[3]

def p_error(p):
    print(f"Error de sintaxis en la entrada {p}")

parser = yacc.yacc()

while True:
    try:
        s = input('calcular: ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
