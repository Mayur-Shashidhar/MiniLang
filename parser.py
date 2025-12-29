import ply.yacc as yacc
from lexer import tokens, lexer

def p_program(p):
    'program : statements'
    pass

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    pass

def p_statement(p):
    '''statement : typed_assign_statement
                 | untyped_assign_statement
                 | func_decl_statement
                 | for_loop_statement
                 | invalid_function_def
                 | expression_statement'''
    p[0] = p[1]

def get_value_type(value):
    if isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, str):
        return 'str'
    else:
        return 'unknown'

def p_typed_assign_statement(p):
    '''typed_assign_statement : data_type NAME EQUALS expression'''
    type_name = p[1]
    var_name = p[2]
    value = p[4]
    
    if type_name == 'int' and not isinstance(value, int):
        print(f"Parser: TYPE ERROR - Cannot assign {type(value).__name__} value '{value}' to int variable '{var_name}'")
        print(f"Parser: Expected an integer value")
    elif type_name == 'float' and not isinstance(value, (int, float)):
        print(f"Parser: TYPE ERROR - Cannot assign {type(value).__name__} value '{value}' to float variable '{var_name}'")
        print(f"Parser: Expected a numeric value")
    elif type_name == 'str' and not isinstance(value, str):
        print(f"Parser: TYPE ERROR - Cannot assign {type(value).__name__} value '{value}' to str variable '{var_name}'")
        print(f"Parser: Expected a string value")
    elif type_name == 'bool' and not isinstance(value, bool):
        print(f"Parser: TYPE ERROR - Cannot assign {type(value).__name__} value '{value}' to bool variable '{var_name}'")
        print(f"Parser: Expected a boolean value (True or False)")
    else:
        print(f"Parsed typed assignment: {type_name} {var_name} = {value}")
    
    p[0] = ('typed_assign', type_name, var_name, value)

def p_untyped_assign_statement(p):
    'untyped_assign_statement : NAME EQUALS expression'
    print(f"Parsed assignment: {p[1]} = {p[3]}")
    p[0] = ('assign', p[1], p[3])

def p_data_type(p):
    '''data_type : INT_TYPE
                 | FLOAT_TYPE
                 | STR_TYPE
                 | BOOL_TYPE
                 | LIST_TYPE'''
    p[0] = p[1]

def p_func_decl_statement(p):
    'func_decl_statement : DEF NAME LPAREN parameters RPAREN COLON suite'
    print(f"Parsed function declaration: {p[2]} with parameters: {p[4]}")
    p[0] = ('func_decl', p[2], p[4], p[7])

def p_parameters(p):
    '''parameters : param_list
                  | empty'''
    p[0] = p[1]

def p_param_list(p):
    '''param_list : param_list COMMA NAME
                  | NAME'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_suite(p):
    'suite : statement'
    p[0] = [p[1]]

def p_for_loop_statement(p):
    'for_loop_statement : FOR NAME IN sequence COLON suite'
    print(f"Parsed for-loop: for {p[2]} in {p[4]}")
    p[0] = ('for_loop', p[2], p[4], p[6])

def p_sequence(p):
    '''sequence : NAME
                | list
                | range_func
                | STRING'''
    p[0] = p[1]

def p_list(p):
    'list : LBRACKET items RBRACKET'
    p[0] = ('list', p[2])

def p_items(p):
    '''items : items COMMA expression
             | expression'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_range_func(p):
    'range_func : RANGE LPAREN expression RPAREN'
    p[0] = ('range', p[3])

def p_expression_statement(p):
    'expression_statement : expression'
    pass

def p_expression(p):
    '''expression : term
                  | expression PLUS term'''
    if len(p) > 2:
        p[0] = ('add', p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : NUMBER
            | FLOAT
            | BOOLEAN
            | STRING
            | NAME'''
    p[0] = p[1]

def p_statement_return(p):
    'statement : RETURN expression'
    print("Parsed return statement.")
    p[0] = ('return', p[2])

def p_empty(p):
    'empty :'
    p[0] = []
    pass

def p_invalid_function_def(p):
    '''invalid_function_def : NAME LPAREN parameters RPAREN COLON suite'''
    if p[1] in ['func', 'function', 'de', 'deff']:
        if p[1] == 'de':
            print(f"Parser: ERROR - Invalid keyword '{p[1]}'. Did you mean 'def'?")
        elif p[1] == 'func':
            print(f"Parser: ERROR - Invalid keyword '{p[1]}'. Python uses 'def' for functions, not 'func'")
        elif p[1] == 'function':
            print(f"Parser: ERROR - Invalid keyword '{p[1]}'. Python uses 'def' for functions, not 'function'")
        else:
            print(f"Parser: ERROR - Invalid keyword '{p[1]}'. Did you mean 'def'?")
    else:
        print(f"Parser: ERROR - Cannot call '{p[1]}' as a function in this context")
    p[0] = ('invalid_func', p[1])

def p_invalid_if_assignment(p):
    '''invalid_function_def : IF NAME EQUALS expression'''
    print(f"Parser: ERROR - Invalid syntax 'if {p[2]} = {p[4]}'")
    print(f"Parser: Did you mean 'if {p[2]} == {p[4]}' for comparison?")
    print(f"Parser: Note: Use '==' for comparison, '=' is for assignment")
    p[0] = ('invalid_if', p[2], p[4])

def p_error(p):
    if p:
        print(f"Parser: Syntax error at '{p.value}' (token type: {p.type}) on line {p.lineno}")
        print(f"Parser: Invalid syntax - this doesn't match any valid Python pattern")
        parser.errok()
    else:
        print("Parser: Syntax error at EOF")

parser = yacc.yacc()

if __name__ == "__main__":
    while True:
        print("\n--- Interactive Python Parser ---")
        print("Enter Python code to parse. Type '!done' on a new line when you are finished.")

        lines = []
        while True:
            try:
                line = input(">>> ")
                if line.strip() == '!done':
                    break
                lines.append(line)
            except EOFError:
                break
        
        code = "\n".join(lines)

        import re
        code_to_parse = re.sub(r'print\(.*\)', '', code)

        print("\n--- Starting Combined Parser ---")
        parser.parse(code_to_parse, lexer=lexer)
        print("\n--- Parsing Complete ---")

        another_run = input("\nWould you like to start another run? (y/n): ").lower()
        if another_run != 'y':
            print("Exiting parser.")
            break