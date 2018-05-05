from lyte import say, whereami, explain, blurt

import makemyHTML
say('say')
print('print')
blurt('blurt')

whereami = explain(__name__)
if whereami.visible:
    say('say')
    print('print')
    blurt('blurt')

