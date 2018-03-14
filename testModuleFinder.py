from modulefinder import ModuleFinder

def relevantPyFiles(focalScript = 'test.py'):
    finder = ModuleFinder(['.'])
    finder.run_script(focalScript)

    import os

    relevantPyFiles=[]
    for name, mod in finder.modules.items():
        if os.path.isfile(name+'.py'):
            relevantPyFiles.append(name+'.py')
            #print(f' {name}.py', end='\t: ')
            #print(', '.join(list(mod.globalnames.keys())))

    return(relevantPyFiles)

if __name__=='__main__':
    focalScript = 'test_modularity.py'
    print(f'{focalScript} calls these modules residing in the current directory:')
    print(relevantPyFiles(focalScript))