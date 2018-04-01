from pyonly2 import *
from IS import *
import os

TESTING=True

def makePYJandJSfolderss(pyName):
    """ assumes basename directory exists """
    os.mkdir(f'{baseName(pyName)}/PYJs')
    os.mkdir(f'{baseName(pyName)}/JSs')
    pass

if TESTING:
    pyName = 'testPJs.py'
    pbDelete(baseName(pyName))
    makeFile(pyName, f"print('this is from {pyName}')" )
    ret = lyten(f'{pyName}')
    makePYJandJSfolderss(pyName)

IS('testPJs.js', IN, lsl('testPJs'))
IS('PYJs', IN, lsl('testPJs'))


def makeJSs():
    pass

