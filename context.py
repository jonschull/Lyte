try:
    if globals(): language='Python'
except ReferenceError:
    language = 'Rapydscript'

try:
    if alert: context = 'browser'
except :
    context='commandline'
    
def say(s):
    if context=='browser':
        document.body.innerHTML+= s + '</br>'
    else:
        print(s)    

say(language + ' via ' + context)
say('next...we do imports...')
