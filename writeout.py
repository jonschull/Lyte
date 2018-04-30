#create dummy pyj so rapydscript doesn't stumble on "import writeout"
with open('writeout.pyj', 'w') as file:  
    file.write("""def writeout(*args, **kwargs): pass
""")
    

def writeout(fname, content):
    f=open(fname,'w')
    f.write(content)
    f.close()
    print('writeout.py created', fname)


if __name__=='__main__':
    writeout('test.html', '<i>hello world</i>')