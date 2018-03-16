def relevantPyFiles(focalScript = 'test.py'):
    import modulefinder 
    finder = modulefinder.ModuleFinder(['.'])
    finder.run_script(focalScript)

    import os

    relevantPyFiles=[]
    for name, mod in finder.modules.items():
        if os.path.isfile(name+'.py'):
            relevantPyFiles.append(name+'.py')
            #print(f' {name}.py', end='\t: ')
            #print(', '.join(list(mod.globalnames.keys())))
    relevantPyFiles.reverse()
    return(relevantPyFiles)

def make_pyjs(focalScript = 'test_modularity.py'):
    verbose=False
    #focalScript = 'test_modularity.py'
    pyFilenames=relevantPyFiles(focalScript)
    #print(f'{focalScript} calls these modules residing in the current directory:')
    for pyName in pyFilenames:
        if pyName != 'pyonly.py':  #pyonly.py uses SpecialCare; handles it itself of itself 
            pyjName = pyName.replace('.py', '.pyj')
            if verbose: print(f'::make_pyjs::  {pyName} -> {pyjName}', end=' ')
            pyjFile =      open(pyjName, 'w'       )
            pyjFile.write("""
from pythonize import strings
strings()
from __python__ import dict_literals, overload_getitem, bound_methods

""")
            pyjFile.write( open( pyName).read() )
            pyjFile.close()


    """('this program is meant to be imported by pyonly.py or run from the commandline')
       ('It creates maximally python-like pyjs for argv[0] and all the local .pys argv[0] imports')"""

import sys
make_pyjs(sys.argv[1])
