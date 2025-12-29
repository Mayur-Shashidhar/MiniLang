import ply.lex as lex

tokens = (
    'EQUALS',
    'DEF', 'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'RETURN', 'PLUS',
    'FOR', 'IN', 'LBRACKET', 'RBRACKET', 'RANGE',
    'INT_TYPE', 'FLOAT_TYPE', 'STR_TYPE', 'BOOL_TYPE', 'LIST_TYPE',
    'IF', 'WHILE',
    'NAME', 'NUMBER', 'FLOAT', 'BOOLEAN', 'STRING',
)

reserved = {
   'def'   : 'DEF',
   'return': 'RETURN',
   'for'   : 'FOR',
   'in'    : 'IN',
   'range' : 'RANGE',
   'True'  : 'BOOLEAN',
   'False' : 'BOOLEAN',
   'int'   : 'INT_TYPE',
   'float' : 'FLOAT_TYPE',
   'str'   : 'STR_TYPE',
   'bool'  : 'BOOL_TYPE',
   'list'  : 'LIST_TYPE',
   'if'    : 'IF',
   'while' : 'WHILE'
}

t_EQUALS   = r'='
t_PLUS     = r'\+'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COLON    = r':'
t_COMMA    = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)
    return t

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"Lexer: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
