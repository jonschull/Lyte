from vpytohtml import *
from plumbum.path.utils import delete
from plumbum.cmd import ls, touch, mkdir

def test_login():
    B = BrowserFromService(headless = False)
    sleep(1)
    login(B)
    sleep(1)
    assert B.find_element_by_tag_name('body').text.startswith('Logged in')
    
    B.close()
    
    
def test_createTestPy(timestamp=''):
    "confirm existence of 'test.py'"
    delete('test.py')
    createTestPy()
    assert open('test.py').read().strip().startswith('print(interval)')
    delete('test.py')


def test_srcFromFileName():
    """confirm that srcFromFilename has the right content"""
    delete('test.py')
    createTestPy()
    assert srcFromFileName('test.py').strip().startswith('def GlowMe')


def test_goToWorkspace():
    """confirm we got to the right page""" 
    B = BrowserFromService(headless = False)
    
    login(B)
    sleep(1)
    print(goToWorkspace(B))
    assert B.find_elements_by_partial_link_text('Run this program') != None
    
    B.close()

   
def test_getEmbeddableSrc():
    """confirm he embeddable src was delivered by the right page"""
    global B
    
    B = BrowserFromService(headless = False)
    sleep(1)
    assert getEmbeddableSrc(B).startswith('<div id="glowscript" class="glowscript">')
    
    B.close()


def test_make_importsJS():
    """confirm that the default imports.js content exists"""
    assert 'function interval' in make_importsJS()


def test_createHTML( ):    
    """ confirm that createHTML creates the right folders and files  """
    delete('arbitrary')
    delete('arbitrary.py')

    global B
    with open('arbitrary.py', 'w') as f:
        f.write('box(color=color.purple)')
        
    B = BrowserFromService(headless = False)
    importsJS = make_importsJS()    
    ret = createHTML('arbitrary.py', B, importsJS = importsJS)
    print(ret.__dict__)
    
    assert 'arbitrary.py' in ls().split()
    assert ret.folderName == 'arbitrary'
    assert 'arbitrary' in ls().split()
    assert 'index.html' in ls('arbitrary').split()
    assert 'imports.js' in ls('arbitrary').split()
    assert 'supportScripts' in ls('arbitrary').split()
    assert 'box(color=color.purple)' in open('arbitrary.py').read()
    # THIS CURRENTLY DOES NOT ENSURE FUNCTIONALITY OF arbitrary.py BECAUSE
    # we haven't put it into the workspace,
    # so the javscript in index.html is does not contain our program
    
    B.close()
    delete('arbitrary')
    delete('arbitrary.py')

def test_GSserver():
    """kill the server,  restart it, confirm life"""
    def test_the_Server(port_Number):
        port_Number=str(port_Number)
        try:
            killServer(port_Number)
        except:
            pass
        assert GSserverIsRunning() == 1
        sleep(1)
        assert requests.get(f'http://localhost:{port_Number}')
    
    test_the_Server(8080)


def test_webServer():
    """kill the server if it's alive
       then start it and point it to a randomly named directory.
       To prove its in the randomly named directory,
           put a randomly-named file in it it and see if it shows up in the server.
           """
    try:
        killServer(8081)
    except:
        pass
 
    import random
    randomDirName = str(random.randint(10000,99999))
    mkdir(randomDirName)
    randomFileName = str(random.randint(10000,99999))
    touch(f'{randomDirName}/{randomFileName}') #create file in local directory
    
    webServer(randomDirName)
    sleep(1)
    assert randomFileName in requests.get(f'http://localhost:8081/{randomDirName}').text
    
    delete(randomDirName)    


    
def xxxxxtest_vpy_to_html(): #this test is too slow and too brittle  
    global B
    fname = 'vpytohtml_tester.py'
    delete(fname)
    

    for headless in [False, True]:
        B = BrowserFromService(headless = headless)
        print(f'\n\nexpect error, headless={headless}')
        with open(fname, 'w') as f:
                  f.write('sphere(color=color.green') #note missing paren after green
        assert 'GLOWSCRIPT ERROR' in vpy_to_html( fname, headless=headless, openBrowser=True)
        
        print(f'\\nnexpect success, headless={headless}')
        with open(fname, 'w') as f:  #now has closing paren
                  f.write("""sphere(color=color.green)
scene.caption="<a href='http://google.org'>in browser?</a>"
""")
                  
        assert 'SUCCESS' in vpy_to_html( fname, headless=headless, openBrowser=True)
        #file:///Users/jonschull-MBPR/fork/vpytohtml/vpytohtml_tester/index.html
        pathStart = pwd().strip() #/Users/jonschull-MBPR/fork/vpytohtml\
        dirName = fname.replace('.py','')
        fullURL = f'file://{pathStart}/{dirName}/index.html'
        print('FP', fullURL)
        B.get(fullURL)
        sleep(1)
        links = B.find_elements_by_partial_link_text('browser')
        assert links
        if links:
            assert links[0].text == 'in browser?'
            
        try:
            B.close()
        except:
            pass
           

