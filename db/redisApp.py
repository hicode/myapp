# coding=utf-8

from redis import Redis,StrictRedis

#from gevent import monkey
#monkey.patch_socket()
import time
from celery import Celery

#BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://localhost:6379/2'
celery = Celery('tasks', broker=BROKER_URL)

#@celery.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')

@celery.task
def add(x, y):
    return x + y


'''
r_server = StrictRedis("192.168.137.148") #"localhost")
p = r_server.pipeline() # transaction=False

#p.set('one', 'first').rpush('list', 'hello').rpush('list', 'world').execute()  
#p.set('hello','redis').sadd('faz','baz').incr('num').execute()

fldLen = 10
iLst = range(3000)

msetVal = {}
for i in iLst:
    msetVal["mst%d"%(i)] = "DeGizmo123"*fldLen
t1 = time.time()
r_server.mset( msetVal )
print( time.time()-t1 )

t1 = time.time()
for i in iLst:
    a=p.set("name%d"%(i), "DeGizmo123"*fldLen)
p.execute()
print( time.time()-t1 )

t1 = time.time()
for i in iLst:
    b=r_server.get("name%d"%i)
print( time.time()-t1 )

mgetKeyL = msetVal.keys()
t1 = time.time()
b=r_server.mget( mgetKeyL )
print( time.time()-t1 )

r = Redis(host='localhost', port=6379, db=0)   #如果设置了密码，就加上password=密码
r.set('foo', 'bar')   #或者写成 r['foo'] = 'bar'
r.get('foo')
r.delete('foo')
r.dbsize()   #库里有多少key，多少条数据
r['test']='OK!'
r.save()   #强行把数据库保存到硬盘。保存时阻塞
r.flushdb()   #删除当前数据库的所有数据
a = r.get('chang')
dir(a)
r.keys()   # 列出所有键值。（这时候已经存了4个了）

info = r.info() 
for key in info: 
  print( "%s: %s" % (key, info[key]) )

'''