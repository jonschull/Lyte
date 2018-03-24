from plumbum.path.utils import copy, delete
from plumbum.cmd import mkdir, cd, pwd
from plumbum import local, FG, TF

from chromedriverService import BrowserFromService, Keys, msg



testDir = 'testBuild'

delete(testDir)
mkdir( testDir)

fileNames ="""
vpytohtml.py
chromedriver.txt
SSstache.py
chromedriverService.py
copypaste.py
testBuild.py
""".split()

for fileName in fileNames:
    copy(fileName, f'{testDir}/{fileName}')
    
def positionWindow():
    T.maximize_window()
    screen = T.get_window_size()
    width  = screen['width']
    height = screen['height']
    T.set_window_rect(0,0,round(width/2), round(height/2))
  

#butterfly=local['/Users/jonschull-MBPR/miniconda3/bin/butterfly.server.py']
#print(butterfly('--unsecure') )

T = BrowserFromService(headless = False)
T.get('http://localhost:57575')

from time import sleep
print('You have 5 seconds to enter your password in the terminal.')
sleep(5)

def typeThis(s):
    from selenium.webdriver import ActionChains
    actions=ActionChains(T)
    actions.send_keys(s + Keys.RETURN).perform()

workdir = pwd().strip() + '/' + testDir
typeThis(f"""

ipython3

clear
""")

positionWindow()

sleep(1)

typeThis(f"""

exit

cd {workdir}

ipython3 vpytohtml.py

""")