from chromedriverService import BrowserFromService, Keys
print('hi')
from copypaste import write_to_clipboard, read_from_clipboard
from time import sleep

B = BrowserFromService()
#from selenium import webdriver
#B=webdriver.Firefox()


B.get('http://localhost:8080/_ah/login')

def login():
    input=B.find_element_by_id('email')
    input.click()
    input.send_keys(Keys.RIGHT * 20)
    input.send_keys(Keys.BACKSPACE * 20)
    input.send_keys('jschull@gmail.com')
    input.send_keys(Keys.TAB*2)
    input.send_keys(Keys.RETURN)

login()





def clearOutWorkspace():
    global textArea
    B.get('http://localhost:8080/#/user/jschull/folder/Private/program/new/edit')
    sleep(1)
    textArea=B.find_element_by_tag_name('textarea')
    sleep(1)
    textArea.send_keys(Keys.COMMAND+"a")
    sleep(1)
    textArea.send_keys(Keys.BACKSPACE)

#clearOutWorkspace()

trace=True

def srcFromFileName(filename='test.py'):
    """get source, apply transformation"""
    if trace: print('srcFromFileName',filename)

    thesource=open(filename).read()
    
    lines= thesource.split('\n')
    
##    firstLine = 'GlowScript 2.7 VPython'
##    if lines[0] != firstLine:
##        lines.insert(0, firstLine )
##        
    lines.insert(1, 'def GlowMe( me=""): pass')
    lines.insert(2, "get_library('http://localhost:8080/lib/jonlib.js')")
    fixedLines=[]
    for line in lines:
        
        toxicStarters = 'GlowMe from import DICT=dict'.split()
        for poison in toxicStarters:
            if line.strip().startswith(poison):
                line='##GlowMe    '+line
                print(line)                
        fixedLines.append(line)
            
    return '\n'.join(fixedLines)

def goToWorkspace():
    global textArea
    B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace/edit')
    textArea=B.find_element_by_tag_name('textarea')


def typeInWorkspace( source = srcFromFileName()):
    global textArea
    try:
        textArea.send_keys('GlowScript 2.7 VPython') #expect trouble
    except:
    #fix trouble
        B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace/edit')
        textArea=B.find_element_by_tag_name('textarea')
    
    textArea.send_keys(source)
    
    

goToWorkspace()
#typeToWorkspace()
from selenium.webdriver import ActionChains
def pasteToBrowser():
    actions=ActionChains(B)
    sleep(1)
    actions.context_click().send_keys(Keys.ARROW_DOWN).perform() #THIS MAKES PAST WORK.  
    #actions=ActionChains(B)
    #actions.send_keys('GlowScript 2.7 VPython').send_keys(Keys.ENTER).perform()

    #THISWORKS
    actions=ActionChains(B)
    actions.send_keys(Keys.SHIFT+Keys.INSERT).perform()

pasteToBrowser()

#>>> input = B.find_element_by_id('prog-new-dialog').find_element_by_tag_name('form').find_element_by_tag_name('input')
