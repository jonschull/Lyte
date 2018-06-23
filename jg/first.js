var gsversion = 2.7
var printpane = false
var exporting = false // not currently in export mode
var lastprintwidth = null

var glowscript_run = undefined
window.Jupyter_VPython = undefined
if (!navigator.onLine) window.Jupyter_VPython = 'glowscript_data/' // get textures when offline
// TAB at end of line should lengthen the line; implement Ctrl-1 and Ctrl-2



function fontloading() { // trigger loading of fonts for 3D text
    "use strict";
	// override the fontloading url's in the GlowScript library
	if (window.__font_sans === undefined) {
		var fontrefsans = opentype_loadjs(Roboto_sans) // a sans serif font
		window.__font_sans = fontrefsans // an opentype.js Font object
	}
	if (window.__font_serif === undefined) {
        var fontrefserif = opentype_loadjs(Nimbus_serif) // a serif font
		window.__font_serif = fontrefserif // an opentype.js Font object
	}
}
fontloading() // get the sans and serif font files used by 3D text

// localCompile is a modification of https://github.com/BruceSherwood/glowscript/blob/master/ide/ide.js
function localCompile(header, compReady, errordiv) {

     //jsg
    document.getElementById('sourcetext').style.width='10%'
    document.getElementById('glows').style.width='50%'
    //jsg

	errordiv.innerHTML = ""
    var compiler_url
    if (header.lang == 'vpython' || header.lang == 'rapydscript') {
        compiler_url = "glowscript_libraries/RScompiler." + header.version + ".min.js"
    } else compiler_url = "glowscript_libraries/compiler." + header.version + ".min.js"
    window.glowscript_compile = undefined
    $.ajax({
        url: compiler_url,
        dataType: "script",
        cache: true,
        crossDomain: true  // use script tag rather than xhr
    }).fail(function (xhr, err, exc) {
        (xhr)
        alert(err + " getting " + xhr.url + ": " + exc)
    }).done(function () {
        if (!window.glowscript_compile) {
            alert("Failed to load compiler from " + compiler_url)
            return
        }

        var embedScript
        try {
            embedScript = window.glowscript_compile(header.source, {lang: header.lang,
                version: header.version.substr(0,3)})
        } catch(err) { // need to decrement 3 -> 2 in Error: Missing right parenthesis, see line 3: b = box(pos=37
            err = err.toString() // gets the error message
            var patt = new RegExp('line(\\s*)([0-9]*):')
            var m = err.match(patt)
            if (m !== null) {
                var colonindex = m.index + 4 + m[1].length + m[2].length
                var n = parseFloat(m[2])-1
                err = err.slice(0,m.index)+'line '+n+err.slice(colonindex)
            }
            errordiv.innerHTML = "<p>"+err+"</p>"
            return
        }
                compReady(embedScript)
     })
}

function parseVersionHeader( source ) {
    var sourceLines = source.split("\n")
    var header = sourceLines[0]
    // Remove a newline or similar character at the end of header:
    if (header.charCodeAt(header.length-1) < 32)
        header = header.substring(0,header.length-1)
    var rest = source.substring( header.length+1 )
    var ret = {
        version: null,
        lang: '', // 'vpython' (default) or 'rapydscript' or 'javascript' or a string that is neither (e.g. when editing header)
        source: rest,
        ok: false,
        unpackaged: false,
        isCurrent: false
    }
    header = header.split(" ")
    if (header.length === undefined) return ret
    if (header[0] == ' ') return ret
    var elements = []
    for (var i=0; i<header.length; i++) { // remove empty strings corresponding to spaces
        if (header[i] != '') elements.push(header[i])
    }
    if (elements.length < 2 || elements.length > 3) return ret
    if (elements[0] != 'GlowScript') return ret
    ret.lang = 'javascript' // the default if no language is specified
    if (elements.length == 3) {
        ret.lang = elements[2].toLowerCase()
        if (!(ret.lang == 'javascript' || ret.lang == 'rapydscript' || ret.lang == 'vpython')) return ret
    }
    var ver = elements[1]
    if (ver != gsversion) alert('The version number, '+ver+', should be '+gsversion)
    var okv = true
    return {
        version: ver,
        lang: ret.lang,
        source: rest,
    }
}

