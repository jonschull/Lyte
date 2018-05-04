from lyte import say, whereami, explain

from vpython import box, cone, color

import makemyVPHTML

box()
cone(color=color.red)
say('is this thing on')

whereami = explain(__name__)
if whereami.visible:
    print('once now?')