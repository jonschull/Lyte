Lyte
=================

This is a framework for coding python in the browser, and on the web.

Based on Rapydscript, which transpiles python-like code into javascript, Lyte allows you to edit pure python files.  (These  will also run with the python compiler, if they are written in the subset of python rapydscript supports.)

Your Project
------------

### ← README.md

That's this file.

### ← index.html

Includes just enough javascript to enable rapydscript and install python.py files into rapydscript's virtual file system.  In this case we install lyte.py.

You can change pyInstall lines to include other python files.

Note: because Glitch insists that the root html file be called index.html, I manually set rootName to "lyte", in order to ensure that lyte.py is exported.
In other contexts (such as offline development), you should uncomment the line that derives rootName from the windowLocation.  This allows you to work on multiple projects at the the same time in the same directory.  

When rootName is set automatically from windowLocation, you can name your html file "whatever.html", and it will automatically pyInstall, import and run whatever.py.  

Open the browser's developer tools to see error messages, console.log, and rapydscript "print" outputs.


### ← lyte.py

Adds a convenient say() function that "prints" to the document.body.html.
With lyte imported, "say('hello world!')" works.

Also adds convenient Keys, Values, and Items functions to make javascript Objects (defined by {} in javascript) act more like python dictionaires (defined by {} in python!).

### ← compileThis*.py
For demonstrating how pyInstall works.  

Note that pyInstall does not do a python import.  YOU do that, either in doMain() or in one of the python files you have already imported.  (That is, compiledThis3 can import compiledThis2.)  

### ← style.css

CSS files add styling rules to your content.

### ← script.js

Lyte is all about making python importable but you can still include javascript.  Variables, functions, and objects imported to your HTML file from script.js and from python files) are accessible from the console.  

### ← assets

Drag in `assets`, like images or music, to add them to your project.

Note: I think glitch wants rapydscript files to go into assets.  I haven't done that here but you may need to do some tweaking if you clone this project.

### Author

Made by Jon Schull, jschull@gmail.com, a python programmer who has tried to learn just enough javascript to not need javascript.  
-------------------

\ ゜o゜)ノ