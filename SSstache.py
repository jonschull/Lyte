"""Support Script stache"""
from plumbum import local
from plumbum.cmd import ls
from plumbum.path.utils import copy, delete

import os, shutil

TESTING = True
if TESTING:
    pytest=local['pytest']
    

def makeSupportScriptStache(stacheDir   =   'VPsupportScripts',
                            GLOWPATH    =   '/Users/jonschull-MBPR/glowscript',
                            scriptNames ="""/lib/jquery/IDE/jquery.min.js
                                            /lib/jquery/IDE/jquery-ui.custom.min.js 
                                            /package/glow.2.7.min.js 
                                            /package/RSrun.2.7.min.js
                                            /css/redmond/jquery-ui.custom.css 
                                            /css/ide.css""".split() ):
    """ Create folder called stacheDir
        fill it with the scripts we named
        by getting them from GLOWPATH (the directory where they can be found)
        pytest
    """
    
    verbose = False
    SSS = os.getcwd() + '/' +  stacheDir
    if verbose: print('makeSupportScriptStache\t', SSS, end=' ')
    try:
        os.mkdir(SSS)
        if verbose: print('created')
    except FileExistsError:
        if verbose: print('exists')
    
    #scriptNames = '/lib/jquery/IDE/jquery.min.js /lib/jquery/IDE/jquery-ui.custom.min.js /package/glow.2.7.min.js /package/RSrun.2.7.min.js'.split()
    #scriptNames = scriptNames + '/css/redmond/jquery-ui.custom.css /css/ide.css'.split()
    for scriptName in scriptNames:
        scriptPath = GLOWPATH + scriptName
        scriptShortName = scriptName.split('/')[-1]
        shutil.copyfile(scriptPath, SSS+'/'+scriptShortName)
    return SSS

           
def prepareHTMLdir(dirName='test'):
    """create HTMLdir if necessary
    pytest
    """
    verbose=False
    htmldir=os.getcwd() + '/' + dirName
    print('prepareHTMLdir\t', htmldir, end=' ')
    try:
        os.mkdir(dirName)
        if verbose: print('created')
    except FileExistsError:
        if verbose: print('exists')    
    return htmldir
        
        
def out(s):
    """simple debug utility
    if x==5, out(x) will print
      =x= 5
    """
    print(f'={s}= {globals()[s]}');

    
def makeHTMLdir(HTMLdir,
                stacheDir   =   'VPsupportScripts',
                GLOWPATH    =   '/Users/jonschull-MBPR/glowscript',
                scriptNames ="""/lib/jquery/IDE/jquery.min.js
                                /lib/jquery/IDE/jquery-ui.custom.min.js 
                                /package/glow.2.7.min.js 
                                /package/RSrun.2.7.min.js
                                /css/redmond/jquery-ui.custom.css 
                                /css/ide.css""".split() ):
    """create a stacheDir if necessary.
       create HTMLdir
       create supportScript
           fill it with scriptNames from stacheDir
           
    pytest
    """
    verbose=False
    if not os.path.exists(stacheDir):
        makeSupportScriptStache(stacheDir, GLOWPATH, scriptNames)
        
    prepareHTMLdir(HTMLdir)
    
    destDir = HTMLdir + '/' + 'supportScripts'
    delete(destDir)
    if verbose: print('stacheDir', stacheDir)
    print('destDir', destDir)
    copy(stacheDir,destDir)
    if verbose: print('makeHTMLdir\t', destDir, 'created and filled')
    
    return {'HTMLdir': HTMLdir, 'destDir': destDir}


def putInHTMLdir(filename = 'test.py'):
    """  create a directory for the python file
         then put the pythonfile into it 
    """
    verbose=False
    HTMLdir = filename.replace('.py','')
    newDir = makeHTMLdir(HTMLdir)

    shutil.copyfile(filename, HTMLdir+'/'+ filename)
    if verbose: print('putInHTMLdir\t', filename, 'copied into', HTMLdir)


if __name__=='__main__':
    with open('boxtest.py','w') as f:
        f.write('box()')
        
    putInHTMLdir('boxtest.py')
    
    #if TESTING: print(pytest('-v'))




