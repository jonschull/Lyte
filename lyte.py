import pyonly

#we need a copy of this file for rapydscript to import
pyonly.make_lyte_pyj()

#determine language
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
    
def appendToBody(s):
    """ this is called by say if we are in the browser """
    document.body.innerHTML+= s + '<br/>\n'
    
def say(s):
    if context=='browser':
        appendToBody(s)
    else:
       print(s)
       
def alert_(s):
    try:
        alert(s) #will work in browser
    except:
        say(s)  #will work otherwise

if __name__=='__main__':
    say(  f'saying:   {language} in {context}')  #Lyte REQUIRES PYTHON3
    print(f'printing: {language} in {context}')
    alert_(f'alerting: {language} in {context}')
    #appendToBody('body??')

