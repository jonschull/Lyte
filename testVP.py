import a
from makemyPYJ import makeDummyPYJ
makeDummyPYJ('vpython', funcNames=['box', 'cone', 'sphere', 'exec'])

from vpython import *
from vpython import box, cone

import makemyVPHTML

box() 
cone()
for i in range(3):
    print(i,'okey dokey?')