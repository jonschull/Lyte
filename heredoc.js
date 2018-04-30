function hereDoc(f) {
                      return f.toString().
                          replace(/^[^\/]+\/\*!?/, '').
                          replace(/\*\/[^\/]+$/, '');
                    }
