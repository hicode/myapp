from statsmodels.regression.tests.glmnet_r_results import rslt_0
try:
    # py3
    from urllib.request import Request, urlopen
    #from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    #from urllib import urlencode

from multiprocessing.dummy import Pool as ThreadPool 

urls = [
    'http://hq.sinajs.cn/list=sz160125',
    'http://hq.sinajs.cn/list=sh600585', 
    #'http://hq.sinajs.cn/list=sz002594', 
    #'http://hq.sinajs.cn/list=sh510900', 
    #'http://ichart.yahoo.com/table.csv?s=600000.ss&a=01&b=01&c=1990&d=08&e=31&f=2015&g=d', 
    #'http://ichart.yahoo.com/table.csv?s=002594.sz&a=01&b=01&c=1990&d=08&e=31&f=2015&g=d', 
    #'http://ichart.yahoo.com/table.csv?s=160125.sz&a=01&b=01&c=1990&d=08&e=31&f=2015&g=d',
    ]

rslt = []
import os
import sys

def dataFromUrl(url):
    import contextlib
    global rslt, lock
    try: 
        req = Request( url )
        with contextlib.closing( urlopen(req, timeout=10) ) as resp:
            x = resp.read()
    except:
        str = 'thread pid/name:%s/%s, url: %s\r\n' % (os.getpid(), threading.currentThread().getName(), url)
        sys.stdout.write( str)
        return
    #lock.acquire()
    str = 'thread pid/name:%s/%s, url: %s\r\n' % (os.getpid(), threading.currentThread().getName(), url)
    sys.stdout.write( str )
    rslt.append( x )
    #lock.release()

import threading

# Make the Pool of workers
pool = ThreadPool(1) 
# Open the urls in their own threads
# and return the results
lock = threading.RLock()
#for url in urls[3:]:
#dataFromUrl(urls[-1])

results = pool.map(dataFromUrl, urls)
#close the pool and wait for the work to finish 
pool.close() 
pool.join()


import multiprocessing

import time

def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1

def worker1(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1

def worker2(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1
'''
if __name__ == '__main__':
  p = multiprocessing.Process(target = worker, args = (3,))
  p.start()
  print "p.pid:",pdpid
  print "p.name:", p.name
  print "p.is_alive:", p.is_alive()
  
  main()
  urlList = []
  histRec = {}
  maxProcNum = 9
  for url in urlList:
      createprocess()
      
'''
