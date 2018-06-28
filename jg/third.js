// Splits library: https://github.com/nathancahill/Split.js
var splits = Split(['#sourcetext', '#glows', "#printing"], {sizes: [50,40,20], onDrag:splitdrag})
// splits.getSizes() returns current percentage widths; splits.setSizes([w1,w2]) resets them

//jg June21. Move to runCode
var lastwindowwidth = window.innerWidth
// GSedit.init("#sourcetext", source, 0.5*lastwindowwidth, false) // not readonly

function splitdrag() {
	var s = splits.getSizes() // returns [width1, width2, width3]
	lastprintwidth = splits.getSizes()[2]
	GSedit.setwidth(0.01*s[0]*window.innerWidth)
}

function splitAdjust() {  // p is true if print pane should be open
	var current = splits.getSizes()
	var w1 = current[0]*lastwindowwidth/window.innerWidth
	var w2 = current[1]
	var w3 = current[2]
	var rest = 100-w1
	lastwindowwidth = window.innerWidth
	if (printpane) {
		if (lastprintwidth === null) splits.setSizes([w1,0.7*rest,0.3*rest])
		else splits.setSizes([w1,rest-lastprintwidth,lastprintwidth])
		lastprintwidth = splits.getSizes()[2]
	} else splits.setSizes([w1,rest,0])
	GSresize(0.01*w1*window.innerWidth)
}

$(window).resize(function () {
	splitAdjust()
})

window.onbeforeunload = undefined // execute window.onbeforeunload = Quit if GSedit.changed() is true

function Quit(e) { // Some browsers just say "Do you want to leave this site? Changes you made may not have been saved."
   var s = "To continue without saving, click OK.\nTo save, click Cancel, then click save."
   e.returnValue = s
   return s
}

// https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
function download(filename, text) {
	var element = document.createElement('a');
	element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	element.setAttribute('download', filename);
	element.style.display = 'none';
	document.body.appendChild(element);
	element.click();
	document.body.removeChild(element);
}

var lastname = '' // the file name chosen the last time the user saved code

function saveCode() {
	var name = prompt("Enter the file name (without extension)", lastname)
	if (name === null) return
	lastname = name
	var extension = '.py'
	if (!GSedit.isPython()) extension = '.js'
	if (exporting) extension = '.html'
	download(name+extension, GSedit.getValue())
}

function reportScriptError(program, err) { // This machinery only gives trace information on Chrome
    // The trace information provided by browsers other than Chrome does not include the line number
    // of the user's program, only the line numbers of the GlowScript libraries. For that reason
    // none of the following cross browser stack trace reporters are useful for GlowScript:
    // Single-page multibrowser stack trace: https://gist.github.com/samshull/1088402
    // stacktrase.js https://github.com/stacktracejs/stacktrace.js    https://www.stacktracejs.com/#!/docs/stacktrace-js
    // tracekit.js; https://github.com/csnover/TraceKit
    var feedback = err.toString()+'<br>'
    var prog = program.split('\n')
    //for(var i=0; i<prog.length; i++) console.log(i, prog[i])
    var unpack = /[ ]*at[ ]([^ ]*)[^>]*>:(\d*):(\d*)/
    var traceback = []
    if (err.cursor) {
        //console.log('err.cursor',err.cursor)
        // This is a syntax error from narcissus; extract the source
        var c = err.cursor
        while (c > 0 && err.source[c - 1] != '\n') c--;
        traceback.push(err.source.substr(c).split("\n")[0])
        //traceback.push(new Array((err.cursor - c) + 1).join(" ") + "^") // not working properly
    } else {
        // This is a runtime exception; extract the call stack if possible
        try {
            // Strange behavior: sometimes err.stack is an array of end-of-line-terminated strings,
            // and at other times it is one long string; in the latter case we have to create rawStack
            // as an array of strings.
            var rawStack
            if (typeof err.stack == 'string') rawStack = err.stack.split('\n')
            else rawStack = err.stack
            //for (var i=0; i<rawStack.length; i++) console.log(i, rawStack[i])

            // TODO: Selection and highlighting in the dialog
            var first = true
            var i, m, caller, jsline, jschar
            for (i=1; i<rawStack.length; i++) {
                m = rawStack[i].match(unpack)
                if (m === null) continue
                caller = m[1]
                jsline = m[2]
                jschar = m[3]
                if (caller.slice(0,3) == 'RS_') continue
                if (caller == 'compileAndRun') break
                if (caller == 'main') break

                var line = prog[jsline-1]
                if (window.__GSlang == 'javascript') { // Currently unable to embed line numbers in JavaScript programs
                    traceback.push(line)
                    traceback.push("")
                    break
                }
                var L = undefined
                var end = undefined
                for (var c=jschar; c>=0; c--) {  // look for preceding "linenumber";
                    if (line[c] == ';') {
                        if (c > 0 && line[c-1] == '"') {
                            var end = c-1 // rightmost digit in "23";
                            c--
                        }
                    } else if (line[c] == '"' && end !== undefined) {
                        L = line.slice(c+1,end)
                        break
                    } else if (c === 0) {
                        jsline--
                        line = prog[jsline-1]
                        c = line.length
                    }
                }
                if (L === undefined) continue
                var N = Number(L)-1
                if (first) traceback.push('At or near line '+N+': '+window.__original.text[N-1])
                else traceback.push('Called from line '+N+': '+window.__original.text[N-1])
                first = false
                traceback.push("")
                if (caller == '__$main') break
            }
        } catch (ignore) {
        }
    }
    for (var i= 0; i<traceback.length; i++) feedback += '<br>'+traceback[i]
    gsErrordiv = $("#gserrors")[0]
    gsErrorHandler(feedback)
}

//runCode()
//https://stackoverflow.com/questions/23813607/how-to-wait-for-an-element-to-be-defined-in-javascript
