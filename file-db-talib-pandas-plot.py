# coding=utf-8
import sys
import time
from codetools.util.cbook import unique
from pandas.core.common import notnull
from django.db.models.lookups import IsNull
sys.path.append(r"D:\ssd-e-bak\new\ali\dor\bak sure\s\good\MBSC-Upgrade")

from autoTest import VosTool
fLst = VosTool.getFileLst(        r'C:\new_tdx\vipdoc\sh\lday', '', False )
fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\sz\lday', '', False )
#fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\ds\lday', '', False )

from ctypes import *
class dayK_TDX(Structure):
     _fields_ = [ ('date',c_int), ('o',c_int), ('h',c_int), ('l',c_int), ('c',c_int), ('amnt',c_float), ('vol',c_int), ('pre_c',c_int) ]

class dayK_THS(Structure):
     _fields_ = [ ('date',c_int), ('o',c_int), ('h',c_int), ('l',c_int), ('c',c_int), ('amnt',c_float), ('vol',c_int),
      ('rsv1',c_int) , ('rsv2',c_int), ('rsv3',c_int), ('rsv4',c_int), ('rsv5',c_int), ('rsv6',c_int), ('rsv7',c_int), ('rsv8',c_int), ('rsv9',c_int), ('rsv10',c_int),
      ('rsv11',c_int) , ('rsv12',c_int), ('rsv13',c_int), ('rsv14',c_int), ('rsv15',c_int), ('rsv16',c_int), ('rsv17',c_int), ('rsv18',c_int), ('rsv19',c_int), ('rsv20',c_int),
      ('rsv21',c_int) , ('rsv22',c_int), ('rsv23',c_int), ('rsv24',c_int), ('rsv25',c_int), ('rsv26',c_int), ('rsv27',c_int), ('rsv28',c_int), ('rsv29',c_int), ('rsv30',c_int),
      ('rsv31',c_int) , ('rsv32',c_int), ('rsv33',c_int), ('rsv34',c_int), ('rsv35',c_int) ]

import sqlite3 as db

conn = db.connect( r'D:\data\dayk1.db' )
cur = conn.cursor()
cur.execute( 'create table if not exists dayK(market, code, date, p, o, h, l, c, amt, vol, divi)')
cur.execute( 'create table if not exists dayK1(market, code, date, p, o, h, l, c, amt, vol, divi)')
conn.commit()

#insert into dayk1 select market, code,date,o/divi,h/divi,l/divi,c/divi,amt,vol,divi from dayk

k1=dayK_TDX()
rec = {}

#f.readinto(k1)
#k1.date, k1.amnt, k1.vol, k1.o, k1.h, k1.l, k1.c, k1.pre_c
#cur.execute( 'insert into dayK values ("%s", %s, %s, %s, %s, %s, %s, %s)' % ( 'sz000001', k1.date, float(k1.o)/100, float(k1.h)/100, float(k1.l)/100, float(k1.c)/100, float(k1.amnt)/10000, k1.vol/10000) )
#conn.commit()


#replace into
#prepared statment

