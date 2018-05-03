from lyte import explain, say, blurt, visible, whereami

import makemyHTML

whereami = explain(__name__)
    
if whereami.name =='__embedded__' and whereami.context == 'browser':
    print('ok once just in browser')
    
if visible(whereami):
    print('once in shell, once in browser')


