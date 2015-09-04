# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
plt.plot([1,2,3,5,8,13],marker='*') #linestyle='', 
plt.ylabel('y')
plt.show()
plt.plot([0,2,3],[1,2,3],c='r',marker='*',linestyle='-',linewidth=1) #linestyle='', 
#plt.axis=([0,6,1,7])
plt.xlim(0,6)
plt.ylim(1,7)
plt.show()
t=np.arange(0,5,0.2)
ln1,ln2,ln3=plt.plot(t,t,'r*-',t,t**2,'bs',t,t**3,'g^-',linewidth=3) #linestyle='', 
plt.plot(t,t*2,marker='o')
plt.show()
fig=plt.figure()
ax=fig.add_subplot(223)
