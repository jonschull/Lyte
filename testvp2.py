from lyte import say, whereami, explain, blurt

from mockvpython import box, cone, color

import makemyVPHTML

whereami = explain(__name__)

if whereami.visible:
    box()
    cone()
    say('say')
    print('print')
    blurt('blurt')
