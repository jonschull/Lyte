if __name__=='__main__':
    import makemyPYJ

try:
    from pythonize import strings
    strings()
except ModuleNotFoundError:
    pass

def blurt(word):
    try:
        alert(word)
    except NameError:
        print(word)
    return '--blurt'

def say(*args):
    args=[str(arg) for arg in args]
    s=''.join(args)
    try:
        GSprint(s)
        return '--say'
    except:
        pass
    
    NOBREAK=False
    if args:
        if args[-1] == 'NOBREAK':
            args=args[0:-1]
            NOBREAK = True
    try:
        el=document.getElementById('lyte')
        el.innerHTML+=s
        if not NOBREAK:
            el.innerHTML+='<br/>'
    except NameError:
        print(s)
    except TypeError: #this happens with glowscript 
        print(s)
    return('--say')
        

def oldsay(*args):
    """ output arguments like print, only to document.body.innerHTML, if possible.
        if it IS possible, return 1; else 0
        if no arguments given, output nothing (but still return 1 or 0)
        accept 'NOBREAK' as last argument to suppress '<br/>\n'
    """
    NOBREAK = False
    if args:
        if args[-1] == 'NOBREAK':
            args=args[0:-1]
            NOBREAK = True
    
    s=' '.join(args)
    verbose=False
    if language == 'RS':
        try:
            if s:
                if NOBREAK:
                    document.body.innerHTML +=  s
                else:
                   document.body.innerHTML += s+'<br/>\n'
            else:
                document.body.innerHTML += ''
            return 1
        except TypeError:
            if verbose:
                print(f'browserhead:: {s}')
            else:
                if s:
                    if NOBREAK:
                        print(s, end='') #is there way to suppress carriage return??
                    else:
                        print(s)
            return 0
        except ReferenceError:
            if verbose:
                print(f'rapydscript shell:: {s}')
            else:
                if s:
                    if NOBREAK:
                        print(s) #is there way to suppress carriage return??
                    else:
                        print(s)
            return 1
    else: #language is Python
        if verbose:
            print(f'python shell:: {s}')
        else:
            if s:
                if NOBREAK:
                    print(s, end='')
                else:
                    print(s)
        return 1




def inPythonZone():
    if language == 'RS':
        try:
            document.body.innerHTML# +=  s  + '<br/>\n'
        except TypeError:
            return 0
        except ReferenceError:
            return 0
    return 1


try: 
    if globals(): language='Python'
except ReferenceError:
    language = 'RS'
    try:
        if dir(vpython): #works when we have imported vpython (not mockvpython)
            language = 'GS'
    except:
        pass
    
try:  #if this works, we're in the browser
    document
    context='browser'
except NameError:
    context='shell'


def visible(whereami):
    if whereami.name =='__embedded__' and whereami.context == 'browser': return True
    if whereami.name == '__main__'    and whereami.context == 'shell':   return True
    try:
        GSprint
        return True
    except:
        return False

def whereami(__name__):
    from attrthing import AttrThing
    ret = AttrThing(language=language, context=context,  name=__name__)
    if context=='browser':
        if __name__ == '__embedded__':
            ret.headBody = 'body'
        else:
            ret.headBody='head'
    else:
        ret.headBody = 'NA'
    ret.visible = visible(ret)
    return ret


if __name__ == '__main__':
    say(str(whereami(__name__)))
