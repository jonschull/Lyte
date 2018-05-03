from makemyPYJ import makeDummyPYJ, sameWords, makemyPYJ
makeDummyPYJ('makemyVPHTML')
makeDummyPYJ('sys')
makeDummyPYJ('writeout', ['writeout'])
makeDummyPYJ('plumbum',['local'])

import sys
import writeout
from lyte import say
from plumbum import local
RS = local['/Users/jonschull-MBPR/rapydscript-ng/rapydscript-ng/bin//rapydscript']
plopen = local['open']


myName = sys.argv[0].replace('.py','')
see = local['see']
def edit():
    see(f'{myName}.html')

lines = open(sys.argv[0]).readlines()
    
hasVPimport = False
for i,line in enumerate(lines):
    if sameWords(line, 'from vpython import *'):
        lines[i] = '##commented out by makemyHTML##' + line
        hasVPimport = True
print('\nhasVPimport',hasVPimport)
    
def includeInHTML():
    global lines
    includeLine=0
    for i, line in enumerate(lines):
        importFlag1 = line.strip().startswith('import makemyVPHTML')
        importFlag2 = line.strip().startswith('##LYTEML--INCLUDE') #to avoid recursive import in makemyHTML
        flaggedLine = importFlag1 or importFlag2
        if flaggedLine:
            if importFlag1: firstChar = 'i'
            if importFlag2: firstChar = '#'
            includeLine = i + 1
            indented = line.find(firstChar)
    if includeLine:
        
        lines = [line[indented:] for line in lines]
        return ''.join(lines[includeLine:])
    

my__main__ =  includeInHTML()


simpleTemplate= f"""<html>
    <head>
        <meta charset="UTF-8" />
        <script type="text/javascript" src="rapydscript.js"></script>
        <script type="text/javascript" src="heredoc.js">    </script>
        <script type="text/javascript" src="{myName}.js">   </script>
    </head>
    <body>
    </body>
    <script type="text/javascript">var compiler = RapydScript.create_embedded_compiler();
    eval(compiler.compile(hereDoc(`##### Python zone begins 






{my__main__}







## Python zone ends`))); </script> </html>  """


VPtemplate = f"""<html>
    <head>
        <meta charset="UTF-8" />
        <script type="text/javascript" src="rapydscript.js"></script>
        <script type="text/javascript" src="heredoc.js">    </script>
        <script type="text/javascript" src="{myName}.js">   </script>


    <link type="text/css" href="supportScripts/jquery-ui.custom.css" rel="stylesheet" />
    <link type="text/css" href="supportScripts/ide.css" rel="stylesheet" />
    <script type="text/javascript"  src="supportScripts/jquery.min.js"></script>
    <script type="text/javascript"  src="supportScripts/jquery-ui.custom.min.js"></script>
    <script type="text/javascript"  src="supportScripts/glow.2.7.min.js"></script>
    <script type="text/javascript"  src="supportScripts/RSrun.2.7.min.js"></script>
    <script type="text/javascript"  src="supportScripts/heredoc.js"></script>
    <script charset="UTF-8"         src="supportScripts/rapydscript.js"></script>
    <script type="text/javascript"  src="supportScripts/GlowScript.js"></script>
        
    </head>
    <body>
        <div id="glowscript" class="glowscript">
        </div>  

    </body>
    <script type="text/javascript">var compiler = RapydScript.create_embedded_compiler();
    var MYVP = compiler.compile(hereDoc(`##### Python zone begins 






{my__main__}







## Python zone ends`)); </script> </html>  """

if hasVPimport:
    template = VPtemplate
else:
    template = simpleTemplate

#print(template)
writeout.writeout(f'{myName}.html', template )

print(f'RS', '-b', f'{myName}.py', '-o', f'{myName}.js \n')

if hasVPimport:
    makemyPYJ(myName = myName + '.py') #make PYJ
    RS('-b', f'{myName}.pyj', '-o', f'{myName}.js')    #compile the PYJ
else:
    RS('-b', f'{myName}.py', '-o', f'{myName}.js')     #compile the PY

plopen(f'{myName}.html')

if __name__== '__main__':
    ##LYTEML--INCLUDE THIS:
    say('this is {myName} (makemyHTML.html)')
    say(f'this is {myName} (makemyHTML.html)')
    say('<hr/>', "<i>note that variables (like myName) that can't be defined by javascript in the browser are unavailable</i>")

