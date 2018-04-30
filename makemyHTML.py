from makemyPYJ import makeDummyPYJ
makeDummyPYJ('makemyHTML')
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

def includeInHTML():
    includeLine=0
    lines = open(sys.argv[0]).readlines()
    for i, line in enumerate(lines):
        importFlag1 = line.strip().startswith('import makemyHTML')
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

template = f"""
<html>
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

#print(template)
writeout.writeout(f'{myName}.html', template )

print(f'RS', '-b', f'{myName}.py', '-o', f'{myName}.js \n')
RS('-b', f'{myName}.py', '-o', f'{myName}.js')
plopen(f'{myName}.html')

if __name__== '__main__':
    ##LYTEML--INCLUDE THIS:
    say('this is {myName} (makemyHTML.html)')
    say(f'this is {myName} (makemyHTML.html)')
    say('<hr/>', "<i>note that variables (like myName) that can't be defined by javascript in the browser are unavailable</i>")

