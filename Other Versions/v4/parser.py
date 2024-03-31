import lexer
import ply.yacc as yacc

tokens = lexer.tokens
VARIABLE_TYPES = lexer.VARIABLE_TYPES


precedence = (
		('left', 'OR' ),
		('left', 'AND'),
        ('left', 'OROR'),
        ('left', 'ANDAND'),
        ('left', 'EQUALEQUAL', 'NOTEQUAL'),
        ('left', 'LESSER', 'LESSEREQUAL', 'GREATER', 'GREATEREQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
        ('left', 'XOR'),
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

def p_plus(p):
    '''
    exp : PLUS exp
    '''
    p[0] = p[2]

def p_minus(p):
    '''
    exp : MINUS exp
    '''
    p[0] = ('*',-1,p[2])

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



parser = yacc.yacc()

