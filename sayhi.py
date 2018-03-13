from lyte import say, language, context, alert_
#print('doc', document)
#if context != 'browser': alert=print

if __name__=='__main__':
    say(    f'saying:   {language} in {context}')  #Lyte REQUIRES PYTHON3
    print(  f'printing: {language} in {context}')
    alert_(f'alerting: {language} in {context}')
    if context=='browser':
        say('')
        say('look in the console for print output')

import pyonly

#pyonly.runRapydscript()

pyonly.makeHTMLandJS()
