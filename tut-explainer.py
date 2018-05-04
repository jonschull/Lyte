from lyte import explain, say

say('top saying', __name__, str(say()))
print('top printing', __name__, str(say()))


import makemyHTML
if say():
    say('saying', __name__, str(say()))
    print('printing', __name__, str(say()))
