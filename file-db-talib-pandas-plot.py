# coding=utf-8

from common import *

#import sys
#import time
#from codetools.util.cbook import unique
#from pandas.core.common import notnull
#from django.db.models.lookups import IsNull
#sys.path.append(r"D:\ssd-e-bak\new\ali\dor\bak sure\s\good\MBSC-Upgrade")

#from autoTest import VosTool
#fLst = VosTool.getFileLst(        r'C:\new_tdx\vipdoc\sh\lday', '', False )
#fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\sz\lday', '', False )
##fLst += VosTool.getFileLst( r'C:\new_tdx\vipdoc\ds\lday', '', False )

from ctypes import *
class dayK_TDX(Structure):  # ?? c_int
     _fields_ = [ ('date',c_uint32), ('o',c_uint32), ('h',c_uint32), ('l',c_uint32), ('c',c_uint32), ('amnt',c_float), ('vol',c_uint32), ('pre_c',c_uint32) ]




#'''
class tick_Dzh_(Structure):
    _pack_ = 1
    _fields_ = [ ('t',c_int32), ('c',c_float), ('vol',c_float), ('amt',c_float), ('dealnum',c_uint16), ('x',c_uint16), ('overflowMark',c_byte), ('sbType',c_byte), 
                ('volB1',c_uint16), ('volB2',c_uint16), ('volB3',c_uint16), ('volB4',c_uint16), ('volB5',c_uint16), 
                ('volS1',c_uint16), ('volS2',c_uint16), ('volS3',c_uint16), ('volS4',c_uint16), ('volS5',c_uint16), 
                ('pB1',c_byte), ('pB2',c_byte), ('pB3',c_byte), ('pB4',c_byte), ('pB5',c_byte), 
                ('pS1',c_byte), ('pS2',c_byte), ('pS3',c_byte), ('pS4',c_byte), ('pS5',c_byte) ]
    # sbType : C0|A0-sell    80|E0-buy

class tick_Dzh(Structure):
    _pack_ = 1
    _fields_ = [ ('volB1',c_uint32), ('volB2',c_uint32), ('volB3',c_uint32), ('volB4',c_uint32), ('volB5',c_uint32) ]
    # sbType : C0|A0-sell    80|E0-buy

def getPrp_Dzh(fn, pid):
    pass

def getTick_Dzh(fn, pid):
    try:
        recLst = []
        with open( fn, 'rb' ) as fp:  # HTTP Error 404: Not Found
            rec = tick_Dzh()
            fp.read(0x2a0)
            while 0 <> fp.readinto( rec ):   # sizeof(head) is 20 ??set pack=1  # x = fp.read(16)
                recLst.append( rec ) #[pid, '%04d-%02d-%02d' % (year, mon, day), rec.seq, type, rec.p/1000.0, rec.buy/1000.0, rec.sell/1000.0, rec.vol, rec.dealnum ] )
                rec = tick_Dzh()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return recLst

def getDzhTickData(conn):
    #cur = conn.cursor()
    import scandir

    dirLst = [('sz', 'sz'), ('sh', 'sh')]
    fileDict = {}
    for d in dirLst:
        dir = 'C:\\dzh365\\data\\%s\\TEMP\\'  % d[0]
        market = d[1].upper()
        if market<>'SZ':
            continue
        tblName = 'myapp_productweight'
        recLst = []
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                if code<>'000002':
                    continue
                #if market=='HK':
                #    code = '0' + code
                prodId=code + '.' + market
                #if prodId not in prodMapId.keys():
                #    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                #    continue
                recLst += getTick_Dzh(dir + fn, 1) #prodMapId[prodId].id)
                #submarket = Submarket(market, code)
        #cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", recLst )
        if recLst<>[]:
            cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (?,?,?,?,?,?,?,?,?)", recLst )
            conn.commit()

#getDzhTickData(1)
#'''


def l2txt(fn, lst):
    with open(fn, 'w') as fp:
        for r in lst:
            fp.write(str(r)+'\r\n')

class tick_QL(Structure):
    _pack_ = 1
    _fields_ = [ ('seq',c_uint32), ('date',c_uint32), ('p',c_uint32), ('x',c_uint32), ('vol',c_uint32), ('buy',c_uint32), ('sell',c_uint32), ('dealnum',c_uint32), ('x1',c_uint32), ('x2',c_uint32), ('x3',c_uint32), ('x4',c_uint32), ('x5',c_uint32) ]

