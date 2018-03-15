def XXXmake_pyj():
    from sys import argv
    pyName = argv[0]
    pyjName   = pyName.replace('.py', '.pyj')
    pycode=open(pyName).read()
    pyj   =open(pyjName,'w')
    pyj.write(pycode)
    pyj.close()

def make_pyjs():
    from sys import argv
    pyName = argv[0]
    ###import make_pyjs
    #make_pyjs.make_pyjs(pyName) #for some reason this makes rapydscript try to import sys
    #                            # and fail. Whereas my_pyj above does not cause the sys failure
    from plumbum import local
    python3 = local['python3']
    print( python3('make_pyjs.py', pyName)  )
    
make_pyjs()  #THIS IS AUTOMATICALLY EXECUTED WHEN PYONLY.py IS IMPORTED UNDER PYTHON
    
def makeHTMLandJS(openBrowser=True):
    from sys import argv
    pyName = argv[0]
    HTMLname = pyName.replace('.py', '.html')
    JSname =   pyName.replace('.py', '.js'  )

    print(f'::webME:: making {JSname} and {HTMLname}::::')
    HTMLfile = open(HTMLname, 'w')
    content = f""" <html>
        <head> <meta charset="UTF-8"> 
         </head>
        <body>
           <script type="text/javascript" language="javascript" src="{JSname}">
           </script>
        </body>
    </html>"""
    
    HTMLfile.write(content)
    HTMLfile.close()
    from plumbum import local
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']

    rs(pyName, '-o', JSname)
    if openBrowser:
        browser=local['open']
        browser(HTMLname)
 
    
def runRapydscript():
    from plumbum import local
    from sys import argv
    pyName = argv[0]
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
    print('\n >>rRS>> rapydscript -x', pyName,'\n')
    print(rs('-x', pyName) )


#create dummy pyonly.pyj with dummy functions for rapydscript
pyjFile=open('pyonly.pyj','w')
pyjFile.write('#### pyj is here to satisfy Rapydsript import ####\n\n')
for dirObj in dir():
    if not dirObj.startswith('__'):
        if not dirObj == 'pyjFile':
            pyjFile.write(f'def {dirObj}(*args, **kwargs): pass\n')     
pyjFile.close()

if __name__=='__main__':
    print('can not test makeHTMLandJS() with itself')
    print('test by running....    python3 sayhi.py    ')
    #print(relevantPyFiles('lyte.py'))
