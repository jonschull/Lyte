from IS import * #testing framework

import SSstache
import sys
import plumbum
from plumbum import local
from plumbum.cmd import touch, ls, pwd
from plumbum.cmd import open as pbOpen #so as not to conflict with python's open
from plumbum.path.utils import copy  #watch out for conflict with python's copy
from plumbum.path.utils import delete as pbDelete
rapydscript = local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']

def RS(*args, **kwargs):
    import inspect
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)[1][3]
    question = inspect.getouterframes(curframe, 2)[1][-2][-1].strip()
    lineNumber = inspect.getouterframes(curframe, 2)[1][-4]

    if SHOWRS:
        from trace import trace
        if type(args)==type(()):
            print(f'\nline {lineNumber}: rapydscript', args)
            trace()
            print(f'line {lineNumber}: \t\trapydscript', args)
            print()
        else:
            print('f\nline {lineNumber}: rapydscript', ' '.join(args))
    Error, output, errorMsg = rapydscript[args].run(retcode=None)
    IS('', EQUALTO, errorMsg)
    return output
        #print(ret.split('plumbum.commands.processes.ProcessExecutionError')[1])
#RS('-x', 'dummy.py')

def lsl(*args):
    """items from ls() returned as list"""
    try:
        return ls(*args).split()
    except plumbum.commands.processes.ProcessExecutionError:
        return []
        
        
def makeFile(fName, contents="print('makeFile')"):
    with open(fName,'w') as f:
        f.write(contents)
def contents(pyName=sys.argv[0]):
    return open(pyName).read()
if TESTING:  #makeFile, contents
    makeFile('testMakeFile', 'makefile')
    IS(contents('testMakeFile'), EQUALTO, 'makefile'  )
    pbDelete('testMakeFile')

def baseName(pyName=sys.argv[0]):
    return pyName.replace('.py','')
if TESTING:
    IS(baseName('somename.py'), EQUALTO, 'somename') 


def myHTML(pyName=sys.argv[0]):
    jsName = pyName.replace('.py','.js')
    
    return f"""<html>
            <head> <meta charset="UTF-8">
            <title>{pyName}</title>
             </head>
            <body>
               <script type="text/javascript" language="javascript"
               src="{jsName}">
               </script>
            </body>
        </html>
    <!--------------------------------------------------------
        This file (index.html) and the other files in this folder 
        were generated by lyte2.py so that the python script named {pyName}
        can run in the browser, using the javascript version named {jsName}

        
    ---------------------------------------------------------------->
     
    """

if TESTING:
    IS('lyte2.py', IN, myHTML() )
    IS(f'{baseName(sys.argv[0])}.js', IN, myHTML(sys.argv[0]) )
    makeFile('dummy.py', "print('I am dummy.py')")
    IS('dummy.js', IN, myHTML('dummy.py') )
    IS('<title>dummy.py</title>', IN, myHTML('dummy.py'))
    pbDelete('dummy.py')
    pbDelete('dummy')

    
    
def makeMyDir(pyName=sys.argv[0]):
    ret= AttrDict() #for testing
    
    if pyName:
        ret.fileName=pyName
    else:
        ret.fileName=sys.argv[0]
        
    SSstache.makeHTMLdir(ret.fileName)
    return ret
if TESTING:
    makeMyDir()
    myName= sys.argv[0]
    IS(myName, IN, lsl(baseName(myName) ))
    IS('supportScripts',      IN, lsl(baseName(myName)) )
    makeFile('dummy.py', "print('I am dummy.py')" )
    makeMyDir('dummy.py')
    IS('dummy.py', IN, lsl('dummy') )
    IS('supportScripts',      IN, lsl('dummy') )
    pbDelete('dummy.py')
    pbDelete('dummy')

def makeMyIndexHTML(pyName=sys.argv[0]):
    makeMyDir(pyName)
    myDir=baseName(pyName)
    contents(pyName)
    makeFile(f'{myDir}/index.html', myHTML(pyName) )
if TESTING:
    makeFile('makeMyIndex.py', 'this is to test makeFile and makeMyIndex')
    makeMyIndexHTML('makeMyIndex.py')
    IS('<html>', IN, contents('makeMyIndex/index.html') )
    pbDelete('makeMyIndex')
    pbDelete('makeMyIndex.py')
        
def makeMyJS(pyName=sys.argv[0]):
    """assumes myDir exists"""
    myDirName = baseName(pyName)
    ret = RS('-x', pyName) #for error checking
    RS(pyName, '-o', f"{myDirName}/{myDirName+'.js'}") 
    return ret

if TESTING:#TESTING: #test makeMyIndexHTML and makeMyJS
    makeFile( 'dummy.py', "print('hello dummy')" )
    makeMyDir('dummy.py')
    makeMyIndexHTML('dummy.py')
    myDirName = baseName('dummy.py')
    IS('index.html', IN, lsl(myDirName) )
    IS('src="dummy.js"',   IN, contents(f'{myDirName}/index.html' ) )
    IS('<html>',     IN, contents(f'{myDirName}/index.html' ) )
    programOutput = makeMyJS('dummy.py')
    IS('dummy.js',   IN, lsl('dummy') )
    IS('hello dummy\n', EQUALTO, programOutput)
    pbDelete('dummy.py')
    pbDelete('dummy')
    
def lyten(pyName=sys.argv[0]):
    """presumes pyName exists"""
    makeMyDir(pyName)
    makeMyJS(pyName)
    makeMyIndexHTML(pyName)
    dirName = baseName(pyName)
    indexPath = baseName(pyName)+'/index.html'
    print(f'\n|| Created folder with {indexPath}\n')
    return indexPath
if 0:#TESTING:
    makeFile('dummy.py', "print('this is from lyten')" )
    ret = lyten('dummy.py')
    IS(ret, EQUALTO, 'dummy/index.html')
    pbDelete('dummy')
    pbDelete('dummy.py')
    #pbOpen(f'dummy/index.html')
    #NEED BETTER TEST
    
def enLytenMe():
    lyten() #with no parameters
    
def runMe(openBrowser=False):
    print('_'*20, 'running under rapyscript', '_'*20)
    if sys.argv[0] == __file__:
        print(f"SORRY:  runMe() won't work on {__file__}")
    else:
        ret = RS('-x', sys.argv[0])
        if ret:
            print(ret)
        if openBrowser:
            indexPath = f'{baseName(sys.argv[0])}/index.html'
            pbOpen(indexPath)
    
    
def testLyte():
    python=local['python3']
    ret = python('lyte2.py')
    print(ret)
    return ret

#lyten(f'{pwd().strip()}/import_lyte2/import_lyte2.py')

if TESTING:
    print(f"""
___________________________                   
|Test Summary
|YES: {RESULTS.yes:4}
|NO: {RESULTS.no:4}                
""")
    

#create dummy pyonly.pyj with dummy functions for rapydscript
pyjFile=open('pyonly2.pyj','w')
pyjFile.write('#### pyj is here to satisfy Rapydsript import ####\n\n')
for dirObj in dir():
    if not dirObj.startswith('__'):
        #print( dirObj)
        pyjFile.write(f'def {dirObj}(*args, **kwargs): pass\n')     
pyjFile.close()

if __name__=='__main__':
    makeFile('hello.py', "print('hello from hello.py')")
    if len( sys.argv ) > 1:
        lyten('hello.py')
    else:
        print(f'{sys.argv[0]}:  try python3 {sys.argv[0]} hello.py') 