function getHeader(exporting) {
    var text = GSedit.getValue()
    var end = text.indexOf('\n')
    var i = text.slice(0,end).indexOf("GlowScript") // Look for "GlowScipt" in first line
    var j = text.slice(0,end).indexOf("vpython")    // Look for "vpython" in first line
    if (i < 0 && j) text = "GlowScript "+gsversion+" VPython" + "\n" + text
    var header = parseVersionHeader(text)
    printpane = false
    if (header.source.search(/print\s*\(/) >= 0) { // if the program uses print() or GSprint(), expand 3rd pane
    	printpane = true
        if (!exporting) {
            var end = header.source.indexOf('\n')
            var insert
            if (header.lang == 'vpython' || header.lang == 'rapydscript')
                 insert = "print_options(place=$('#printing'),  width=300, height=500, clear=True)\n"
            else insert = "print_options({place:$('#printing'), width:300, height:500, clear:true})\n"
            header.source = header.source.slice(0,end+1) + insert + header.source.slice(end+1)
        }
    }
    // Look for mention of MathJax in program and attempt to get it (need internet access; files too big to include in package)
    if (header.source.indexOf('MathJax') >= 0) {
        alert('Cannot currently use MathJax in GlowScript Offline.')
    }
    return header
}

var gsErrordiv
var savecode = null

function runCode() {
  var lastwindowwidth = window.innerWidth
  GSedit.init("#sourcetext", source, 0.5*lastwindowwidth, false) // not readonly

	var header = getHeader(false)
	//splitAdjust()
    gsErrordiv = $("#gserrors")[0]
    localCompile(header, ready, gsErrordiv, false)
}

function ready(program) {
    var w = $("#glows")
    w[0].innerHTML = "" // Comment this and the next if get a solution for too many WebGL context
    w[0].innerHTML = '<div id="glowscript" class="glowscript"></div>'

    try {
        window.userMain = eval(program)
        // At this point the user program has not been executed.
        // Rather, eval_script has prepared the user program to be run.

        //$("#loading").remove()
        window.__context = {
            glowscript_container: $("#glowscript")
        }
        window.userMain(function (err) {
            if (err) {
                reportScriptError(program, err)
            }
        })
    } catch (err) {
        reportScriptError(program, err);
    }
}

function exportCode() {
	if (savecode !== null) { // Restore operation
		exporting = false
		GSedit.setValue(savecode)
		savecode = null
	    $("#export").html('Export')
	} else { // Export operation
		exporting = true
		var header = getHeader(true)
	    gsErrordiv = $("#gserrors")[0]
	    localCompile(header, showcode, gsErrordiv)
	}
}

function showcode(sc) {
	// In creating the string embedHTML it was necessary to break 'script' into 'scr'+'ipt' to avoid problems parsing GlowScript.html
	var exporturl = "https://s3.amazonaws.com/glowscript/"
	var verdir = '2.1'
    var divid = "glowscript"
    var embedHTML = (
        '<div id="' + divid + '" class="glowscript">\n' +
        '<link type="text/css" href="'+exporturl+'css/redmond/' + verdir + '/jquery-ui.custom.css" rel="stylesheet" />\n' +
        '<link href="https://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet" type="text/css" />\n' +
        '<link type="text/css" href="' + exporturl + 'css/ide.css" rel="stylesheet" />\n' +
        '<scr'+'ipt type="text/javascript" src="' + exporturl + 'lib/jquery/' + verdir + '/jquery.min.js"></scr'+'ipt>\n' +
        '<scr'+'ipt type="text/javascript" src="' + exporturl + 'lib/jquery/' + verdir + '/jquery-ui.custom.min.js"></scr'+'ipt>\n' +
        '<scr'+'ipt type="text/javascript" src="' + exporturl + 'package/glow.' + gsversion + '.min.js"></scr'+'ipt>\n' +
        '<scr'+'ipt type="text/javascript" src="' + exporturl + 'package/RSrun.' + gsversion + '.min.js"></scr'+'ipt>\n' +
        '<scr'+'ipt type="text/javascript"><!--//--><![CDATA[//><!--\n' +
        ';(function() {' +
        sc +
        '\n;$(function(){ window.__context = { glowscript_container: $("#glowscript").removeAttr("id") }; main(__func) })})()\n' +
        '\n//--><!]]></scr'+'ipt>' +
        '\n</div>')
    savecode = GSedit.getValue()
    GSedit.setValue(embedHTML)
    startcursor = 0
    endcursor = embedHTML.length
    setTimeout(resetCursor, 30) // experimentally, can't correctly update cursor position here
    $("#export").html('Restore')
}

var startcursor
var endcursor
var resetCursor = function() {
    GSedit.editarea[0].focus()
    GSedit.editarea[0].setSelectionRange(startcursor,endcursor)
}

function gsErrorHandler(err) {
    gsErrordiv.innerHTML = "<p>"+err+"</p>"
}

function readSingleFile(evt) {
	exporting = false
	var ok = true
	if (GSedit.changed()) {
		var s = "To continue without saving, click OK.\nTo save, click Cancel, then click Save."
		if (confirm(s)) ok = true
		else ok = false
	}
	if (ok) {
		savecode = null
	    $("#export").html('Export')
	    var f, reader
	    f = evt.target.files[0]
	    if (f) {
	        reader = new FileReader()
	        reader.onload = function(e) {
	        	var content = e.target.result
	        	GSedit.setValue(content)
	        }
	        reader.readAsText(f)
	    }
	}
}
document.getElementById('read_local_file').addEventListener('change', readSingleFile, false)