def getTick_QL(fn, pid):  # 成交量待正解 dealnum待正解
    try:
        recLst = []
        with open( fn, 'rb' ) as fp:  # HTTP Error 404: Not Found
            rec = tick_QL()
            fp.read(8)
            while 0 <> fp.readinto( rec ):   # sizeof(head) is 20 ??set pack=1  # x = fp.read(16)
                type = rec.date >> 24
                date = rec.date % 0x1000000
                t = date%0x8000
                m = (t+8)/60 + 6 
                h = 9 + m/60
                m = m % 60
                byte1 = rec.vol % 0x100
                hbit11 = rec.vol/0x200000
                num = (rec.vol>>8)%0x2000  #13bit
                recLst.append( [pid, '%02d:%02d'%(h,m), date>>13, rec.seq, type, rec.p/1000.0, rec.buy/1000.0, rec.sell/1000.0, rec.vol, byte1, hbit11, num, rec.dealnum ] )
                rec = tick_QL()
                l2txt(r'd:\\tick.csv', recLst)

    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return recLst

def getQlTickData(conn):
    #cur = conn.cursor()
    import scandir

    dirLst = [('sznse', 'sz'), ('shase', 'sh'), ('hkse','hk')]
    fileDict = {}
    for d in dirLst:
        dir = 'D:\\qianlong1\\qijian\\QLDATA\\realtime\\%s\\detail\\' % d[0]
        market = d[1].upper()
        if market<>'HK':
            continue
        tblName = 'myapp_productweight'
        recLst = []
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                if market=='HK':
                    code = '0' + code
                prodId=code + '.' + market
                #if prodId not in prodMapId.keys():
                #    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                #    continue
                recLst += getTick_QL(dir + fn, 1) #prodMapId[prodId].id)
                #submarket = Submarket(market, code)
        #cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", recLst )
        if recLst<>[]:
            cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (?,?,?,?,?,?,?,?,?)", recLst )
            conn.commit()

#getQlTickData(1)




class compIdx_THS(Structure):
    _pack_ = 1
    _fields_ = [ ('len',c_uint16), ('idxNum',c_uint16) ]

class compIdx_THS_rec(Structure):
    _pack_ = 1
    _fields_ = [ ('type',c_byte), ('code',c_byte*9), ('freeRecNum', c_uint16), ('addr', c_uint32), ('recNum', c_uint16) ]

class dividend_THS_rec(Structure):
    _pack_ = 1
    _fields_ = [ ('date',c_uint32), ('w1',c_int32), ('exdividendDate',c_int32), ('cash',c_uint32), ('split',c_uint32), 
                ('bonus',c_uint32), ('dispatch',c_uint32), ('price',c_uint32), ('regDate',c_uint32), ('listingDate',c_uint32), ('desc',c_uint32) ]

class dayK_THS(Structure):
    header = tHS_FHeader()
    # fldList

def diviFromThs(fn, pid):
    idxDivi = compIdx_THS_rec()
    recDivi = dividend_THS_rec()
    try:
        recDiviLst = []
        with open( fn, 'rb' ) as fp:  # HTTP Error 404: Not Found
            head = tHS_FHeader()
            fp.readinto( head )   # sizeof(head) is 20 ??set pack=1  # x = fp.read(16)
            head.recCount = head.recCount & 0xffffff

            #idxBlockAddr = sizeof(head) + head.fldCount * 4 + head.fldCount * 2
            #fp.read( idxBlockAddr-sizeof(head) ) # read columnList
            fp.read( head.fldCount * 4 + head.fldCount * 2 )
            headIdxBlock = compIdx_THS()
            fp.readinto( headIdxBlock )
            idxDiviLst = []
            for i in range(headIdxBlock.idxNum):  #while fp.readinto(k1):
                fp.readinto( idxDivi )
                idxDiviLst.append( idxDivi )
                idxDivi = compIdx_THS_rec()

            for idx in idxDiviLst:  #while fp.readinto(k1):
                validRecNum = idx.recNum-idx.freeRecNum-1
                for i in idx.recNum:
                    if i > validRecNum:
                        break  #continue
                    fp.seek(idx.addr)
                    fp.readinto( recDivi )
                    recDiviLst.append( recDivi ) #recDiviLst.append( [pid, k1.date, getValTHS(k1.o), getValTHS(k1.h), getValTHS(k1.l), getValTHS(k1.c), getValTHS(k1.amnt), getValTHS(k1.vol), 0] )
                    recDivi = dividend_THS_rec()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return recDiviLst

