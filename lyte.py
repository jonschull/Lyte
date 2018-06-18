print('This is lyte.py.  Pure.py files in the browser. It should be used by lyte.html')

def say(*args):
    for arg in args:
        document.body.innerHTML += ' ' + str(arg).replace('\n','<br/>')

def Keys(o):
    return [k for k in o]

def Values(o):
    return [o[k] for k in o]

def Items(o):
    return list(zip(Keys(o), Values(o)))

d={'one': 1, 'two':2}

document.body.innerHTML=''
say('<h1>Demo of lyte</h1>')
say('<a href="lyte.glitch.me">http://lyte.glitch.me</a>, based on <a href="https://glitch.com/edit/#!/lyte>https://glitch.com/edit/#!/lyte">https://glitch.com/edit/#!/lyte</a>.')
say('<h2>The say() function</h2> ')
say('Say works like print, but for document.innerHTML:', 1,2,3)

say('<hr/>')
say('<h2>Keys, Values, and Items for {} objects.</h2> ')
say('  Javascript Objects {} support brackets and dot-notation:  D.one:', d.one, "d['one']==d.one", d['one']==d.one,'\n')
say('  Convenience functons make them nicer:<b> Keys(d), Values(d), Items(d) </b>\n')
say(f'   Keys(d):  <b> {Keys(d)  } </b>\n') #formatted strings are great
say(f'   Values(d):<b> {Values(d)} </b>\n')
say(f'   Items(d): <b> {Items(d) } </b>\n')
say("""<pre>
for k,v in Items(d): #python loops are nice
    say(f'{k}:{v}')
</pre>
    """)
for k,v in Items(d): #python loops are nice
    say(f'{k}:{v}    \n')
say('<hr/>')

say('<h2>Console and Devtools</h2>')
say("""With rapydscript, "print" and error messages go into the console.
Right click and choose "Inspect" to see the console and the devtools""")
print('THIS SHOULD BE IN THE CONSOLE')

say("""<hr/> <ul><h2>Theory of operation.</h2></ul>
    <li>     Rename lyte.html to whatever.html (any filename you want)
    </li>
    <li>     Create whatever.py (a python file with the matching name)
    </li>
    <li>     In whatever.html, manually <b>pyInstall</b> any other python files you want in the virtual filesystem for whatever.py to import.
    </li>
    <li>     Make sure Rapyscript.js can be found by whatever.html
    </li>
    <li>     Get on with your life.
    </li>
  </ul>
""")
