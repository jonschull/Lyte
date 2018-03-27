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
    
    
    SSS = os.getcwd() + '/' +  stacheDir
    print('makeSupportScriptStache\t', SSS, end=' ')
    try:
        os.mkdir(SSS)
        print('created')
    except FileExistsError:
        print('exists')
    
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
    
    htmldir=os.getcwd() + '/' + dirName
    print('prepareHTMLdir\t', htmldir, end=' ')
    try:
        os.mkdir(dirName)
        print('created')
    except FileExistsError:
        print('exists')    
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

    if not os.path.exists(stacheDir):
        makeSupportScriptStache(stacheDir, GLOWPATH, scriptNames)
        
    prepareHTMLdir(HTMLdir)
    
    destDir = HTMLdir + '/' + 'supportScripts'
    delete(destDir)
    print('stacheDir', stacheDir)
    print('destDir', destDir)
    copy(stacheDir,destDir)
    print('makeHTMLdir\t', destDir, 'created and filled')
    
    return {'HTMLdir': HTMLdir, 'destDir': destDir}



def putInHTMLdir(filename = 'test.py'):
    """  create a directory for the python file
         then put the pythonfile into it 
    """
    HTMLdir = filename.replace('.py','')
    newDir = makeHTMLdir(HTMLdir)

    shutil.copyfile(filename, HTMLdir+'/'+ filename)
    print('putInHTMLdir\t', filename, 'copied into', HTMLdir)


if __name__=='__main__':
    putInHTMLdir('boxtest.py')
    
    if TESTING: print(pytest('-v'))




