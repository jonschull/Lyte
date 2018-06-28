GlowScript in Glitch 
=================

Pure Python GlowsScript Online, and off.

This is an experimental framework for Glowscript (Vpython) in the browser, and on the web.  Based on  [Lyte](https://glitch.com/~lyte) and [GlowScript](http://GlowScript.org).

To Bruce Sherwood's [GlowScript Offline system],(https://groups.google.com/forum/#!starred/glowscript-users/Qq0rExnxOYc) it adds the ability to import pure python and as-you-type real-time recompilation.

* To run a program click in Glitch, click the green "Show __Live__" button above.
* To remix the program, you should only need to modify index.js and your own .py files

This  demo is a force-directed graph layout routine written in python-compatible glowscript (based on [this])(http://patrickfuller.github.io/jgraph/examples/ipython.html).  

Because it is written in ptyon-compatible Glowsdript the two pure python files can be run with the Python compiler or via GlowScript in the browser.  

This source is in the PPGSO branch of http://github.com/jonschull/lyte


Your Project
------------

### ← README.md

That's this file.

### ← index.html

Adds to the GlowScript Offline system just enough  javascript to enable rapydscript to install python.py files into rapydscript's virtual file system.  In this case we install utils.py.  

You should not need to modify index.html

Javascript inside index.html defines 
* pyInstall() and compile this put .py files into the Rapydscript virtual file system and makes them available as global utilties (as if they were written in javascript)
* getSource() 
  * amalgamates .py files into a variable called "source"
  * comments out the import statements that GlowScript currently rejects


### ← index.js

index.js is where _you_ specify and install your project-specific imports.
In principle, this is the only file you should need to modify

In this case, index.js 
* pyInstalls utils.py 
* makes utils.filterImports globally available 
  * you can add your own utilities this way too
* uses getSource to inject amalgamated layerouter.py + main.py into the GlowScript Offline system 
* trigger's GlowsScripts RunCode() to make it all go.
  
### ← layerouter.py and main.py
* layerouter.py contains the graph layout
* it is imported by main.py

### ← style.css

CSS files add styling rules to your content.  

### ← the jg directory

breaks glowscript.js into two sections to sandwich my stuff
* first.js
* (My stuff)
* third.js

jg-style.css tweaks the GlowScript style sheet in order to hide the GlowScript source code. (You can get it to pop back out expanding the left most pane).

### Author

Jon Schull, jschull@gmail.com, a python programmer who has tried to learn just enough javascript to not need javascript.  
-------------------
