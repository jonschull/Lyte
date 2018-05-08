"""
This currently assumes that we are running from a directory in which everything works
and building the system in a sibling directory calld 7VP.

Obviously, this should be generalized.

"""
newdir = '../8lyte/'


from plumbum import local
mkdir = local['mkdir'] #will crash if directory exists
mkdir(newdir)

cp = local['cp']

cp('lyteBuild.py'      , f'{newdir}')
cp('tut-H.py'          , f'{newdir}tut-H.py')
cp('tut-explainer.py'  , f'{newdir}tut-explainer.py')
cp('a.py'              , f'{newdir}a.py')
cp('b.py'              , f'{newdir}b.py')
cp('lyte.py'           , f'{newdir}')
cp('lyteML.py'         , f'{newdir}')
cp('makemyPYJ.py'      , f'{newdir}')
cp('makemyHTML.py'     , f'{newdir}')
cp('attrthing.py'      , f'{newdir}')
cp('writeout.py'       , f'{newdir}')
cp('rapydscript.js'    , f'{newdir}')
cp('heredoc.js'        , f'{newdir}')
cp('readme.txt'        , f'{newdir}')
cp('testVP.py'         , f'{newdir}')
cp('makemyVPHTML.py'   , f'{newdir}')
cp('vpython.pyj'       , f'{newdir}')
cp('beginswith.py'     , f'{newdir}')
cp('testvp.py'         , f'{newdir}')
cp('lyteBuild.py'      , f'{newdir}')

mkdir(f'{newdir}supportScripts')
cp('-R', 'supportScripts/'  , f'{newdir}supportScripts/')

mkdir(f'{newdir}lyte3 architecture')
cp('-R', 'lyte3 architecture/'  , f'{newdir}lyte3 architecture/')


building = False
if building:
    py3=local['python3']

    #this creates PYJs that subsequent modules need
    print(py3(f'{newdir}attrthing.py'))
    print(py3(f'{newdir}lyte.py'))
    print(py3(f'{newdir}makemyPYJ.py'))
    #print(py3(f'{newdir}makePYJs.py'))
    print(py3(f'{newdir}lyteML.py'))
    print(py3(f'{newdir}a.py'))
    print(py3(f'{newdir}b.py'))
    print(py3(f'{newdir}beginswith.py'))
    print(py3(f'{newdir}testvp.py'))







