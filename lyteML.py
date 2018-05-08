from lyte import say
from attrthing import AttrThing 
#from writeout import writeout

from makemyPYJ import makeDummyPYJ

import makemyPYJ

class tag(AttrThing):    
    roster=AttrThing()  #roster will be [{ID:tag, ID:tag...}]
    
    def _IDs(s=''):
        return [t._ID for t in tag.roster.values()]
    
    def make_ID(candidateID):  #to make a unique ID append str(number) to the tag name 
        if not candidateID in tag._IDs():
            return candidateID
        else:
            existingIDs = tag._IDs()
            i=1
            newCandidateID = candidateID + '-' + str(i)
            while newCandidateID in existingIDs:
                i+=1
                newCandidateID = candidateID+'-'+str(i)
            return newCandidateID

    def __init__(self, myTag, myText='', **kwargs):
        AttrThing.__init__(self)
        self._tag = myTag      # an unadorned html or xml tag such as 'p'
        self._text = myText    # the text of the tag
        self._numKids=0        # used to generate ID"numbers"
        self._IDnum='0'        # root's IDnum is 0; first child 0.0
        self._ID='H'           # root's default name
        self._kidIDnums = []   # list keeps kids in order
        self.kwargs = kwargs   # these store attributes inserted by HTML()
        tag.roster[self._IDnum] = self  #elements go into the roster indexed by _IDnum
 
    def toHTML(self):
        return HTML(self)

    def addChild(self, _tag='unknown', _text='', **kwargs):
        child = tag(_tag,_text, **kwargs)
        child._IDnum = self._IDnum + '.' + str(self._numKids) # 0, 0.0, 0.0.1, etc. later, we count dots to scale html indents 
        candidateID =    self._ID + '_' + _tag                # head_body_h1 etc.  (dots are bad in IDs) 
        child._ID = tag.make_ID(candidateID)                  # head_body_h1-2 full IDs have a number at end 
        self._kidIDnums.append(child._IDnum)                  # used with  roster to retrieve an ordered list of children()
        self._numKids += 1                                    # not used?
        tag.roster[child._IDnum]=child                        # into the roster
        self[_tag]=child                                      # define the child as a python variable (may be overwritten) 
        return child                                          # allows chaining

    def add(self, *args, **kwargs):                           # dispatches to addChild and can accommodate (_tag, _text) or ((_tag, _text),(_tag, _text)...)
        #print('args', args)
        if type(args[0]) == type('string'):                  
            if len(args) == 1:
                return self.addChild(args[0])
            else:
                return self.addChild(args[0], args[1])
        #we also handle tuples/strings 
        for arg in args:
            _tag, _text = arg
            self.add(_tag, _text) 
        
         
    def attrs(self):                                       # format attributes for tags
        if self.kwargs:
            ret=[]
            for k in self.kwargs:
                ret.append(f'{k}="{self.kwargs[k]}"')
            return ', '.join(ret)
        else:
            return ''
    
    def children(self):
        return [tag.roster[IDnum] for IDnum in self._kidIDnums]

def HTMLs(children): #collect renderings of children
    ret=[]
    for child in children:
        ret.append(HTML(child))
    if ret:
        return '\n'.join(ret)
    else:
        return ''
    
def HTML(t): #insert renderings of children (recursively) into renderings of self
    def make_indents(ID='0.0'):
        if not '.' in ID:
            return ''
        indent='  '
        indents = []
        for i in range(ID.count('.')):
            indents.append(indent)
        return(''.join(indents))    
    indent = make_indents(t._IDnum)
    return f"""{indent}<{t._tag} id="{t._ID}" {t.attrs()}>\t\t\t{t._text}
{HTMLs(t.children())}{indent}</{t._tag}>
"""### ^^^^^^^^^^^^^^  we recurse into children by way of HTMLs


H = tag('html')
    
    
import makemyHTML

if say():

    ##LYTEML--INCLUDE
    say('this is lyteML')

    H = H.add('html')  #tag is called implicitly by add and addChild, but we have to start somewhere.
    H.add('head')                                                                      # creates H.head
    H.add('body').add('h1',     'lyteML')                                              # you can chain adds
    H.body.add('p',             "lyte <b>M</b>arkup <b>L</b>anguage")                  # inline HTML works
    H.body.add('h1',            'another heading')                                     # creates H.body.h1 (etc.)
    H.body.add('h2',            'the <i>add</i> command')                              # overwrites H.body.h1 (but preserves the element)
    H.body.add('p',             "Text strings are optional; can include <i>html</i>")  #inline HTML works


    H.body.add('h2',            '<i>add</i>s can be chained and take lists of pairs')
    H.body.add('span',             "(view the <i>__main__</i> clause of <a href='lyteML.py'>lyteML.py</a> source to see how that works)")  #inline HTML works
    H.body.add('ol', 'Here is a list').add(['li', 'item'],
                                           ['li', 'another item'] )                    # you can provide add with a series of [_tag, _text] pairs
    
    H.body.add('h2',              'use <i><b>addChild</b></i> to set attributes')
    H.body.add('p','                (like "border=1" in tables)')                      # use addChild to slip in attributes like border=1
    H.body.addChild('table', border=1)
    H.body.table.add('tr').add( ('td',    'row 1 cell 1'),                             # refer to H.body.table to build it out
                                ('td',    'row 1 cell 2'))
                                
    H.body.table.add('tr').add( ('td',    'row 2 cell 1'),
                                ('td',    'row 2 cell 2'))
    
    H.body.add('pre',           """
                                    Multi-line strings
                                    are 
                                    convenient...
                                """)
    
    H.body.add('hr')      
    H.body.add('p',             """
                                For live browser updates, try <b>
                                <a href="https://www.browsersync.io/#install">
                                   browser-sync
                                </a>
                                start --server --files *.html</b>
                                """)

    say(HTML(H))   #this generates the HTML
