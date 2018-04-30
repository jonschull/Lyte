import sys
from plumbum import local
cp = local['cp']
rm = local['rm']
ls = local['ls']
pwd = local['pwd']

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def makeMyPYJ():
    """
    When RapydScript is asked to import x,
    it looks for x.pyj.  Therefore, 
    to facilitate RapydScript compiles, we
    * remove pyj and py-cached
    * copy the calling x.py to x.pyj
    """


    myName = sys.argv[0] #the calling py
    PYJname = myName.replace('.py', '.pyj')

    #remove all the ".pyj-cached'files
    fileNames=ls().split()
    for fileName in fileNames:
        if fileName.endswith('.pyj-cached'):
            rm(fileName)

    cp(myName, PYJname)
    
    print(f'(makemyPYJ copied {myName} to {PYJname} and removed *.pyj-cached)\n')

def makeDummyPYJ(baseName, funcNames=[]):
    f=open(f'{dir_path}/{baseName}.pyj','w')
    for funcName in funcNames:
        f.write(f"""
def {funcName}(*args, **kwargs):
    pass
""")
        print(f"makemyPYJ.py executed makeDummPYJ('{baseName}', '{funcName}')")
 
myDir = pwd().strip()
print('pwd', pwd())
print('__file__', __file__)
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print('dir_path', dir_path)

if __name__== '__main__':
    makeDummyPYJ('makeMyPYJ', funcNames = ['makeDummyPYJ', 'makeMyPYJ']) 
else:
   import sys
   makeMyPYJ()
 
