import time
import win32com.client



from threading import Timer

def executeEvery(seconds,callback):
    def f():
        callback()
        t = Timer(seconds,f)
        t.start()
    def stop():
        t.cancel()
        
    t = Timer(seconds,f)
    t.start()
    
    return stop    
        
def printHello():
    print('hello')


def sendPgdn():
    wsh.SendKeys( "{PGDN}" )


wsh = win32com.client.Dispatch( "Wscript.Shell" )

#executeEvery(1,printHello)


pass

for i in range(100000000):
    #time.sleep(0.1)
    wsh.SendKeys( "{PGDN}" )
    #time.sleep(0.1)
    #wsh.SendKeys( "{HOME}" )
    #time.sleep(0.1)
    #wsh.SendKeys( "^{LEFT}" )

