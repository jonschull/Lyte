TESTING = True#__name__ == '__main__'

EQUALTO='EQUALTO'
IN = 'IN'
ERROR='ERROR'

VERBOSE = False
SHOWRS = False

class AttrDict(dict): #http://code.activestate.com/recipes/576972-attrdict/;
    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.__dict__ = self
        
RESULTS = AttrDict(yes=0, no=0)


if TESTING:
    if VERBOSE:
        print('IS?  Line')          

def IS(a='', condition=EQUALTO, b='',hint='' ):
    import inspect
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)[1][3]
    question = inspect.getouterframes(curframe, 2)[1][-2][-1].strip()
    lineNumber = inspect.getouterframes(curframe, 2)[1][-4]

    if (a=='' and condition==EQUALTO and b==''):
        return lineNumber
    
    if not condition in [EQUALTO, IN, ERROR]:
        print (f'BADCONDITION at line {lineNumber}', condition)
        return
    
    nice = question.replace('IS(','IS(\t ')
    nice=nice.replace('IN',     '\t\t\t\t\t IN\t')
    nice=nice.replace('EQUALTO','\t\t\t\t\t EQUALTO\t')
    
 
    if (condition == 'EQUALTO' and a == b) or \
       (condition == 'IN'      and a in b):
       if VERBOSE: print(f'yes {lineNumber:3}    {nice}')
       RESULTS.yes += 1
       return

    print('='*80)
    print(f' re ||NO:   {nice}')
    print(f"""line|||||                    |{a:1}|\t\t\t\t\t          x x x x   
{lineNumber:3} ||||||||is NOT {condition:8}  |{b}|""")
    RESULTS.no +=1
    