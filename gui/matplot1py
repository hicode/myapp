# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np

import sqlite3
cn=sqlite3.connect(r'C:\Users\c52139\Desktop\py\mt4csv.db') #(r'd:\autotrade\tradeData.db')
cn.row_factory=sqlite3.Row
cur=cn.cursor()
#cur.execute('select * from weight_distribute1 order by c')
cur.execute('select * from wd')  # create view wd as select count(*) weight, price c from min1k_exp group by price
#create view wd as select count(*) weight, close c from min5k group by close
weights=[]
prices=[]
for r in cur.fetchall():
    #weights.append(r[0])
    #prices.append(r[1])
    weights.append(r['weight'])
    prices.append(r['c'])
plt.plot(weights,prices)
plt.show()

w0=weights[prices.index('1225.75')]
w1=weights[prices.index('1179.30')]
w2=weights[prices.index('1166.85')]
w3=weights[prices.index('1213.85')]
w4=weights[prices.index('1195.65')]
plt.plot([w0,w1,w2,w3,w4],[1225.75, 1179.30, 1166.85, 1213.85, 1195.65],'ro')
plt.show()

w0=weights[prices.index('13320')]
w1=weights[prices.index('13171')]
w2=weights[prices.index('12625')]
w3=weights[prices.index('12860')]
w4=weights[prices.index('13025')]
plt.plot([w0,w1,w2,w3,w4],[13320,13171,12625,12860,13025],'ro')
plt.show()

'''
i1=prices.index(12100)
i2=prices.index(14200)
plt.plot(weights[i1:i2],prices[i1:i2])
w=weights[prices.index(13171)]
plt.plot([w],[13171],'ro')
plt.show()


plt.plot([1,2,3,5,8,13],marker='*') #linestyle='', 
plt.ylabel('y')
plt.show()
plt.plot([0,2,3],[1,2,3],c='r',marker='*',linestyle='-',linewidth=1) #linestyle='', 
#plt.axis=([0,6,1,7])
plt.xlim(0,6)
plt.ylim(1,7)
plt.show()

'''
t=np.arange(0,1,0.2)  #(0,5,0.2)
ln1,ln2,ln3=plt.plot(t,t,'r*-',t,t**2,'bs',t,t**3,'g^-',linewidth=3) #linestyle='', 
plt.plot(t,t*2,marker='o')
plt.show()

fig=plt.figure()
ax=fig.add_subplot(223)


x=random(1000)
hist(x)
show()

from pylab import *
