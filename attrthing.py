rapydscriptVersion = """
try:
    from pythonize import strings
    context='RAPYDSCRIPT'
    strings()
    from __python__ import dict_literals, overload_getitem
except ModuleNotFoundError:
    context='PYTHON'
    #from attrthing import AttrThing as DICT

#print('context', context)

class AttrThing():
    def __init__(self,*args, **kwargs):
        if len(args)==1:
            if type(args[0])==type({}): #convert an object into a DICT
                #self._germ='{}'
                obj=args[0]
                keys= Object.keys(obj)
                values= Object.values(obj)
                for i in range(len(keys)):
                   k=keys[i]
                   v=values[i]
                   self[k]=v
                   #print(k,v,'\t',end='')
            else:
                if type(args[0])==type(dict()): #convert a dict
                    d=args[0]
                    #self._germ='dict()'
                    for k,v in zip(d.keys(), d.values()):
                        if not k.startswith('_'):
                            self[k]=v
                    
            
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
        return '{' + ''.join(ret) + '}'
        
def tests():
    D=AttrThing(a=1,b=2)
    D['c']=3
    D.d=4
    D[6]=6 ##########################NOTE: 6 becomes "6"
    D[7]='seven'
    D['phrase with spaces'] =  5
    #D(c='c-redux')
    print('D[7]', D[7])
    print('keys\t',   D.keys())
    print('values\t', D.values())
    print('items\t',  D.items())
    print('D\t',      D)
    print('str(D)\t', str(D))

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
        super(AttrThing, self).__init__(**kwargs)
        
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
        return '{' + ''.join(ret) + '}'


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
    #		 Note: Return keys() and values() as lists to allow indexing via a.keys()[0]
    #['THIS', 'THAT'] 
    #		 Note: a('this','that') returns a list

    
    a.l=[1,2,3]
    a.t=(1,2,3)
    print(a.l, 'should be list !!!') #note
    #[1, 2, 3] should be list !!!
    
    print(a.l, a('l'), a['l'], a.l ==a('l')==a['l'], 'all accessors return the same thing')
    #[1, 2, 3] [1, 2, 3] [1, 2, 3] True all accessors return the same thing
    a.l.append('this fails with the more sophisticated but mysterious https://pypi.python.org/pypi/attrdict')
    print( a.l )
    #[1, 2, 3, 'this fails with the more sophisticated but mysterious https://pypi.py
    
    #print(a.PreDefined_nonStandardAttr)
    #__getattr:__for PreDefined_NonStandarAttr, arbitrary code  function calls can go in __getattr_
    
    #print(a.not_Predfined_and_not_standard) #raises exception
    #AttributeError: __getattr__ failed to help with attrnamenot_Predfined_and_not_standard


