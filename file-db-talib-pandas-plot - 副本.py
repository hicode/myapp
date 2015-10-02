# coding=utf-8
import sys
sys.path.append(r"D:\ssd-e-bak\new\ali\dor\bak sure\s\good\MBSC-Upgrade")

from autoTest import VosTool
fLst = VosTool.getFileLst(        r'C:\new_tdx\vipdoc\sh\lday', '', False )
fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\sz\lday', '', False )
fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\ds\lday', '', False )

from ctypes import *
class dayK_TDX(Structure):
     _fields_ = [ ('date',c_int), ('o',c_int), ('h',c_int), ('l',c_int), ('c',c_int), ('amnt',c_float), ('vol',c_int), ('pre_c',c_int) ]

class dayK_THS(Structure):
     _fields_ = [ ('date',c_int), ('o',c_int), ('h',c_int), ('l',c_int), ('c',c_int), ('amnt',c_float), ('vol',c_int),
      ('rsv1',c_int) , ('rsv2',c_int), ('rsv3',c_int), ('rsv4',c_int), ('rsv5',c_int), ('rsv6',c_int), ('rsv7',c_int), ('rsv8',c_int), ('rsv9',c_int), ('rsv10',c_int),
      ('rsv11',c_int) , ('rsv12',c_int), ('rsv13',c_int), ('rsv14',c_int), ('rsv15',c_int), ('rsv16',c_int), ('rsv17',c_int), ('rsv18',c_int), ('rsv19',c_int), ('rsv20',c_int),
      ('rsv21',c_int) , ('rsv22',c_int), ('rsv23',c_int), ('rsv24',c_int), ('rsv25',c_int), ('rsv26',c_int), ('rsv27',c_int), ('rsv28',c_int), ('rsv29',c_int), ('rsv30',c_int),
      ('rsv31',c_int) , ('rsv32',c_int), ('rsv33',c_int), ('rsv34',c_int), ('rsv35',c_int) ]

import sqlite3
conn = sqlite3.connect( r'D:\dayk1.db' )
cur = conn.cursor()
cur.execute( 'create table if not exists dayK(pid, date, o, h, l, c, amt, vol, divi)')
cur.execute( 'create table if not exists dayK1(pid, date, o, h, l, c, amt, vol, divi)')
conn.commit()

#insert into dayk1 select pid,date,o/divi,h/divi,l/divi,c/divi,amt,vol,divi from dayk

k1=dayK_TDX()
rec = {}

#f.readinto(k1)
#k1.date, k1.amnt, k1.vol, k1.o, k1.h, k1.l, k1.c, k1.pre_c
#cur.execute( 'insert into dayK values ("%s", %s, %s, %s, %s, %s, %s, %s)' % ( 'sz000001', k1.date, float(k1.o)/100, float(k1.h)/100, float(k1.l)/100, float(k1.c)/100, float(k1.amnt)/10000, k1.vol/10000) )
#conn.commit()


#replace into
#prepared statment


import os
for f in fLst:
  fp = open(os.path.join( f[1], f[0] ), "rb")
  pid = f[0].split('.')[0]
  while fp.readinto(k1):
    cur.execute( 'insert into dayK values ("%s", %s, %s, %s, %s, %s, %s, %s)' % ( pid, k1.date, float(k1.o)/100, float(k1.h)/100, float(k1.l)/100, float(k1.c)/100, float(k1.amnt)/10000, k1.vol/10000) )
  #executemany()
  fp.close()

conn.commit()

'''
  #k1.date, k1.amnt, k1.vol, k1.o, k1.h, k1.l, k1.c, k1.pre_c
  rec['product'] = fname
  rec['dt'] = k1.date
  rec['o'] = k1.o
  rec['h'] = k1.h
  rec['l'] = k1.l
  rec['c'] = k1.c
  rec['amt'] = k1.amt
  rec['vol'] = k1.vol
  colRecInserted = '"%s"' % name
  for fld in rec:
      recInserted = '%s,"%s"' % ( recInserted , rec[fld] )
      cols = '%s,"%s"' % ( cols, fld )
  cur.execute( 'insert into "%s" (%s) values(%s)' % ( tblName, cols[1:], recInserted[1:] ) )
'''
f.close()



import talib
import pandas as pd

url = 'https://raw.github.com/pydata/pandas/master/pandas/tests/data/tips.csv'
tips1 = pd.read_csv(url)
tips = pd.read_csv(r'D:\bak\s\db\tips.csv')
tips.head()

outputs = talib.SMA(tips1.tip.values, timeperiod=5)

dayk000001 = pd.read_sql_query('select * from dayK where pid="sz000001"', conn)
sma5 = talib.SMA( dayk000001.c.values, timeperiod=5)
sma10 = talib.SMA( dayk000001.c.values, timeperiod=10)
sma20 = talib.SMA( dayk000001.c.values, timeperiod=20)
sma60 = talib.SMA( dayk000001.c.values, timeperiod=60)

cci14 = talib.CCI( dayk000001.h.values, dayk000001.l.values, dayk000001.c.values)

#<TICKER>,<DTYYYYMMDD>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
#EURUSD,20010102,230100,0.9507,0.9507,0.9507,0.9507,4
#EURUSD,20010102,230200,0.9506,0.9506,0.9505,0.9505,4
#EURUSD,20140530,185900,1.3638,1.3639,1.3638,1.3639,4
#EURUSD,20140530,190000,1.3638,1.3638,1.3629,1.3629,4
tips2 = pd.read_csv(r'E:\迅雷下载\压缩包任务组_20140727_2050\EURUSD.txt')
tips2 = pd.read_csv(r'E:\迅雷下载\压缩包任务组_20140727_2050\EURUSD.txt', names=['pid','date','time','o','h','l','c','vol'])
tips2 = pd.read_csv(r'E:\Stk_DAY_FQ_20150227\SH600600.csv', header=0, names=['pid','date','time','o','h','l','c','vol'])
tips2 = pd.read_csv(r'E:\Stk_DAY_FQ_20150227\SH600600.csv', header=1)
tips2 = pd.read_csv(r'E:\Stk_DAY_FQ_20150227\SH600601.csv', skiprows=1, names=['pid','date','o','h','l','c','amt','vol', 'divi'])
sma5 = talib.SMA( tips2.c.values, timeperiod=5)
sma10 = talib.SMA( tips2.c.values, timeperiod=10)
sma20 = talib.SMA( tips2.c.values, timeperiod=20)
sma60 = talib.SMA( tips2.c.values, timeperiod=60)
cci14 = talib.CCI( tips2.h.values, tips2.l.values, tips2.c.values)

tips2.to_sql('dayk3', conn, if_exists='append')
#start 52:46 54:46




import sys
sys.path.append(r"E:\new\ali\dor\bak sure\s\good\MBSC-Upgrade")

from autoTest import VosTool
fLst = VosTool.getFileLst( r'E:\Stk_DAY_FQ_20150227', '', False )

import pandas as pd
import sqlite3
conn = sqlite3.connect( r'D:\dayk1.db' )

import os
for f in fLst:
  tips2 = pd.read_csv(os.path.join( f[1], f[0] ), skiprows=1, names=['pid','date','o','h','l','c','amt','vol', 'divi'])
  tips2.to_sql('dayk', conn, if_exists='append')

cur.execute( 'create table if not exists dayK1(pid, date, o, h, l, c, amt, vol, divi)')
