from cffi.cparser import lock
from gevent._threading import RLock
threading.Event
threading.Condition
start
join
setdaemon
cancel
lock 
RLock
Queue 

import threading 
def sayhello(): 
        print "hello world" 
        global t        #Notice: use global variable! 
        t = threading.Timer(5.0, sayhello) 
        t.start() 
   
t = threading.Timer(5.0, sayhello) 
t.start() 

import time  
import thread  
def timer(no, interval):  
    cnt = 0  
    while cnt<10:  
        print 'Thread:(%d) Time:%s\n'%(no, time.ctime())  
        time.sleep(interval)  
        cnt+=1  
    thread.exit_thread()  


def test(): #Use thread.start_new_thread() to create 2 new threads  
    thread.start_new_thread(timer, (1,1))  
    thread.start_new_thread(timer, (2,2))  




import threading  
class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, interval):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.thread_stop = False  
    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:  
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            time.sleep(self.interval)  
    def stop(self):  
        self.thread_stop = True  

def test():  
    thread1 = timer(1, 1)  
    thread2 = timer(2, 2)  
    thread1.start()  
    thread2.start()  
    time.sleep(20)  
    thread1.stop()  
    thread2.stop()  
    return  
