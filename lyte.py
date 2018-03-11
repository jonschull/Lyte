try:
    if globals(): language='Python'
except ReferenceError:
    language = 'Rapydscript'

try:
    if alert: context = 'browser'
except :
    context='commandline'
    
if context != 'browser':
    from pymsgbox import alert as pymsgAlert
    alert=pymsgAlert
    
def say(s):
    if context=='browser':
        document.body.innerHTML+= s + '</br>'
    else:
        print(s)    

if context == 'browser':
    print = say


if __name__=='__main__':
    say(language + ' via ' + context)
    alert('this is an alert')
