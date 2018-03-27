from plumbum.path.utils import copy, delete
from plumbum.cmd import mkdir, pwd
from plumbum import local, FG, TF

from chromedriverService import BrowserFromService, Keys, msg

from datetime import datetime
timestamp = datetime.now().strftime("-%Y-%m-%d_%H%M%p")


def testBuild(target='lyte.py', fileNames= ['lyte.py', 'pyonly.py'] ):
    local.cwd.chdir(initialDir)
    global testDirName, fileName
    testDirName = target.replace('.py','')+ timestamp 
    print(f'\n\nTESTBUILD: making {testDirName}')
    mkdir( testDirName)


    for fileName in  fileNames:
        print(f'TESTBUILD: copying {fileName} -> {testDirName}/{fileName}')
        print('xxxx', f'{testDirName}/{fileName}')
        copy(fileName, f'{testDirName}/{fileName}')
        
    local.cwd.chdir(testDirName)
    print(pwd())
    print(f'TESTBUILD: running ipython3 {testDirName}/{target}\n')
    
    ipython3 = local['ipython3']
    ipython3(target)
    

initialDir=pwd().strip()

lytefiles="""
lyte.py
pyonly.py
""".split()

testBuild('lyte.py', lytefiles)


vpyfiles ="""
    vpytohtml.py
    chromedriver.txt
    SSstache.py
    chromedriverService.py
    copypaste.py
    testBuild.py
    """.split()

testBuild('vpytohtml.py', vpyfiles) #vpython

