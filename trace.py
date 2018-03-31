import traceback

def trace(*args, **kwargs):
    global lines, stack, ret
    ret = ''
    stack= traceback.format_stack()
    #stack.reverse()
    print('Your call sequence:')
    for i,line in enumerate(stack[1:-2]):
        lines=line.split('\n')
        lines[0] = lines[0].split('/')[-1].replace(',','\t\t\t')
        if not lines[0].startswith('backend'):
            ret = f'step{i:2}  {lines[0]}\t\t\t\t' +  lines[1].replace('args',f'{args}')
            #print('\n', ret.split(),'\n')
            word, step, file, word, line, word, caller, called = ret.split()[:8]
            other = ''.join(ret.split()[7:])
            file=file.replace('"','')
            print(f'line {line:3}\t\t{other} \t\t\t\t\t\t\t {file}')

def trace_caller(*args,**kwargs):
    trace()
    
def trace_caller_caller(*args,**kwargs):
    trace_caller()
    

if __name__=='__main__':
    trace_caller_caller(10)
