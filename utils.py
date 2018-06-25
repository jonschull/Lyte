"""
filterImports also in lyte.py
"""


try:
    from pythonize import strings
    strings()
except ModuleNotFoundError:
    print('no need for pythonize')

def filterImports(s):
  lines=s.split('\n')
  for i,line in enumerate(lines):
      if 'import' in line:
          lines[i]='##' + lines[i]
  return '\n'.join(lines)


if __name__=='__main__':
    testScript = """
from vpython import *
import vpython
import x
from y import z
box()
z()

    """

    print(filterImports(testScript))
