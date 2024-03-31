import lexer
import ply.yacc as yacc

tokens = lexer.tokens
VARIABLE_TYPES = lexer.VARIABLE_TYPES


precedence = (
		('left', 'OR'),
		('left', 'AND'),
        ('left', 'OROR'),
        ('left', 'ANDAND'),
        ('left', 'EQUALEQUAL', 'NOTEQUAL'),
        ('left', 'LESSER', 'LESSEREQUAL', 'GREATER', 'GREATEREQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
        ('right', 'NOT'),
)


def p_final(p):
    '''final : struct final 
            | do_while final
            | var_dec final
            | var_ass final
            | semi_exp final
            | print final
    '''
    p[0] = [p[1]]+p[2]

def p_final_e(p):
    ''' final : empty
    '''
    p[0] = [p[1]]

def p_struct(p):
    '''struct : STRUCT NAME LBRACE somedata RBRACE SEMICOLON
    '''
    p[0] = (p[1], 'DEF' , p[2] , p[4])

def p_somedata(p):
    '''
    somedata : var_dec somedata
    ''' 
    p[0] = [p[1]] + p[2]

def p_somedata_e(p):
    '''
    somedata : empty
    ''' 
    p[0] = [p[1]]

def p_do_while(p):
    '''
    do_while : DO LBRACE final RBRACE WHILE LPAREN exp RPAREN SEMICOLON
    '''
    p[0] = ('DO_WHILE', p[7] ,p[3])

def p_print(p):
    '''
        print : PRINT LPAREN toprint RPAREN SEMICOLON
    '''
    p[0] = (p[1] , p[3])

def p_toprint(p):
    '''
        toprint : exp
    '''
    p[0] = p[1]

def p_toprint_rec(p):
    ''' 
    toprint : exp COMMA toprint
    '''
    p[0] = ('PRINT' , p[1],('PRINT',p[3]))

def p_new_var_dec(p):
    '''
    var_dec :  VARTYPE var_ass 
    '''
    p[0] = ('INI', p[1],p[2])

def p_struct_var_dec(p):
    '''
    var_dec :  NAME NAME SEMICOLON  
    '''
    p[0] = ('STRUCT', 'INI', p[1],p[2])

def p_new_var_dec_empty(p):
    '''
    var_dec :  VARTYPE NAME SEMICOLON
    '''
    p[0] = ('INI_EMPTY', p[1],p[2])



def p_var_ass(p):
    '''
    var_ass : NAME EQUAL exp SEMICOLON
            
    '''
    p[0] = (p[2], p[1],p[3])


def p_exp(p):
    '''exp :    exp DIVIDE exp
            |   exp MULTIPLY exp
            |   exp PLUS exp
            |   exp MINUS exp
            |   exp XOR exp
            |   exp LESSER exp
            |   exp GREATER exp
            |   exp LESSEREQUAL exp
            |   exp GREATEREQUAL exp
            |   exp EQUALEQUAL exp
            |   exp NOTEQUAL exp
            |   exp AND exp
            |   exp OR exp
            |   exp MODULO exp
    '''
    p[0] = (p[2],p[1],p[3])


def p_exp_NOT(p):
    '''
    exp : NOT exp
    '''
    p[0] = (p[1],p[2])
    
def p_exp_inc(p):
    '''
    semi_exp : NAME INCREMENT SEMICOLON
    '''
    p[0] = ('=' , p[1] , ('+' ,('NAME', p[1]) , 1 ))

def p_exp_prenth(p):
    '''
    exp : LPAREN exp RPAREN
    '''
    p[0] = p[2]
def p_exp_dec(p):
    '''
    semi_exp : NAME DECREMENT SEMICOLON
    '''
    p[0] = ('=', p[1] , ('-' ,('NAME', p[1]) ,1 ))




def p_struct_get_var_exp(p):
    '''
    exp : NAME DOT NAME
    '''
    p[0] = ('STRUCT' , 'NAME' , p[1],p[3])


def p_var_exp(p):
    '''
    exp : NAME
    '''
    p[0] = ('NAME' , p[1])



def p_struct_val_exp(p):
    '''
    semi_exp : NAME DOT NAME SEMICOLON
    '''
    p[0] = ('STRUCT','NAME' , p[1] , p[3])


def p_struct_val_ini_exp(p):
    '''
    semi_exp : NAME DOT NAME EQUAL exp SEMICOLON
    '''
    p[0] = ('STRUCT','=' , p[1] , p[3],p[5])

def p_exp_var(p):
    '''
    exp : INT
        | DOUBLE
        | STRING
        | BOOL
        | CHAR
    '''
    p[0] = p[1]

def p_empty(p):
    '''empty : 
    '''
    p[0] = None

def p_error(p):
    print("Syntax error in input!")
    print(p)


# variables = {}

# def run(tree):
#     global variables
#     print(tree)
#     if type(tree) == tuple:
#         if tree[0] == '+':
#             return run(tree[1]) + run(tree[2])
#         elif tree[0] == '-':
#             return run(tree[1]) - run(tree[2])
#         elif tree[0] == '*':
#             return run(tree[1]) * run(tree[2])
#         elif tree[0] == '/':
#             val = run(tree[2])
#             if val:
#                 return run(tree[1]) / val
#             else:
#                 print("Divide by Zero ERROR")
#         elif tree[0] == '%':
#             return run(tree[1]) % run(tree[2])
#         elif tree[0] == '^':
#             return run(tree[1]) ^ run(tree[2])
#         elif tree[0] == '<':
#             return run(tree[1]) < run(tree[2])
#         elif tree[0] == '>':
#             return run(tree[1]) > run(tree[2])
#         elif tree[0] == '<=':
#             return run(tree[1]) <= run(tree[2])
#         elif tree[0] == '>=':
#             return run(tree[1]) >= run(tree[2])
#         elif tree[0] == '==':
#             return run(tree[1]) == run(tree[2])
#         elif tree[0] == '!=':
#             return run(tree[1]) != run(tree[2])
#         elif tree[0] == 'AND':
#             return run(tree[1]) and run(tree[2])
#         elif tree[0] == 'OR':
#             return run(tree[1]) or run(tree[2])
#         elif tree[0] == 'NOT':
#             return ~run(tree[1])
#         elif tree[0] == 'PRINT':
#             if type(tree[1]) == tuple and tree[1][0] == 'PRINT':
#                 print(run(tree[1][1]),' ',end = '')
#                 return run(tree[1][2])
#             return print(run(tree[1]))
#         elif tree[0] == 'INI':
#             if tree[1] not in VARIABLE_TYPES:
#                 print("Variable type Unknown")
#                 return "Error"
#             elif tree[2][1] in variables.keys():
#                 print("Variable Already Declared")
#                 return "Error"
#             val = run(tree[2][2])
#             if tree[1] == 'INT' and type(val) != int:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if tree[1] == 'DOUBLE' and type(val) != float:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if tree[1] == 'STRING' and type(val) != str:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if tree[1] == 'BOOL' and type(val) != bool:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             variables[tree[2][1]] = {}
#             variables[tree[2][1]][1] = tree[1]
#             variables[tree[2][1]][0] = val
#             print(variables)
#         elif tree[0] == '=':
#             if tree[1] not in variables.keys():
#                 print("Variable not Declared")
#                 return "Error"
#             val = run(tree[2])
#             typ = variables[tree[1]][1]
#             if typ == 'INT' and type(val) != int:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if typ == 'DOUBLE' and type(val) != float:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if typ == 'STRING' and type(val) != str:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             if typ == 'BOOL' and type(val) != bool:
#                 print("Variable Type MISMATCH")
#                 return "Error"
#             variables[tree[1]][0] = val
#         elif tree[0] == 'NAME':
#             if tree[1] not in variables.keys():
#                 print("There is no such variable" , tree[1])
#                 return "Error"
#             return variables[tree[1]][0]


            
#     else:
#         return tree


parser = yacc.yacc()



# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
#     parser.parse(s,lexer=lexer)