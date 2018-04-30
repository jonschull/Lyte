"""
This currently assumes that we are running from a directory in which everything works
and building the system in a sibling directory calld 6best.

Obviously, this should be generalized.

"""

from plumbum import local
cp = local['cp']
cp('lyteBuild.py'  , '../6best/')
cp('H.py'          , '../6best/tut-H.py')
cp('explainer.py'  , '../6best/tut-explainer.py')
cp('a.py'          , '../6best/a.py')
cp('b.py'          , '../6best/b.py')
cp('lyte.py'       , '../6best/')
cp('lyteML.py'     , '../6best/')
cp('makemyPYJ.py'  , '../6best/')
cp('makePYJs.py'   , '../6best/')
cp('makemyHTML.py' , '../6best/')
cp('attrthing.py'  , '../6best/')
cp('writeout.py'   , '../6best/')
cp('rapydscript.js', '../6best/')
cp('heredoc.js'    , '../6best/')
cp('readme.txt'    , '../6best/')


