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
    #focalScript = 'test_modularity.py'
    pyFilenames=relevantPyFiles(focalScript)
    print(f'{focalScript} calls these modules residing in the current directory:')
    for pyName in pyFilenames:
        if pyName != 'pyonly.py':  #pyonly.py uses SpecialCare; handles it itself of itself 
            pyjName = pyName.replace('.py', '.pyj')
            print(f'::mf::  {pyName} -> {pyjName}')
            pyjFile =      open(pyjName, 'w'       )
            pyjFile.write( open( pyName).read() )
            pyjFile.close()
    
import sys
make_pyjs(sys.argv[1])
