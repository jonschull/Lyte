from SSstache import *
from plumbum.path.utils import delete
from plumbum.cmd import ls, touch, mkdir


def test_makeSupportScriptStache():
    delete('xyz')
    assert makeSupportScriptStache(stacheDir='xyz').endswith('xyz')
    assert ls('xyz').split()==['RSrun.2.7.min.js', 'glow.2.7.min.js', 'ide.css', 'jquery-ui.custom.css', 'jquery-ui.custom.min.js', 'jquery.min.js']
    delete('xyz')
       
def test_prepareHTMLdir():
     delete('xyz')
     prepareHTMLdir('xyz') 
     assert('xyz' in ls().strip())
     delete('xyz')

     
def test_makeHTMLdir():
    HTMLdirName = '123'
    delete( HTMLdirName )
    
    fakeSSname = 'fakeSupportScripts'
    delete(fakeSSname)
    mkdir(fakeSSname)
    scriptNames=['xyz.test', 'xyz2.test']
    for scriptName in scriptNames:
        touch(f'{fakeSSname}/{scriptName}')

    
    makeHTMLdir( HTMLdirName , 
                 stacheDir = fakeSSname,
                 GLOWPATH='.', 
                 scriptNames= scriptNames) 
                 
    assert('supportScripts' in ls( HTMLdirName ).split() )
    
    assert( ls('123/supportScripts').split() == scriptNames )
    
    delete( HTMLdirName )
    
    
def test_putInHTMLdir():
    open('box2.py','w').write('box(color=color.green)')
    putInHTMLdir('box2.py')
    assert( 'box2.py' in ls('box2').split() )
    delete('box2.py')
    
             
#prepareHTMLdir(dirName='xyz')
#test_makeHTMLdir()