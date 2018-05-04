from lyte import explain, say, blurt, whereami

import makemyVPHTML

whereami = explain(__name__)

if whereami.visible:
    say(whereami)
    say('once in shell, once in browser')
    say(1,2,3,'four')
    


