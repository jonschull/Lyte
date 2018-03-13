import sys
pyName=sys.argv[0]

def make_lyte_pyj():
    mytext=open('lyte.py').read()
    pyj=open('lyte.pyj','w')
    pyj.write(mytext)
    pyj.close()


def makeHTMLandJS(openBrowser=True):
    HTMLname = pyName.replace('.py', '.html')
    JSname =   pyName.replace('.py', '.js'  )

    print(f':::: making {JSname} and {HTMLname}::::')
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
    #print(content)
    
    from plumbum import local
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
    rs('-x', pyName)
    rs(pyName, '-o', JSname)
    if openBrowser:
        browser=local['open']
        browser(HTMLname)
    
    
def runRapydscript():
    from plumbum import local
    rs=local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
    print('---rapydscript---')
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