#diviFromThs(u'D:\\data\\hqzqzyb2\\finance\\权息资料.财经', 1)


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

'''
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
'''
        




# os.xx ( command =" mysqldump myapp_product ") 
#cur.execute(statement)

#from sqlalchemy import create_engine
#connHis = create_engine('mysql+mysqldb://root:@localhost/myapp')


#import mysql as db  #connector.paramstyle　
#connHis = db.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
import MySQLdb as db
connHis = db.connect( host='localhost', user='root', passwd='', db='myapp', charset='utf8' )
cur = connHis.cursor()
#statement =" select * from myapp_product into outfile 'test.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n';
statement =" load data infile 'myapp_cns_kmonth.csv' into table myapp_kmonth fields terminated by ',' (product_id, @year, @month, @date,p,o,h,l,c,@hdate,@ldate,vol) set date=STR_TO_DATE(@date,'%Y%m%d'), hdate=STR_TO_DATE(@hdate,'%Y%m%d'), ldate=STR_TO_DATE(@ldate,'%Y%m%d') "
cur.execute( statement )
statement =" load data infile 'myapp_cns_kweek.csv' into table myapp_kweek fields terminated by ',' (product_id, @year, @week, @date,p,o,h,l,c,@hdate,@ldate,vol) set date=STR_TO_DATE(@date,'%Y%m%d'), hdate=STR_TO_DATE(@hdate,'%Y%m%d'), ldate=STR_TO_DATE(@ldate,'%Y%m%d') " #fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n';
cur.execute( statement )
connHis.commit()

import mysql.connector
cnx = mysql.connector.connect(user='root', database='myapp')
curA = cnx.cursor(buffered=True)
cnx1 = mysql.connector.connection.MySQLConnection(user='root', database='myapp')


statement =" select * from myapp_product into outfile 'test.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
cnx1.cmd_query( statement )



state2 = "delete from myapp_productidx; delete from myapp_periodHL_;"
cnx1.cmd_query_iter( state2 )  #cur.execute(state2 , multi=True)


'''
select * from myapp_product into outfile 'd:\test.csv' fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
load data infile 'd:\test.csv' into table myapp_product fields terminated by ','  optionally enclosed by '"' escaped by '"' lines terminated by '\r\n';   
'''

# Query to get employees who joined in a period defined by two dates
query = (
  "SELECT s.emp_no, salary, from_date, to_date FROM employees AS e "
  "LEFT JOIN salaries AS s USING (emp_no) "
  "WHERE to_date = DATE('9999-01-01')"
  "AND e.hire_date BETWEEN DATE(%s) AND DATE(%s)")

# UPDATE and INSERT statements for the old and new salary
update_old_salary = (
  "UPDATE salaries SET to_date = %s "
  "WHERE emp_no = %s AND from_date = %s")
insert_new_salary = (
  "INSERT INTO salaries (emp_no, from_date, to_date, salary) "
  "VALUES (%s, %s, %s, %s)")

# Select the employees getting a raise
curA.execute(query, (date(2000, 1, 1), date(2000, 12, 31)))

# Iterate through the result of curA
for (emp_no, salary, from_date, to_date) in curA:

  # Update the old and insert the new salary
  new_salary = int(round(salary * Decimal('1.15')))
  curB.execute(update_old_salary, (tomorrow, emp_no, from_date))
  curB.execute(insert_new_salary,
               (emp_no, tomorrow, date(9999, 1, 1,), new_salary))

  # Commit the changes
  cnx.commit()

cnx.close()






def db_Csv():
    pass



'''
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
CREATE INDEX "myapp_kdaily_cns_tmp_idx111" ON "myapp_kdaily_cns_tmp" ("product_id", "id");
update myapp_seqdate a set a.pdate=b.date from myapp_seqdate a, myapp_seqdate b where a.product_id=b.product_id and a.id=b.id+1
insert into myapp_seqdate(product_id, date, pdate) select a.product_id, a.date, b.date from myapp_kdate a, myapp_kdate b where a.product_id=b.product_id and a.id=b.id+1
create view kdaily as select * from myapp_kdaily_cns union select * from myapp_kdaily_hks  
EXPLAIN QUERY PLAN SELECT * FROM myapp_kdaily_cns WHERE year>2010
'''




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


