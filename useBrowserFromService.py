from chromedriverService import BrowserFromService, Keys
from copypaste import write_to_clipboard, read_from_clipboard
from time import sleep

B = BrowserFromService(headless = True)

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
                print(line)                
        fixedLines.append(line)
            
    return '\n'.join(fixedLines)

def goToWorkspace():
    global textarea
    B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace/edit')
    textarea=B.find_element_by_tag_name('textarea')

goToWorkspace()
#typeToWorkspace()
from selenium.webdriver import ActionChains

targetName = 'test.py'

def pasteToBrowser( src ):
    #select all and delete
    textarea=B.find_element_by_tag_name('textarea')
    textarea.send_keys(Keys.COMMAND+"a") #select all
    textarea.send_keys(Keys.BACKSPACE)
    
    #fill clipboad (and right click because it seems to allow things to work (bizarrely)
    actions=ActionChains(B)
    actions.context_click().send_keys(Keys.ARROW_DOWN).perform() #THIS MAKES PAST WORK.
    write_to_clipboard('GlowScript 2.7 VPython\n\n' + src + '\n')

    #paste
    actions=ActionChains(B)
    actions.send_keys(Keys.SHIFT+Keys.INSERT).perform()
pasteToBrowser( srcFromFileName( targetName ) )

def getEmbeddableSrc():
    B.get('http://localhost:8080/#/user/jschull/folder/Public/program/workspace/share')
    sleep(1) #allow time for textarea to fill
    textarea=B.find_element_by_tag_name('textarea')
    embeddableSrc = B.find_element_by_css_selector('.embedSource').text
    return embeddableSrc

def createHTML( src ): #works but uses glowscript template
    src = src.split('<![CDATA[//><!--')[1]
    htmlName = targetName.replace('.py', '.html')
    f=open( htmlName, 'w' )
    
    f.write(f"""

<div id="glowscript" class="glowscript">
<link type="text/css" href="http://localhost:8080/css/redmond/jquery-ui.custom.css" rel="stylesheet" />
<link type="text/css" href="http://localhost:8080/css/ide.css" rel="stylesheet" />

<script type="text/javascript" language="javascript" src="http://localhost:8080/lib/jquery/IDE/jquery.min.js"></script>
<script type="text/javascript" language="javascript" src="http://localhost:8080/lib/jquery/IDE/jquery-ui.custom.min.js"></script>
<script type="text/javascript"                       src="http://localhost:8080/package/glow.2.7.min.js"></script>
<script type="text/javascript"                       src="http://localhost:8080/package/RSrun.2.7.min.js"></script>

<script type="text/javascript"><!--//--><![CDATA[//><!--

{src}  """)
    
    f.close()
    
    print(f'{htmlName} created')
createHTML( getEmbeddableSrc() )

B.quit()