'''
import os
tdxGlbMarkets = {12:'EM', 27:'HKI', 47:'ZJQ'}   # expensive metal, 
for f in fLst:
  fp = open(os.path.join( f[1], f[0] ), "rb")
  pid = f[0].split('.')[0]
  code = pid[2:]
  market = pid[:2]
  if f[1].split('\\')[-2]=='ds':
      code=pid[3:]
      market=tdxGlbMarkets[ pid[:2] ]
      pass
  recLst = []
  while fp.readinto(k1):
    #cur.execute( 'insert into dayK1 values ("%s", "%s", %s, %s, %s, %s, %s, %s, %s, %s, %s)' % ( market, code, k1.date, k1.pre_c, float(k1.o)/100, float(k1.h)/100, float(k1.l)/100, float(k1.c)/100, float(k1.amnt)/10000, k1.vol/10000, 0) )
    recLst.append( [market, code, k1.date, k1.pre_c, float(k1.o)/100, float(k1.h)/100, float(k1.l)/100, float(k1.c)/100, float(k1.amnt)/10000, k1.vol/10000, 0] )
  cur.executemany('insert into dayK1 (market, code, date, p, o, h, l, c, amt, vol, divi) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', recLst)
  conn.commit()
  fp.close()
'''

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
f.close()
'''

import talib
import pandas as pd
from datetime import datetime


url = 'https://raw.github.com/pydata/pandas/master/pandas/tests/data/tips.csv'
tips1 = pd.read_csv(url)
tips = pd.read_csv(r'C:\Anaconda3\Lib\site-packages\pandas\tests\data\tips.csv')
x=tips.head()

outputs = talib.SMA(tips1.tip.values, timeperiod=5)

dayk000001 = pd.read_sql_query('select * from dayK1 where market="600109"', conn)
sma5 = talib.SMA( dayk000001.c.values, timeperiod=5)
sma10 = talib.SMA( dayk000001.c.values, timeperiod=10)
sma20 = talib.SMA( dayk000001.c.values, timeperiod=20)
sma60 = talib.SMA( dayk000001.c.values, timeperiod=60)

minv = talib.MIN(dayk000001.l.values)
maxv = talib.MAX(dayk000001.h.values)
floorv = talib.FLOOR(dayk000001.h.values)
ceilv = talib.CEIL(dayk000001.l.values)

cci14 = talib.CCI( dayk000001.h.values, dayk000001.l.values, dayk000001.c.values)
bol20 = talib.BBANDS(dayk000001.c.values, timeperiod=20)
rsi = talib.RSI(dayk000001.c.values)
macd = talib.MACD(dayk000001.c.values, )

        


connHis = db.connect( r'E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3' )
def addPreClose(conn):
    df_cns = pd.read_sql_query('select * from myapp_kDaily_cns', conn)
    df_hks = pd.read_sql_query('select * from myapp_kDaily_hks', conn)
    df_cni = pd.read_sql_query('select * from myapp_kDaily_cni', conn)
    df_hki = pd.read_sql_query('select * from myapp_kDaily_hki', conn)
    dfl = [df_cns, df_cni, df_hks, df_hki]
    df = pd.concat(dfl, ignore_index=True)

    cur = conn.cursor()
    for key in prodDict8Submarket:
        tblName = MapSubmarket2Table( key ).lower()
        if tblName <> 'cns' and tblName <> 'hks' and tblName <> 'cni' and tblName <> 'hki':
            continue 
        for prod in prodDict8Submarket[key]:
            if prod.dateHistEnd == None:
                continue
            elif prod.ratioFrwdBegin == None:
                sys.stdout.write(  'dateHistEnd is not Null but ratioFrwdBegin isnull:' + prod.code+'.'+prod.submarket + '\r\n' )
                continue

            try:
                cur.execute( "update myapp_kdaily_%s set ratioBack=%s/ratioFrwd where product_id = %s" % (tblName, prod.ratioFrwdBegin, prod.id) )
            except db.Error,e:
                sys.stdout.write(  'except while execute update:' + prod.code+'.'+prod.submarket + ' Error: ' + str(e) + '\r\n' )
    conn.commit()

def moreK(conn, fld):
    dfD = pd.read_sql_query('select * from myapp_kDaily', conn)
    grouped = dfD.groupby([dfD['product_id'], dfD['year'], dfD[fld]])
    h=grouped['h'].max()
    l=grouped['l'].min()
    o=grouped['o'].first()
    c=grouped['c'].last()

def groupK(conn, fld):
    t = time.clock()
    #dfD = pd.read_sql_query('select * from myapp_kDaily where product_id = 8838 ', conn)
    dfD = pd.read_sql_query('select * from myapp_kDaily', conn)
    print('read_sql_query time: %.03f' % (time.clock()-t) )
    
    t = time.clock()
    grouped = dfD.groupby([dfD['product_id'], dfD['year'], dfD[fld]])
    h=grouped['h'].max()
    l=grouped['l'].min()
    o=grouped['o'].first()
    c=grouped['c'].last()
    startD=grouped['date'].min()
    ih=grouped['h'].idxmax()
    hD=dfD.iloc[ih]['date']
    hD.name='hDate'
    hD.index=o.index
    il=grouped['l'].idxmin()
    lD=dfD.iloc[il]['date']
    lD.name='lDate'
    lD.index=o.index
    #dfM = pd.merge( pd.DataFrame(startD), pd.DataFrame(o), on=['product_id', 'year', fld] )
    rsltDf = pd.DataFrame(startD).join( [pd.DataFrame(o), pd.DataFrame(h), pd.DataFrame(l), pd.DataFrame(c), pd.DataFrame(hD), pd.DataFrame(lD) ] )
    print('group month time: %.03f' % (time.clock()-t) )
    return rsltDf

for p in pL['product_id']:

dfW = groupK(connHis, 'week')
t = time.clock()
dfW.to_sql('myapp_kWeek', connHis, if_exists='append')
print('to_sql time: %.03f' % (time.clock()-t) )

dfM = groupK(connHis, 'month')
t = time.clock()
dfM.to_sql('myapp_kMonth', connHis, if_exists='append')
print('to_sql time: %.03f' % (time.clock()-t) )

#def getTrend(dfM):
trendDict = {}
for prod in dfM['product_id']:
    pK=dfM[prod][0]
    trRec = initTrend( dfM[prod].k0 ) 
    trendDict[prod] = trRec
    sureTr = trRec[0]  # latest sure trend
    newTr = trRec[0]  # newTr is latest trend, newTr may be not sure, i.e., it is may dead and become a period of sureTr. 
    # newTr == sureTr means max distance is continue increasing and no withdraw until latest day.   i.e., l or h of today is new max distance
    for k in dfM[prod][1:]:
        if newTr.sure == False:
            if newTr.up ==  False: # fall recent
                if k.h > sureTr.h:  # newTr dead, previous trend (sureTr) continue to grow
                    sureTr.h = k.h
                    newTr = sureTr
                    trRec.delete(-1)
                    continue
                elif k.l < newTr.l:
                    newTr.l = k.l
                    newTr.endDate = k.date
            else:                # up trend
                if k.l < sureTr.l:  # newTr dead, previous trend (sureTr) continue to grow
                    sureTr.l = k.l
                    newTr = sureTr
                    trRec.delete(-1)
                    continue
                elif k.h > newTr.h:
                    newTr.h = k.h
                    newTr.endDate = k.date
            if ( (newTr.h-newTr.l) / newTr.l > 1.5 ) or ( newTr.endDate - newTr.date > 3mon and (newTr.h-newTr.l) / newTr.l > 1.25):  # newTr become sure after enough space and space/time:
                sureTr.close=True
                sureTr.endDate = k.date
                newTr.status = 'sure'
                sureTr = newTr
        else:  
            if newTr.up ==  False: # fall recent
                if k.l < newTr.l:
                    newTr.l = k.l
                    newTr.endDate = k.date
                if k.c > k.p:
                    newTr = newTrend(newTr, k0) # newTr is the same with sureTr before call return
                    trRec.append( newTr )
            else:                # up trend
                if k.h > newTr.h:
                    newTr.h = k.h
                    newTr.endDate = k.date
                if k.c < k.p:
                    newTr = newTrend(newTr, k0) # newTr is the same with sureTr before call return
                    trRec.append( newTr )

def newTrend(curTrend, K):
    newTr={}
    newTr.sure = False
    newTr.date = curTrend.endDate ## ?? k.date
    newTr.up = not curTrend.up
    if curTrend.up == False:
        if K.l < curTrend.l :
            pass

def initTrend(k0):
    #1st trend ::              trendDict[prod].append( {Up:'', startD:'', startV:'', endV:'', status:'close'} )  # pTrend    curTrend   IPO Price
    trRec = []
    firstTr={'up':'', 'h':k0.h, 'l':k0.l, 'date':k0.date, 'c':k0.c, 'status':'sure'}
    # def first trend Up according to o/c price of first K 
    if IsNull( k0.p ):   # have IPO price
      if k0.c>k0.o:     # no change means Up         Up=True
          pass
      else:
          Up=False
    else:
      if k0.c>k0.p:     # no change means fall  
          Up=True
      else:
          Up=False
    firstTr['up'] = Up
    return trRec.append( firstTr )

create view tmp as select product_id, count(*) num from myapp_kdaily_cns group by product_id
delete from myapp_kdaily_cns where product_id in (select product_id from tmp where num<5)
create view tmp as select product_id, count(*) num from myapp_kdaily_cns group by product_id
delete from myapp_kdaily_cns1 where product_id in (select product_id from tmp1 where num<5)

select count(*) from myapp_kdaily_cns1 where c isnull or c=0
# error data: adjC=0?  # some adjC isnull lead to fail of update
update myapp_kdaily_cns1 set adjC=c where adjC isnull;  # some adjC isnull lead to fail of update
delete from myapp_kdaily_cns where year isnull
# Select distinct(date) From MAIN.[myapp_kdaily_cns1] where year isnull

insert into myapp_kweek(product_id,date,period, h,l,amt,vol) select product_id, min(date), 'week', max(h), min(l), sum(amt), sum(vol) from myapp_kdaily group by product_id, year, week;
insert into myapp_kmonth(product_id,date,period, h,l,amt,vol) select product_id, min(date), 'month', max(h), min(l), sum(amt), sum(vol) from myapp_kdaily group by product_id, year, month;
#ALTER TABLE myapp_kdaily ADD COLUMN ratioFrwdBegin decimal
ALTER TABLE myapp_product ADD COLUMN  "dateHistBegin" date

ALTER TABLE myapp_kdaily ADD COLUMN pDate date
insert into myapp_kdate(product_id,date) select product_id, date from myapp_kdaily order by product_id, date
CREATE INDEX "myapp_kdate_idx" ON "myapp_kdate" ("product_id", "date");
CREATE INDEX "myapp_kdate_idx1" ON "myapp_kdate" ("product_id", "id");
update myapp_seqdate a set a.pdate=b.date from myapp_seqdate a, myapp_seqdate b where a.product_id=b.product_id and a.id=b.id+1
insert into myapp_seqdate(product_id, date, pdate) select a.product_id, a.date, b.date from myapp_kdate a, myapp_kdate b where a.product_id=b.product_id and a.id=b.id+1
create view kdaily as select * from myapp_kdaily_cns union select * from myapp_kdaily_hks  
EXPLAIN QUERY PLAN SELECT * FROM myapp_kdaily_cns WHERE year>2010



def intdate(int):
    return datetime.strptime(str(int), '%Y%m%d')


dayk1 = pd.read_sql_query('select * from dayK1 where market="600109"', conn)
dates=map(strdate, dayk1.date.values)
ts = pd.Series(dayk1.h.values, index=dates)
ts1 = ts.resample('W', how='max')



#kdj = talib.kdj

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
conn = db.connect( r'D:\dayk1.db' )

import os
for f in fLst:
  tips2 = pd.read_csv(os.path.join( f[1], f[0] ), skiprows=1, names=['pid','date','o','h','l','c','amt','vol', 'divi'])
  tips2.to_sql('dayk', conn, if_exists='append')

cur.execute( 'create table if not exists dayK1(pid, date, o, h, l, c, amt, vol, divi)')





x = ['ACOS',
 'AD',
 'ADD',
 'ADOSC',
 'ADX',
 'ADXR',
 'APO',
 'AROON',
 'AROONOSC',
 'ASIN',
 'ATAN',
 'ATR',
 'AVGPRICE',
 'BBANDS',
 'BETA',
 'BOP',
 'CCI',
 'CDL2CROWS',
 'CDL3BLACKCROWS',
 'CDL3INSIDE',
 'CDL3LINESTRIKE',
 'CDL3OUTSIDE',
 'CDL3STARSINSOUTH',
 'CDL3WHITESOLDIERS',
 'CDLABANDONEDBABY',
 'CDLADVANCEBLOCK',
 'CDLBELTHOLD',
 'CDLBREAKAWAY',
 'CDLCLOSINGMARUBOZU',
 'CDLCONCEALBABYSWALL',
 'CDLCOUNTERATTACK',
 'CDLDARKCLOUDCOVER',
 'CDLDOJI',
 'CDLDOJISTAR',
 'CDLDRAGONFLYDOJI',
 'CDLENGULFING',
 'CDLEVENINGDOJISTAR',
 'CDLEVENINGSTAR',
 'CDLGAPSIDESIDEWHITE',
 'CDLGRAVESTONEDOJI',
 'CDLHAMMER',
 'CDLHANGINGMAN',
 'CDLHARAMI',
 'CDLHARAMICROSS',
 'CDLHIGHWAVE',
 'CDLHIKKAKE',
 'CDLHIKKAKEMOD',
 'CDLHOMINGPIGEON',
 'CDLIDENTICAL3CROWS',
 'CDLINNECK',
 'CDLINVERTEDHAMMER',
 'CDLKICKING',
 'CDLKICKINGBYLENGTH',
 'CDLLADDERBOTTOM',
 'CDLLONGLEGGEDDOJI',
 'CDLLONGLINE',
 'CDLMARUBOZU',
 'CDLMATCHINGLOW',
 'CDLMATHOLD',
 'CDLMORNINGDOJISTAR',
 'CDLMORNINGSTAR',
 'CDLONNECK',
 'CDLPIERCING',
 'CDLRICKSHAWMAN',
 'CDLRISEFALL3METHODS',
 'CDLSEPARATINGLINES',
 'CDLSHOOTINGSTAR',
 'CDLSHORTLINE',
 'CDLSPINNINGTOP',
 'CDLSTALLEDPATTERN',
 'CDLSTICKSANDWICH',
 'CDLTAKURI',
 'CDLTASUKIGAP',
 'CDLTHRUSTING',
 'CDLTRISTAR',
 'CDLUNIQUE3RIVER',
 'CDLUPSIDEGAP2CROWS',
 'CDLXSIDEGAP3METHODS',
 'CEIL',
 'CMO',
 'CORREL',
 'COS',
 'COSH',
 'DEMA',
 'DIV',
 'DX',
 'EMA',
 'EXP',
 'FLOOR',
 'HT_DCPERIOD',
 'HT_DCPHASE',
 'HT_PHASOR',
 'HT_SINE',
 'HT_TRENDLINE',
 'HT_TRENDMODE',
 'KAMA',
 'LINEARREG',
 'LINEARREG_ANGLE',
 'LINEARREG_INTERCEPT',
 'LINEARREG_SLOPE',
 'LN',
 'LOG10',
 'MA',
 'MACD',
 'MACDEXT',
 'MACDFIX',
 'MAMA',
 'MAVP',
 'MAX',
 'MAXINDEX',
 'MA_Type',
 'MEDPRICE',
 'MFI',
 'MIDPOINT',
 'MIDPRICE',
 'MIN',
 'MININDEX',
 'MINMAX',
 'MINMAXINDEX',
 'MINUS_DI',
 'MINUS_DM',
 'MOM',
 'MULT',
 'NATR',
 'OBV',
 'PLUS_DI',
 'PLUS_DM',
 'PPO',
 'ROC',
 'ROCP',
 'ROCR',
 'ROCR100',
 'RSI',
 'SAR',
 'SAREXT',
 'SIN',
 'SINH',
 'SMA',
 'SQRT',
 'STDDEV',
 'STOCH',
 'STOCHF',
 'STOCHRSI',
 'SUB',
 'SUM',
 'T3',
 'TAN',
 'TANH',
 'TEMA',
 'TRANGE',
 'TRIMA',
 'TRIX',
 'TSF',
 'TYPPRICE',
 'ULTOSC',
 'VAR',
 'WCLPRICE',
 'WILLR',
 'WMA',
 '__all__',
 '__builtins__',
 '__doc__',
 '__file__',
 '__function_groups__',
 '__name__',
 '__package__',
 '__path__',
 '__ta_version__',
 '__version__',
 'abstract',
 'atexit',
 'common',
 'func',
 'get_function_groups',
 'get_functions']
