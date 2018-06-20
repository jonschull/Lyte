Lyte
=================

This is a framework for coding python in the browser, and on the web.

To run the program click  the green "Show __Live__" button above.

Based on Rapydscript, which transpiles python-like code into javascript, Lyte allows you to edit pure python files.  If you write code in Rapydscript-compatible python, your pure-python files will work under  Rapydscript *and* python (this can help with debugging, and sanity-checking).

Your Project
------------

### ← README.md

That's this file.

### ← index.html

Includes just enough javascript to enable rapydscript to install python.py files into rapydscript's virtual file system.  In this case we install lyte.py and a few test files.

Change the pyInstall entries in index.html to install other python files.

Open the browser's developer tools to see error messages, console.log, and rapydscript "print" outputs.


### ← lyte.py

Adds a convenient say() function that "prints" to document.body.html.
With lyte imported, "say('hello world!')" works.

Also adds convenient Keys, Values, and Items functions to make javascript Objects (defined by {} in javascript) act more like python dictionaires (defined by {} in python!).

### ← compileThis*.py
For demonstrating how pyInstall works.  

Note that pyInstall does not do a python import.  YOU do that, either in the html file's doMain() function or in one of the python files you have already imported.  (For example, compiledThis3  imports compiledThis2.)  

Variables, functions and classes accessible within doMain() should be usable in the console.

### ← style.css

CSS files add styling rules to your content.

### ← script.js

Lyte is all about making python importable, but you can still include javascript.  

Once loaded, Javacript variables, functions, and classes should be usable by python modules, however, the python files will no longer be testable as stand-alones.  


### ← assets

Drag in `assets`, like images or music, to add them to your project.

Note: I think glitch wants rapydscript files to go into assets.  I haven't done that here but you may need to do some tweaking if you clone this project.

### Author

Jon Schull, jschull@gmail.com, a python programmer who has tried to learn just enough javascript to not need javascript.  
-------------------
