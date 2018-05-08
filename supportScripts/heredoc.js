// allows multi-line strings
// https://stackoverflow.com/questions/805107/creating-multiline-strings-in-javascript?rq=1
function hereDoc(f) {
                      return f.toString().
                          replace(/^[^\/]+\/\*!?/, '').
                          replace(/\*\/[^\/]+$/, '');
                    }
