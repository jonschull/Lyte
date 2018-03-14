from lyte import say

def illuminate( someKeyConcepts='formatted strings, parameters, and values' ):
    
    say("The def command defines a command.")
    say('This one is called "simple"')
    say(f"to illustrate {someKeyConcepts} ")

if __name__== '__main__':
    illuminate( 'the idea of the parameter.  We pass parameters to commands.' )
    
    someKeyConcepts = "that variables can be changed.  That's why they are called variables"
    
import lyte
lyte.webMe()