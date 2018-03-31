from pyonly2 import enLytenMe, runMe
try: 
    if globals(): language='Python'
except ReferenceError:
    language = 'Rapydscript'
    
#determine context
try:  #if this works, we're in the browser
    document.body.innerHTML+= '<hr/>\n' 
    context='browser'
except:
    context='shell'
    
def _appendToBody(s):
    """ this is called by say if we are in the browser """
    document.body.innerHTML+= s + '<br/>\n'
    
def say(s):
    """prints to screen or webpage"""
    if context=='browser':
        _appendToBody(s)
    else:
       print(s)
       
def blurt(s):
    """uses alert in browser; uses say otherwise"""
    try:
        alert(s) #will work in browser
    except:
        say(s)  #will work otherwise
        
print = print #so people can go lyte2.print()

if __name__=='__main__':
    say(  f'saying:   {language} in {context}')  #Lyte REQUIRES PYTHON3
    print(f'printing: {language} in {context}')
    blurt(f'alerting: {language} in {context}')

    print('hello from lyten. 12:57')

    enLytenMe()  #this creates the HTML folder

    runMe(openBrowser=True)

