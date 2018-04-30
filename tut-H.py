from lyte import say

from lyteML import H

import makemyHTML
if say():
    say('Here is how I develop using the lyte system.')
    say('<h1> Introducing the H object from lyteML.py</h1>')

    H = H.add('html')
    H.add('body')
    H.body.add('h2', 'Look ma, no tags')
    H.body.add('ul')
    H.body.ul.add('li', 'item?')
    H.body.ul.add('li', 'second item?')

    H.body.add('h2', 'see the nicely formatted HTML below?  We generate unique IDs too')
    H.body.addChild('h2','For more information, see <a href="lyteML.html">lyteML.html</a> and lytemMLpy')

    say( H.toHTML()  )
