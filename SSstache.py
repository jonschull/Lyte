"""Support Script stache"""
GLOWPATH = '/Users/jonschull-MBPR/glowscript/glowscript'
verbose=False
import os, shutil

def null():
    pass

def makeSupportScriptStache():
    stacheName = 'supportScripts'
    SSS = os.getcwd() + '/' +  stacheName
    print('makeSupportScriptStache\t', SSS, end=' ')
    try:
        os.mkdir('./supportScripts')
        print('created')
    except FileExistsError:
        print('exists')
    
    scriptNames = '/lib/jquery/IDE/jquery.min.js /lib/jquery/IDE/jquery-ui.custom.min.js /package/glow.2.7.min.js /package/RSrun.2.7.min.js'.split()
    scriptNames = scriptNames + '/css/redmond/jquery-ui.custom.css /css/ide.css'.split()
    for scriptName in scriptNames:
        scriptPath = GLOWPATH + scriptName
        scriptShortName = scriptName.split('/')[-1]
        shutil.copyfile(scriptPath, './supportScripts/'+scriptShortName)
    return SSS
           
def prepareHTMLdir(dirName='test'):
    htmldir=os.getcwd() + '/' + dirName
    print('prepareHTMLdir\t', htmldir, end=' ')
    try:
        os.mkdir(dirName)
        print('created')
    except FileExistsError:
        print('exists')    
    return htmldir
        
def out(s):
    print('==', s, globals()[s])

def putInHTMLdir(filename = 'test.py', htmlDir='./test'):
    shutil.copyfile(filename, htmlDir+'/'+ filename)
    print('putInHTMLdir\t', filename, 'copied into', htmlDir)

def makeHTMLdir():
    SSS='./supportScripts'
    if not os.path.exists(SSS):
        makeSupportScriptStache()
        
    HTMLdir = prepareHTMLdir()
    destDir = HTMLdir + '/supportScripts'
    if os.path.exists(destDir):
        shutil.rmtree(destDir)
        print('makeHTMLdir\t', destDir, 'removed')
    shutil.copytree(SSS,destDir)
    print('makeHTMLdir\t', destDir, 'created and filled')
    return {'HTMLdir': HTMLdir, 'destDir': destDir}

if __name__=='__main__':
    newDirs = makeHTMLdir()
    putInHTMLdir('test.py', newDirs['HTMLdir'])




