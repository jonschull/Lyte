// pyFiles that have been pyInstalled can be imported and made global here
async function main(){
  await pyInstall('utils.py') //includes filterImports used by getSource
  await forGlobalEnvt()
  await forGlowScript()
  await runCode()
}
main()


function forGlobalEnvt(){window.eval(compiler.compile(`

from utils import filterImports

`,options = {'basedir':'__stdlib__','omit_baselib':true} )) ////////////////////////
}
//doMain


//pyFiles defined here are turned into GlowScript source.  Then executed by runCode.
async function forGlowScript(){
  source=''
  source += await getSource('cone.py')
  source += await getSource('layerouter.py')
  source += await getSource('main.py') 
}
