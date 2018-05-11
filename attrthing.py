#!/usr/bin/env python3
def typer(thing):
    strType = str(type(thing))
    typeID = strType.split('{')[0].strip()
    typeID = typeID.replace('function ','').replace('()','')
    return "<" + typeID + ">"


rapydscriptVersion = """
try:
    from pythonize import strings
    context='RAPYDSCRIPT'
    strings()
    from __python__ import dict_literals, overload_getitem
except ModuleNotFoundError:
    context='PYTHON'

def typer(thing):
    strType = str(type(thing))
    typeID = strType.split('{')[0].strip()
    typeID = typeID.replace('function ','').replace('()','')
    return "<" + typeID + ">"

class AttrThing():
    def __init__(self,*args, **kwargs):
        #print('args', args, 'kwargs', kwargs,'  len(args)', len(args))
        if len(args)==1: #dict, attrthing or object to be re-typed
            thing = args[0]
            if 1: #typer(thing) == typer(dict()):
                for k,v in thing.items():
                    self[k]=v
        else:
            for kwarg in kwargs:
                self[kwarg]=kwargs[kwarg]

    def __call__(self, *args, **kwargs):
        print('in __call__', args, kwargs)
        for k,v in kwargs.items(): #allow a(this='this', that='that') for existing object
            #self[k]=v
            self.__setattr__(k,v)
  
    def keys(self):
        l= [key for key in Object.keys(self) if not key.startswith('_')]
        l.sort()
        return l
          
    def values(self):
        vs=[]
        for k,v in zip(Object.keys(self), Object.values(self)):
            if not k.startswith('_'):
                vs.append(v)
        vs.sort()
        return vs
        
    def items(self):
        l=[]
        for k in self.keys():
            l.append((k, self[k]))
        l.sort()
        return l
        
    def __next__(self):
        return 'next'
        
    def __repr__(self):
        ret = []
        for k in self.keys():
            ret.append(f"'{str(k)}'")
            ret.append(': ')
            if type(self[k]) == type('string'):
                ret.append('"' + self[k] + '"')
            else:
                ret.append(str(self[k]))
            ret.append(', ')
        ret.pop() #trailing comma
        return '<{' + ''.join(ret) + '}>'

def tests():
    print('==========')
    print(AttrThing(dict(a=1,b=2))) #worked
    print(AttrThing({'a':1,'b':2})) #worked
    print(AttrThing(AttrThing(a=1,b=2))) #worked
    print(AttrThing(a=1,b=2)) #sanity check (works)
        

if __name__=='__main__':
    tests()

"""

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

from writeout import writeout

writeout(f'{dir_path}/attrthing.pyj', rapydscriptVersion)

class AttrDict(dict): #http://code.activestate.com/recipes/576972-attrdict/;
    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.__dict__ = self
        
verbose=False
class AttrThing(AttrDict):
    """  AttrThing does what AttrDict does
         also
         can return multiple elements
         returns keys() and values() as lists to support indexing
         does not turn lists into tuples (c.f., https://pypi.python.org/pypi/attrdict')
    """
    def __init__(self, *args, **kwargs):
        super(AttrThing, self).__init__(*args, **kwargs)
        
    def __call__(self, *args, **kwargs):
        #print('in __call__', args, kwargs)
        for k,v in kwargs.items(): #allow a(this='this', that='that') for existing object
            #self[k]=v
            self.__setattr__(k,v)
            
        if args:
            if len(args)==1: return self.__getitem__(args[0]) 
            
            ret=[] #but also field multiple requests and return answers as lists
            for arg in args:
                ret.append(self.__getitem__(arg))
            return ret

    def keys(self):
           l = list(super(AttrThing, self).keys())
           l = [str(k) for k in l]
           l.sort()
           return l
    
    def values(self):
        l= list(super(AttrThing, self).values())
        #we need to convert all to strings before sorting but then return the untainted values
        D={}
        for element in l:
            D[str(element)] = element
        Dkeys = list(D.keys())
        Dkeys.sort()
        l = [D[k] for k in D]
        return l
    
    def items(self):
        l= list(super(AttrThing, self).items())
        for i, item in enumerate(l):
            l[i] = list(l[i])
            l[i][0] = str(l[i][0])
        l=sorted(l)
        return l
    
    def __repr__(self):
        ret=[]
        for k,v in self.items():
            if type(k) == type(''):
                ret.append("'" + k + "'")
            else:
                ret.append(k)
            ret.append(': ')
            if type(v)==type(''):
                ret.append('"' + str(v) + '"')
            else:
                ret.append(str(v))
            ret.append(', ')
        ret.pop() #trailing comma
        return '<{' + ''.join(ret) + '}>'


if __name__=='__main__':
    a=AttrThing()
    a(first='Can be initialized this way', second='See?')
    print(a)
    print()
    #{'first': 'Can be initialized this way', 'second': 'See?'}


    del a.first, a.second
    a['this']='settable with bracket'
    print(a)
    print()
    #{'this': 'settable with bracket'}

    #like AttrDict
    a.this='settable with dot'
    print(a)
    print()
    #{'this': 'settable with dot'}


    #like AttrDict, gettable 3 ways 
    a.this='THIS'
    print(a.this, a['this'], a('this'), '\t\t', a.this==a['this']==a('this'), "\t\t Note:  a.this == a['this'] == a(this)")
    print()
    #THIS THIS THIS 		 True 		 Note:  a.this == a['this'] == a(this)

    #unlike AttrDict, keys() and values() are lists
    #print(type(a.keys()), type(a.values()), a.keys()[0], a.values()[0], '\n\t\t Note: Return keys() and values() as lists to allow indexing via a.keys()[0]')
    #<class 'list'> <class 'list'> this THIS 
    #		 Note: Return keys() and values() as lists to allow indexing via a.keys()[0]

    a.that='THAT'
    #unlike attrDict, returns multiple values if asked
    print(a('this', 'that'), "\n\t\t Note: a('this','that') returns a list")
    print()

    #new to attrThing:
    #settable after the fact as in vPython
    a(one=1,two=2,three=3)
    print(a, '\n\t\t Note: Settable after the fact via a(one=1,two=2,three=3)')
    print()

    
    a.l=[1,2,3]
    a.t=(1,2,3)
    print(a.l, 'should be list !!!') #note
    #[1, 2, 3] should be list !!!
    
    print(a.l, a('l'), a['l'], a.l ==a('l')==a['l'], 'all accessors return the same thing')
    #[1, 2, 3] [1, 2, 3] [1, 2, 3] True all accessors return the same thing
    print()
    print(AttrThing(dict(convertsFromDict = 'toAttrThing')))
    print(AttrThing({'convertsFromCurly' : 'toAttrThing'}))
    print(AttrThing(AttrThing( acceptsAT = 'and converts')))
 
