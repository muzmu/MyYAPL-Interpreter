import ply.yacc as yacc
from parser import parser
import lexer
import sys

VARIABLE_TYPES = lexer.VARIABLE_TYPES
variables = {}
scope_level = 1
structures = {}

def get_data(vari,level):
    if level < 1:
        print("No such variable exist")
        sys.exit()
    elif vari not in variables[level].keys():
        return get_data(vari,level-1)
    else:  
        return variables[level][vari][0]

def get_data_type(vari,level):
    if level < 1:
        print("No such variable exist")
        sys.exit()
    elif vari not in variables[level].keys():
        return get_data_type(vari,level-1)
    else:  
        return variables[level][vari][1]
    
def set_data_val(vari,level,toset):
    if level < 1:
        print("No such variable exist")
        sys.exit()
    elif vari not in variables[level].keys():
        set_data_val(vari,level-1,toset)
    else:  
        variables[level][vari][0] = toset

def get_struct_data(s_name,vari,level):
    if level < 1:
        print("No such Struct obj exist")
        sys.exit()
    elif s_name not in variables[level].keys():
        return get_struct_data(s_name,vari,level-1)
    else:
        if vari not in variables[level][s_name][0].keys():
            print("No varible" , vari, "exist in struct" ,s_name)
            sys.exit()
        return variables[level][s_name][0][vari][0]

def set_struct_data(s_name,vari,level,data):
    if level < 1:
        print("No such Struct obj exist")
        sys.exit()
    elif s_name not in variables[level].keys():
        return get_struct_data(s_name,vari,level-1)
    else:
        if vari not in variables[level][s_name][0].keys():
            print("No varible" , vari, "exist in struct" ,s_name , )
            sys.exit()
        if variables[level][s_name][0][vari][1] == 'INT' and type(data) != int:
            print("Variable type MISMATCH")
            sys.exit()
        if variables[level][s_name][0][vari][1] == 'BOOL' and type(data) != bool:
            print("Variable type MISMATCH")
            sys.exit()
        if variables[level][s_name][0][vari][1] == 'STRING' and type(data) != str:
            print("Variable type MISMATCH")
            sys.exit()
        if variables[level][s_name][0][vari][1] == 'DOUBLE' and type(data) != float:
            print("Variable type MISMATCH")
            sys.exit()
        variables[level][s_name][0][vari][0] = data
        
        


def run(tree):
    global variables
    global scope_level
    global structures
    if scope_level not in variables.keys():
        variables[scope_level] = {}
    print(tree)
    if type(tree) == tuple:
        if tree[0] == '+':
            return run(tree[1]) + run(tree[2])
        elif tree[0] == '-':
            return run(tree[1]) - run(tree[2])
        elif tree[0] == '*':
            return run(tree[1]) * run(tree[2])
        elif tree[0] == '/':
            val = run(tree[2])
            if val:
                return run(tree[1]) / val
            else:
                print("Divide by Zero ERROR")
                sys.exit()
        elif tree[0] == '%':
            return run(tree[1]) % run(tree[2])
        elif tree[0] == '^':
            return run(tree[1]) ^ run(tree[2])
        elif tree[0] == '<':
            return run(tree[1]) < run(tree[2])
        elif tree[0] == '>':
            return run(tree[1]) > run(tree[2])
        elif tree[0] == '<=':
            return run(tree[1]) <= run(tree[2])
        elif tree[0] == '>=':
            return run(tree[1]) >= run(tree[2])
        elif tree[0] == '==':
            return run(tree[1]) == run(tree[2])
        elif tree[0] == '!=':
            return run(tree[1]) != run(tree[2])
        elif tree[0] == 'AND':
            return run(tree[1]) and run(tree[2])
        elif tree[0] == 'OR':
            return run(tree[1]) or run(tree[2])
        elif tree[0] == 'NOT':
            return ~run(tree[1])
        elif tree[0] == 'PRINT':
            if type(tree[1]) == tuple and tree[1][0] == 'PRINT':
                print(run(tree[1][1]),' ',end = '')
                return run(tree[1][2])
            return print(run(tree[1]))
        elif tree[0] == 'INI':
            if tree[1] not in VARIABLE_TYPES:
                print("Variable type Unknown")
                sys.exit()
                return "Error"
            elif tree[2][1] in variables.keys():
                print("Variable Already Declared")
                sys.exit()
                return "Error"
            val = run(tree[2][2])
            if tree[1] == 'INT' and type(val) != int:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if tree[1] == 'DOUBLE' and type(val) != float:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if tree[1] == 'STRING' and type(val) != str:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if tree[1] == 'BOOL' and type(val) != bool:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            variables[scope_level][tree[2][1]] = {}
            variables[scope_level][tree[2][1]][1] = tree[1]
            variables[scope_level][tree[2][1]][0] = val
            print(variables)
        elif tree[0] == 'INI_EMPTY':
            variables[scope_level][tree[2]] = {}
            variables[scope_level][tree[2]][1] = tree[1]
            variables[scope_level][tree[2]][0] = None
        elif tree[0] == '=':
            data = get_data(tree[1],scope_level)
            val = run(tree[2])
            typ = get_data_type(tree[1],scope_level)
            if typ == 'INT' and type(val) != int:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if typ == 'DOUBLE' and type(val) != float:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if typ == 'STRING' and type(val) != str:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            if typ == 'BOOL' and type(val) != bool:
                print("Variable Type MISMATCH")
                sys.exit()
                return "Error"
            set_data_val(tree[1],scope_level,val)
        elif tree[0] == 'NAME':
            data = get_data(tree[1],scope_level)
            return data
        elif tree[0] == 'DO_WHILE':
            scope_level = scope_level + 1
            for ele in tree[2]:
                run(ele)
            del variables[scope_level]
            scope_level = scope_level -1
            while run(tree[1]):
                scope_level = scope_level + 1
                for ele in tree[2]:
                    run(ele)
                del variables[scope_level]
                scope_level = scope_level -1
        elif tree[0] == 'STRUCT':
            if tree[1] == 'DEF':
                if tree[2] in structures.keys():
                    print("Cannot redefine Struct " , tree[2])
                    sys.exit()
                structures[tree[2]] = {}
                for ele in tree[3]:
                    if ele and ele[0] == 'INI_EMPTY':
                        structures[tree[2]][ele[2]] = {0:None , 1:ele[1]}
                    if ele and ele[0] == 'INI':
                        print("You cannot assign value in struct defination")
                        sys.exit()
            if tree[1] == 'INI':
                if tree[2] not in structures.keys():
                    print(tree[2] , ' Variable type unknown')
                    sys.exit()

                variables[scope_level][tree[3]] = {}
                variables[scope_level][tree[3]][0] = structures[tree[2]].copy()
                variables[scope_level][tree[3]][1] = tree[2]
                print(variables[scope_level][tree[3]])

            if tree[1] == 'NAME':
                # if tree[2] not in structures.keys():
                #     print(tree[2] , ' Variable type unknown')
                #     sys.exit()
                return get_struct_data(tree[2],tree[3],scope_level)

            if tree[1] == '=':
                # if tree[2] not in structures.keys():
                #     print(tree[2] , ' Variable type unknown')
                #     sys.exit()
                set_struct_data(tree[2],tree[3],scope_level,run(tree[4]))






            
    else:
        return tree


while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    for data in parser.parse(s):
        run(data)