import makemyPYJ
def beginsWith(lookFor, line):
    words =      line.strip().split()
    lookFor = lookFor.strip().split()
    if len(words)<len(lookFor):
        return False
    
    return words[:len(lookFor)] == lookFor

def vpythonImport(line):
    return beginsWith('from vpython import *',line)

line ='from   vpython import *'
print(vpythonImport(line))