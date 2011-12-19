import ply.yacc as yacc
import struct
from ascript import tokens, lexer
def p_statementlist(p):
    'statementlist : statementlist statement'
    p[0] = {'kind':'list', 'data': p[1].get('data')+[p[2]]}
def p_statement_var_dec(p):
    'statement : VAR ID ASSIGN expression SEMI'
    p[0] = {'kind':'declare', 'var':p[2], 'exp':p[4]}
def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMI'
    p[0] = {'kind':'assign', 'var':p[1], 'exp':p[3]}
def p_block(p):
    'block : LBRACE statementlist RBRACE'
    p[0] = {'kind': 'block', 'data':p[2]}
def p_argument_list(p):
    'argumentlist : argumentlist COMMA ID'
    p[0] = {'kind':'argument', 'data':p[1].get('data')+[p[3]]}
def p_argument_empty(p):
    'argumentlist : empty'
    p[0] = {'kind':'argument', 'data':[]}
def p_argument_one(p):
    'argumentlist : ID'
    p[0] = {'kind':'argument', 'data':[p[1]]}
def p_function(p):
    'statement : FUNCTION ID LPAREN argumentlist RPAREN LBRACE statementlist RBRACE'
    p[0] = {'kind':'function', 'name':p[2], 'arg': p[4], 'body':p[7]}
def p_block_one(p):
    'block : statement'
    p[0] = {'kind':'block', 'data':[p[1]]}
def p_cmp(p):
    'cmp : EQUAL'
    p[0] = p[1]
def p_condition(p):
    'condition : expression cmp expression'
    p[0] = {'kind':'condition', 'exp1':p[1], 'cmp':p[2], 'exp2':p[3]}
def p_statement_if(p):
    'statement : IF LPAREN condition RPAREN block'
    p[0] = {'kind':'if', 'con':p[3], 'block':p[5]}
def p_statementlist_empty(p):
    'statementlist : empty'
    p[0] = {'kind':'list', 'data':[]}
def p_expression_str(p):
    'expression : STRING'
    p[0] = {'kind' : 'string', 'data': p[1]}
    #print p[0]
def p_expression_num(p):
    'expression : NUMBER'
    p[0] = {'kind' : 'number', 'data': p[1]}
    #print p[0]
def p_expression_id(p):
    'expression : ID'
    p[0] = {'kind' : 'number', 'data':p[1]}
def p_empty(p):
    'empty :'
    pass
def p_statement_trace(p):
    'statement : TRACE LPAREN expression RPAREN SEMI'
    p[0] = {'kind':'trace', 'exp': p[3]}

def p_error(p):
    global lexer
    print 'syntax error', p
def p_realarg_term(p):
    'realarg : expression'
    p[0] = {'kind':'realarg', 'data':[p[1]]}
def p_realarg_list(p):
    'realarg : realarg COMMA expression'
    p[0] = {'kind':'realarg', 'data':p[1].get('data')+[p[3]]}
def p_realarg_empty(p):
    'realarg : empty'
    p[0] = {'kind':'realarg', 'data':[]}
def p_fun_call(p):
    'expression : ID LPAREN realarg RPAREN'
    p[0] = {'kind':'funcall', 'name':p[1], 'arg':p[3].get('data')}
def p_statement_exp(p):
    'statement : expression SEMI'
    p[0] = p[1];
data = file('test.as').read()
parser = yacc.yacc()
result = parser.parse(data)
def outputTab(n):
    i = 0
    while i < n:
        print '\t',
        i += 1
def tranverse(root, stack):
    resultLine = ""
    if root.get('kind') == 'declare':
        if root.get('exp').get('kind') == 'string':
            outputTab(stack)
            print root.get('var'), '=', root.get('exp').get('data')
        elif root.get('exp').get('kind') == 'number':
            outputTab(stack)
            print root.get('var'), '=', root.get('exp').get('data')
    elif root.get('kind') == 'assign':
        outputTab(stack)
        #print 'global', root.get('var')
        #outputTab(stack)
        print root.get('var'), '=', root.get('exp').get('data')
    elif root.get('kind') == 'list':
        for s in root.get('data'):
            tranverse(s, stack)
    elif root.get('kind') == 'if':
        outputTab(stack)
        exp1 = root.get('con').get('exp1').get('data')
        exp2 = root.get('con').get('exp2').get('data')
        cmps = root.get('con').get('cmp')
        print 'if', exp1, cmps, exp2, ':'
        tranverse(root.get('block'), stack+1)
    elif root.get('kind') == 'block':
        for s in root.get('data'):
            tranverse(s, stack)
    elif root.get('kind') == 'trace':
        outputTab(stack)
        print 'print', root.get('exp').get('data')
    elif root.get('kind') == 'function':
        outputTab(stack) 
        print root.get('arg') 
        print 'def', root.get('name'), '(',
        i = 0
        l = len(root.get('arg').get('data'))
        for a in root.get('arg').get('data'):
            print a, 
            if i < (l-1):
                print ',',
            i += 1
        print '):'
        tranverse(root.get('body'), stack+1)
        if len(root.get('body').get('data')) == 0:
            outputTab(stack+1) 
            print 'pass'
    elif root.get('kind') == 'funcall':
        pass
        """
        outputTab(stack)        
        res = root.get('name')+'('
        for e in root.get('arg'):
            res += str(e)+','
        res = res[:len(res)-1]
        res += ')'
        print res
        """
tranverse(result, 0)
