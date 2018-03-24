from chromedriverService import BrowserFromService, Keys, msg
from copypaste import write_to_clipboard, read_from_clipboard
from time import sleep
from selenium.webdriver import ActionChains
import requests

#B = BrowserFromService(headless = True)
#B.get('http://localhost:8080/_ah/login')


def login():
    B.get('http://localhost:8080/_ah/login')
    sleep(1)
    input=B.find_element_by_id('email')
    input.click()
    input.send_keys(Keys.RIGHT * 20)
    input.send_keys(Keys.BACKSPACE * 20)
    input.send_keys('jschull@gmail.com')
    input.send_keys(Keys.TAB*2)
    input.send_keys(Keys.RETURN)
#login()


def srcFromFileName(filename='test.py'):
    """get source, apply transformation"""

    thesource=open(filename).read()
    
    lines= thesource.split('\n')
    lines.insert(1, 'def GlowMe( me=""): pass\n')
    lines.insert(2, "get_library('http://localhost:8080/lib/jonlib.js')\n")
    
    fixedLines=[]
    for line in lines:
        #lines beginning with any of these phrases need to commented out 
        toxicStarters = 'GlowMe from import DICT=dict'.split()
        for poison in toxicStarters:
            if line.strip().startswith(poison):
                line='##GlowMe    '+line
                #print(line)                
        fixedLines.append(line)
            
    return '\n'.join(fixedLines)

def goToWorkspace():
    global textarea
    B.get('http://localhost:8080/#/user/jschull/folder/Public/')
    print('page loaded?') 
    sleep(3)
    B.find_element_by_link_text('Create New Program').click()
    actions=ActionChains(B)
    actions.send_keys('workspace' + Keys.RETURN).perform() #THIS MAKES PAST WORK.

    textarea=B.find_element_by_tag_name('textarea')

#goToWorkspace()
#typeToWorkspace()

#targetName = 'test.py'

def pasteToBrowser( src ):
    #select all and delete
    textarea=B.find_element_by_tag_name('textarea')
    
    #copy into clipboard
    write_to_clipboard('\n' + src + '\n')
    sleep(1)

    actions=ActionChains(B)
    actions.context_click().send_keys(Keys.ARROW_DOWN).perform() #THIS MAKES PASTE WORK.
    
    #paste
    actions=ActionChains(B)
    actions.send_keys(Keys.SHIFT+Keys.INSERT).perform()
#pasteToBrowser( srcFromFileName( targetName ) )

def getEmbeddableSrc( ):
    B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace/share')
    sleep(1) #allow time for textarea to fill
    textarea=B.find_element_by_tag_name('textarea')
    embeddableSrc = B.find_element_by_css_selector('.embedSource').text
    return embeddableSrc



def createHTML( targetName ): #works; depends on glowscript server for scripts but creates directory that is free standing.
    src = getEmbeddableSrc( )
    src = src.split('<![CDATA[//><!--')[1]
    folderName = targetName.replace('.py', '')
    
    import SSstache
    newDirs = SSstache.makeHTMLdir()
    filepath = newDirs['HTMLdir'] + '/' + 'index.html'
    f=open( filepath , 'w' )
    f.write(f"""<!--------------------------------------------------------
    This file (index.html) and the other files in this folder 
    were generated by vpytohtml.py 
    to make the vpython script called "{targetName}" 
    run in the browser without dependencies.
    {targetName}:
    

{srcFromFileName( targetName )}

---------------------------------------------------------------->

<div id="glowscript" class="glowscript">

<link type="text/css" href="supportScripts/jquery-ui.custom.css" rel="stylesheet" />
<link type="text/css" href="supportScripts/ide.css" rel="stylesheet" />

<script type="text/javascript" language="javascript" src="supportScripts/jquery.min.js"></script>
<script type="text/javascript" language="javascript" src="supportScripts/jquery-ui.custom.min.js"></script>
<script type="text/javascript"                       src="supportScripts/glow.2.7.min.js"></script>
<script type="text/javascript"                       src="supportScripts/RSrun.2.7.min.js"></script>
<script type="text/javascript"><!--//--><![CDATA[//><!--
{src}  """)
    f.close()
    
    print(f'Created {filepath}' )
    return filepath
     
from plumbum import local, NOHUP, BG

def startGlowScript():
    python=local['python']
    dev_appserver = local['/Users/jonschull-MBPR/Downloads/google-cloud-sdk/bin/dev_appserver.py']
    GSappYAML = local['/Users/jonschull-MBPR/glowscript/glowscript/app.yaml']
    python[dev_appserver, GSappYAML] & NOHUP(stdout='/dev/null')
    sleep(2) #give the server time to start up
    
def GSserverIsRunning():
    try:
        requests.get('http://localhost:8080')
        msg('okGS)')
    except Exception as e:
        msg('newGS')
        startGlowScript()

def webServer(targetName):
    from plumbum import local, NOHUP, BG
    python3 = local['python3']
    dirName = targetName.replace('.py','')
    if python3['-m', 'http.server', '8081'] & NOHUP(stdout='/dev/null'):
        msg('server at 8081')
        BrowserFromService().get(f'http://localhost:8081/{dirName}')
        
        


def vpy_to_html(targetName = 'test.py', headless=True, openBrowser=False):
    global B
    #headless= True
    msg('(GS:localhost:8080?')
    if GSserverIsRunning():
        msg('OK')
        
    msg(f'Chrome')
    B = BrowserFromService(headless = headless)
    if headless: print('headless', end='...')
    msg(f'logging in')
    
       
    login()
    msg('IN')
    
    #targetName='test.py'
    msg(f'{targetName}-->')
    goToWorkspace()

    pasteToBrowser( srcFromFileName( targetName ) )

    indexHTML = createHTML(targetName )
    B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace')
    ActionChains(B).send_keys(Keys.ESCAPE).perform() #get rid of the magic context menu?
    sleep(2)
    try:
        errorTB = B.find_elements_by_class_name('error-traceback')[1].text
        errorMsg = B.find_elements_by_class_name('error-details')[1].text
        print(f"""GLOWSCRIPT ERROR  {errorTB}
                                    {errorMsg}""")
    except IndexError:
        if openBrowser:
            webServer(targetName)


def createTestPy(timestamp=''):
    msg('creating test.py')
    with open('test.py', 'w') as f:
        f.write(f"""

box()

print('this is test.py')

def f():
    print('this is a function')
f()

print("{timestamp}")

""")

if __name__=='__main__':
    
    import sys
    
    if len(sys.argv)>1:
        pyFile = sys.argv[1]
    else:
        pyFile='test.py'
        import time
        createTestPy(time.strftime('%X %x %Z'))
    
    vpy_to_html( 'test.py', headless=True, openBrowser=True)
    