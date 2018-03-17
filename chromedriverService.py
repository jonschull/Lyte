import requests as R
from   selenium import webdriver
from   selenium.webdriver.common.keys import Keys  
import selenium.webdriver.chrome.service as service
from   selenium.webdriver.chrome.options import Options

#CDS is the URL to an active Chrome Driver Service 

#try to find last chromedriver
def CDSfromFile():
    try:
        lastChromeDriver= open('chromedriver.txt').read()
    except FileNotFoundError:
        lastChromeDriver=0
    return lastChromeDriver
    

def isActive( lastCDS ):
    if lastCDS: # let's see if it's active
        try:
            r = R.get(lastCDS)
            print('lastChromeDriver ', lastCDS, 'is active'  )
            serviceURL = lastCDS
            return True
        except Exception as e:
            print( type(e), '-->',  'lastChromeDriver', 'is not active')
            serviceURL = lastCDS
            lastCD = 0
 
def newCDS():
    global service
    #https://duo.com/decipher/driving-headless-chrome-with-python    
    print('Starting chromedriverService at...', end='')
    service = service.Service('/usr/local/bin/chromedriver')
    service.start()
    CDS=service.service_url
    print( CDS )
    return CDS

 
def BrowserFromService( CDS, headless = False):
    
    chrome_options = Options()  
    if headless:
        chrome_options.add_argument("--headless")
        
    chrome_options.binary = '/usr/local/bin/chromedriver'
    capabilities = chrome_options.to_capabilities()
    #print('capabilities', capabilities)

    Browser = webdriver.Remote(CDS, desired_capabilities = capabilities)

    f=open('chromedriver.txt','w')
    f.write(CDS)
    f.close()
    
    return Browser
    
    
def getCDS():
    lastCDS = CDSfromFile()
    print('lastCDS', lastCDS)

    if isActive( lastCDS ):
        CDS = lastCDS
    else:
        CDS = newCDS()
    return CDS
 
if __name__== '__main__':

    B = BrowserFromService(getCDS(), headless=False )
    
    print('going to google.com')
    B.get('http://google.com')
    print(B.find_element_by_tag_name('body').text)
