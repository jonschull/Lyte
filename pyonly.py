""" pyonly.py is for lyte commands that should 
    do something under python
    do nothing under rapydscript, 
        yet not choke the rapydscript compiler when lyte imports pyonly
        
    the trick is 
        1) to hide all python-specific imports within functions
            (because at compile time, the compiler doesn't test imports within functions)  
        2) to create a mocked up pyonly.pyj that is will allow rapydscrpyt to  find neutered pyonly functions (e.g., when imported by lyte).
        
    (a simpler trick might have been to 
        1) resolve that only lyte would import pyonly
        2) remove "import lyte" before having rapydscpyt compile lyte ) 
        
    
"""

def getPyName():
    import sys
    pyName=sys.argv[0]
    return pyName

def make_lyte_pyj():
    mytext=open('lyte.py').read()
    pyj=open('lyte.pyj','w')
    pyj.write(mytext)
    pyj.close()

from modulefinder import ModuleFinder

def relevantPyFiles(focalScript = 'test.py'):
    """return list of relevant pyfiles for copy_scripts_to_pyj"""
    
    finder = ModuleFinder(['.'])   #TODO don't just search local directories; search "relevant" directories
    finder.run_script(focalScript)

    import os

    relevantPyFiles=[]
    for name, mod in finder.modules.items():
        if os.path.isfile(name+'.py'):
            relevantPyFiles.append(name+'.py')
            #print(f' {name}.py', end='\t: ')
            #print(', '.join(list(mod.globalnames.keys())))

    return(relevantPyFiles)

def copy_Scripts_to_pyj(quiet=False):
    """this makes the focal scripts and its imports importable and usable by rapydscript.
    NOTE: *this* script(pyonly.py) treas pyonly.pyj special, mocking its own commands
    to hide them from rapyscript.
    """
    import sys
    callingScript = sys.argv[0]
    pyFileNames = [callingScript] + relevantPyFiles(callingScript)
    for pyFileName in pyFileNames:
        if pyFileName != 'pyonly.py':
            pyjName = pyFileName.replace('.py', '.pyj')
            pyj = open( pyjName, 'w')
            pyj.write( open(pyFileName).read() )
            pyj.close()
            if not quiet:
                print(f'::lyte:: created {pyjName}')

def makeHTMLandJS(openBrowser=True, quiet=True):
    pyName = getPyName()
    HTMLname = pyName.replace('.py', '.html')
    JSname =   pyName.replace('.py', '.js'  )
    if not quiet:
        print(f'::webME:: making {JSname} and {HTMLname}::::')
    HTMLfile = open(HTMLname, 'w')
    content = f""" <html>
        <head> <meta charset="UTF-8"> 
         </head>
        <body>
           <script type="text/javascript" language="javascript" src="{JSname}">
           </script>
        </body>
    </html>"""
    
    HTMLfile.write(content)
    HTMLfile.close()
    #print(content)
    
    from plumbum import local
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
    rs('-x', pyName)
    rs(pyName, '-o', JSname)
    if openBrowser:
        browser=local['open']
        browser(HTMLname)
    
    
def runRapydscript():
    pyName = getPyName()
    from plumbum import local
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
    print('\n >>> rapydscript -x', pyName,'\n')
    print(rs('-x', pyName) )


#create dummy pyonly.pyj with dummy functions for rapydscript
pyjFile=open('pyonly.pyj','w')
pyjFile.write('#### pyj is here to satisfy Rapydsript import ####\n\n')
for dirObj in dir():
    if not dirObj.startswith('__'):
        if not dirObj == 'pyjFile':
            pyjFile.write(f'def {dirObj}(*args, **kwargs): pass\n')     
pyjFile.close()

if __name__=='__main__':
    pyName = getPyName()
    print('can not test makeHTMLandJS() with itself')
    print('test by running....    python3 sayhi.py    ')