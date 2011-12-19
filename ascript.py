import ply.lex as lex
import ply.yacc as yacc
reserves = {"var" : "VAR", 'if':'IF', 'trace':'TRACE', 'function':'FUNCTION'}
tokens = ['NUMBER', 'ASSIGN', "SEMI", 
"ID", "STRING", 'LBRACE', 'RBRACE',
'LPAREN', 'RPAREN', 'EQUAL', 'COMMA', ]+reserves.values()
t_ASSIGN = r'='
t_SEMI = r';'
t_STRING = r'".*"'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'=='
t_COMMA = r','
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_NUMBER(t):
    r'[+-]{0,1}\d+'
    t.value = int(t.value)
    return t
def t_error(t):
    print "Illegal character '%s' " % t.value[0]
    t.lexer.skip(1)
def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserves.get(t.value, 'ID')
    return t    	
lexer = lex.lex()
"""
data = 'var h = "hello world";'
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok: break
    print tok
"""
