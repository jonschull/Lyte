
async function pyInstall(fileName){
//////////retrieve py files from filesystem, install as pyj///////////
    const response = await fetch(fileName);
    const content = await response.text()
    console.log('pyInstalling ' + fileName ) //+ ':\n content:\n ' + content)
    await compileThis(fileName + 'j', content);
}

Promise.all([    pyInstall('utils.py')  ])
  .then(doMain)
  .then(notYet)

async function notYet(){

    source= await getSource('utils.py')
    source += await getSource('cone.py')
    source += await getSource('PPGSOincrementallayout.py')
    source += await getSource('PPGSOincrementallayout_Main.py')

    await runCode()
}


function doMain(){window.eval(compiler.compile(`
#put your global imports here



from utils import filterImports




`,options = {'basedir':'__stdlib__','omit_baselib':true} )) ////////////////////////
}
