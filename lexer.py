import ply.lex as lex

syntex_words =  [
	'PRINT',
	'NAME',
	'NOT',
	'AND',
	'OR'
]

VARIABLE_TYPES = [
	'STRING',
	'STRUCT',
    'INT',
    'DOUBLE',
    'BOOL',
	'CHAR',
	'VARTYPE',
	'DO',
	'WHILE',
]

tokens = [
	'COMMA',		#,
	'DECREMENT',	#--
	'DIVIDE',		#/
	'DOT',
	'EQUALEQUAL',	#==
	'EQUAL',		#=
	'GREATEREQUAL',	#>=
	'GREATER',		#>
	'INCREMENT',	#++
	'LBRACE',		#{
	'LESSEREQUAL',	#<=
	'LESSER',		#<
	'LPAREN',		#(
	'MINUS',		#-
	'MODULO',		#%
	'MULTIPLY',		#*
	'NOTEQUAL',		#!=
	'PLUS',			#+
	'RBRACE',		#}
	'RPAREN',		#)
	'SEMICOLON',	#;
	'XOR',
]

tokens += syntex_words
tokens += VARIABLE_TYPES
# t_SEMICOLON =   r';'
t_DO = r'DO'
t_WHILE = r'WHILE'
t_XOR = r'\^'
t_EQUALEQUAL = r'=='
t_GREATEREQUAL = r'>='
t_LESSEREQUAL = r'<='
t_NOTEQUAL = r'!='
t_GREATER = r'>'
t_LESSER = r'<'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_NOT = r'NOT'
t_AND = r'AND'
t_OR = r'OR'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_COMMA = r','
t_DOT = r'\.'


t_ignore = ' \t\v\r'


def t_newline(t):
	r'\n'

def t_SEMICOLON(t):
	r';'
	t.lexer.lineno += 1
	return t

def t_VARTYPE(t):
	r'INT|BOOL|STRING|CHAR|DOUBLE'
	return t

def t_BOOL(t):
	r'TRUE|FALSE'
	if t.value == 'TRUE':
		t.value = True
	if t.value == 'FALSE':
		t.value = False
	return t

def t_CHAR(t):
	r'\'[^\'"]\''
	t.value = t.value[1:-1]
	return t

def t_DOUBLE(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_PRINT(t):
	r'PRINT'
	return t


def t_STRUCT(t):
	r'STRUCT'
	return t

def t_NAME(t):
	r'[A-Za-z_][A-Za-z0-9_]*'
	if t.value in (syntex_words+VARIABLE_TYPES):
		t.type = t.value
	return t



def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_error(t):
		print("Instruction " + str(t.lexer.lineno) + "Lexer: Illegal character " + t.value[0] + "<-----")
		t.lexer.skip(1)

lexer = lex.lex()

# lexer.input("1+2.2+FALSE")

# while True:
# 	tok = lexer.token()
# 	if not tok:
# 		break
# 	print(tok)

