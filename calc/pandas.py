from datetime import datetime
now = datetime.now()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

randn = np.random.randn


df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
 'B': ['B0', 'B1', 'B2', 'B3'],
 'C': ['C0', 'C1', 'C2', 'C3'],
 'D': ['D0', 'D1', 'D2', 'D3']},
 index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
 'B': ['B4', 'B5', 'B6', 'B7'],
 'C': ['C4', 'C5', 'C6', 'C7'],
 'D': ['D4', 'D5', 'D6', 'D7']},
 index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
 'B': ['B8', 'B9', 'B10', 'B11'],
 'C': ['C8', 'C9', 'C10', 'C11'],
 'D': ['D8', 'D9', 'D10', 'D11']},
 index=[8, 9, 10, 11])

frames = [df1, df2, df3]
result = pd.concat(frames)





df = pd.DataFrame({'key1':['a','a','b','b','a'],
				'key2':['one','two','one','two','one'],
				'data1':randn(5),
				'data2':randn(5)})

df
grouped = df.groupby(df['key1'])
grouped.mean()
df['data1'].groupby(df['key1']).mean()
df.groupby(df['key2'])['data2'].mean()
df.groupby([df['key1'],df['key2']]).mean()
grouped.size()

for i,j in df.groupby([df['key1'],df['key2']]):
        print(i)
        print('-----------')
        print(j)

df.groupby('key1')['data1']
df['data1'].groupby('key1')

df.groupby({0:'a',1:'a',2:'b',3:'b',4:'a'}).mean()
df.groupby(lambda x:'even' if x%2==0 else 'odd').mean()
index = pd.MultiIndex.from_arrays([['even','odd','even','odd','even'],
                                  [0,1,2,3,4]],names=['a','b'])
df.index = index
df.groupby(level='a').mean()



df = pd.DataFrame({'row' : [0,1,2],
					'One_X' : [1.1,1.1,1.1],
					'One_Y' : [1.2,1.2,1.2],
					'Two_X' : [1.11,1.11,1.11],
					'Two_Y' : [1.22,1.22,1.22]}); 





x1 = pd.to_datetime(now)
x2 = pd.to_datetime(np.nan)

dates = [datetime(2011,1,1), datetime(2011,1,2), datetime(2011,1,3), datetime(2011,2, 3), datetime(2012,1,3)]
ts = pd.Series(randn(5), index=dates)

# time series, timestamp 
ts['2011-1']
ts['2012']
ts['2011-2':'2012']
pd.date_range('20110101', '20110110')
pd.date_range(start='20150101',periods=10)
pd.date_range(end='20150101',periods=10)
pd.date_range('20110101', '20110610', 'BM')
pd.date_range('00:00', '12:00', freq='1h20min')

ts.shift(2)
ts.shift(-2)
ts.shift(2, freq='3D')

# period
p=pd.Period(2010, freq='M')
p+2
pd.period_range('2010-01', '2010-05', freq='M')


# 重采样（resampling）指的是将时间序列从一个频率转换到另一个频率的过程。pandas 对象都含有一个 .resample(freq, how=None, axis=0, fill_method=None, closed=None, label=None, convention='start', kind=None, loffset=None, limit=None, base=0) 方法用于实现这个过程
ts = pd.Series(np.random.randn(5),index=pd.period_range('201001','201105',freq='M'))
ts = pd.Series(range(12),index=pd.period_range('201101','201112',freq='M'))
ts.resample('2M', how='max')

s = Series(randn(5), index=['a', 'b', 'c', 'd', 'e'])
s + s
s - s
s * s
s / s
s * 2

s = Series(randn(5))
s[0]

sa = Series([1,2,3],index=list('abc'))
sa.a
sa['a']
sa.b
Series(5., index=['a', 'b', 'c', 'd', 'e'])


d = {'one' : Series([1., 2., 3.], index=['a', 'b', 'c']), 'two' : Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
df = DataFrame(d)
df.one
df.one.a
df.a # ???

DataFrame(d, index=['d', 'b', 'a'])
DataFrame(d, index=['d', 'b', 'a'], columns=['two', 'three'])
df.index
df.columns
	

d = {'one' : [1., 2., 3., 4.], 'two' : [4., 3., 2., 1.]}
df1 = DataFrame(d)

DataFrame(d, index=['a', 'b', 'c', 'd'])











import pandas as pd

url = 'https://raw.github.com/pydata/pandas/master/pandas/tests/data/tips.csv'
tips1 = pd.read_csv(url)
tips2 = pd.read_csv(r'D:\bak\s\db\tips.csv')
tips.head()

s = pd.Series([1,3,5,np.nan,6,8])
s

dates = pd.date_range('20130101',periods=6)
dates

df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list(��ABCD��))
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list(��ABCD��))
df

#<TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
#EURUSD,20010102,230100,0.9507,0.9507,0.9507,0.9507,4
#EURUSD,20010102,230200,0.9506,0.9506,0.9505,0.9505,4
#EURUSD,20140530,185900,1.3638,1.3639,1.3638,1.3639,4
#EURUSD,20140530,190000,1.3638,1.3638,1.3629,1.3629,4
tips = pd.read_csv(r'C:\Users\c52139\Documents\marketdata-yun\EURUSD.txt')
tips = pd.read_csv(r'C:\Users\c52139\Documents\marketdata-yun\EURUSD.txt', names=['pid','date','time','o','h','l','c','vol'])
tips = pd.read_csv(r'C:\Users\c52139\Documents\marketdata-yun\EURUSD.txt', header=0, names=['pid','date','time','o','h','l','c','vol'])
