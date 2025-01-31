# inspect_functions.py

import inspect

def add(x,y):
       'Adds two things'
       return x+y

print(dir(add))

code_obj = add.__code__

print("Co-Name:", code_obj.co_name)           # The name of the function
print("Co-Argument names:", code_obj.co_varnames)  # Tuple of argument names
print("Co-Numbers of arguments:", code_obj.co_argcount)  # Number of arguments
print("Co-Numbers of local variables:", code_obj.co_nlocals)  # Number of local variables
print("Co-Filesource:", code_obj.co_filename)  # The filename in which the code was defined
print("Co-Lineno:", code_obj.co_firstlineno)  # The first line number of the function
print("Co-Constants:", code_obj.co_consts)    # Tuple of constants used by the code
print("Co-Names:", code_obj.co_names)         # Tuple of global names used by the code
print("Co-Free vars:", code_obj.co_freevars)  # Tuple of free variables
print("Co-Cell vars:", code_obj.co_cellvars)  # Tuple of cell variables (used in closures)

#############################################################################################

# Inspect module usage

sig = inspect.signature(add)

print('\nParameters from inspect module:', tuple(sig.parameters))
