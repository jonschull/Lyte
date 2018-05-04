from vpython import *
stuff = dir()
filteredStuff = [thing for thing in stuff if not thing.startswith('__')]
#print(filteredStuff)
f=open('vpython.pyj','w')
for thing in filteredStuff:
    f.write(f'def {thing}(*args, **kwargs): pass\n')
f.close()