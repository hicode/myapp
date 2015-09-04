import time
t1 = time.time()
from gevent import monkey
monkey.patch_socket()
import redis
r_server = redis.Redis("localhost")
for i in xrange(1000000):
    a=r_server.set("name", "DeGizmo")
    b=r_server.get("name")

print time.time()-t1
