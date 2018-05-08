from lyte import say, whereami, blurt

from vpython import box, cone, color

import makemyVPHTML

if whereami(__name__).visible:
    box()
    cone(color=color.orange)
    say('say')
    print('print')
    blurt('blurt')

