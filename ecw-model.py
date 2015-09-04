# coding=utf-8
#-*- coding utf8 -*-
#889531705
#dpb3rvn
#if8gaim
from swampy.Lumpy import *
#lumpy = Lumpy()
#lumpy.make_reference()

from dm.basic import *

class DataCollection():
    pass

class SoftData( DataCollection ):
    appPath = ''
    def launch( self ):
        pass
    def check( self ):
        pass

class WebData( DataCollection ):
    def structLines(self, formatStr):
    pass

class HyMT4Data( SoftData ):
    appPath = r"C:\Program Files\licai18\BootLoad.exe"
    def getData( self ):
        pass

class StructTxt( object ):
    struc = None
    title = []
    dataGot = {}
    def read( fn ):
        fp = open( fn )
        data = fp.read()
        fp.close()

class CsvTxt( StructTxt ): # use csv module instead
    def transData2Db( self, fn ):
        import csv
        import os.path
        reader = csv.reader( open( fn ) )
        fnl = os.path.split( fn )[1].split( '-' )
        for rowid, row in enumerate( reader ):
            rec = {}
            rec['product'] = fnl[0]
            rec['date'] = row[0]
            rec['time'] = row[1]
            rec['open'] = row[2]
            rec['high'] = row[3]
            rec['low'] = row[4]
            rec['close'] = row[5]
            rec['amount'] = row[6]
            self.db.newRec( fnl[1], rec )
        self.db.conn.commit()

class Mt4BakCsv( CsvTxt, Mt4ErMap ):
    def __init__( self, dbf, csvf = '' ):
        Mt4ErMap.__init__( self, dbf )
        if fn:
            self.cascade2Db()
            self.transData2Db( csvf )

class dataUnit( object ):
    def __init__( self, dict ):
        self.date = dict['date']
        self.time = dict['time']
        self.high = dict['high']
        self.open = dict['open']
        self.low = dict['low']
        self.close = dict['close']
        self.amount = dict['amount']

# 初始化数据: K线数据-二维数组(开/收/高/低/量/时刻)
# 初始化后可得到每时刻各指标值
# K线数据每增加一个时刻数据,可补充相应时刻的各指标值
class Idx():
    kData = None
    idxVal = []
    def __init__( self, set ):
        self.kData = set
        self.maN=[5,14,20]
        self.rsiN=14
        self.cciN=14
        self.bollN=20
        for idx, unit in enumerate( set ):
            #self.calcIdx(idx, unit)
            self.idxVal.append( {} )
            self.idxVal[-1]['date'] = unit['date']
            #self.ma( idx, 5 )
            self.ma( idx, self.maN )
            self.ma( idx, self.maN )
            self.rsi( idx, self.bollN )
            self.cci( idx, self.cciN )
            self.boll( idx, self.bollN )

    def addK(self, K):
        self.kData.append(K)
        self.calcIdx(len(self.kData)-1, K)

    def calcIdx(self,idx,K):
        self.idxVal.append( {} )
        self.idxVal[-1]['date'] = K['date']
        #self.ma( idx, 5 )
        self.ma( idx, 14 )
        self.ma( idx, 20 )
        self.rsi( idx, 14 )#14 )
        self.cci( idx, 14 )#14 )
        self.cci1( idx, 14 )#14 )
        self.boll( idx, 20 )#20 )
    
    def cci( self, idx, n ):
        self.idxVal[idx]['_tp'] = ( float( self.kData[idx]['high'] ) + float( self.kData[idx]['low'] ) + float( self.kData[idx]['close'] ) ) / 3.0
        if idx >= n - 1:
            self.idxVal[idx]['_ma_tp'] = sum( [float( self.idxVal[idx - i]['_tp'] ) for i in range( n )] ) / ( n * 1.0 )
        if idx >= 2 * n - 2:
            md = sum( [ abs( self.idxVal[idx - i]['_tp'] - float( self.idxVal[idx - i]['_ma_tp'] ) ) for i in range( n ) ] )
            md = md / ( n * 1.0 )
            self.idxVal[idx]['cci'] = ( self.idxVal[idx]['_tp'] - self.idxVal[idx]['_ma_tp'] ) / md / 0.015

    def cci1( self, idx, n ):
        if idx >= 2 * n - 2:
            tp = ( float( self.kData[idx]['high'] ) + float( self.kData[idx]['low'] ) + float( self.kData[idx]['close'] ) ) / 3.0
            maN = 'ma%s' % n
            md = sum( [ abs( self.idxVal[idx - i][maN] - float( self.kData[idx - i]['close'] ) ) for i in range( n ) ] ) / ( n * 1.0 )
            self.idxVal[idx]['cci0'] = ( tp - self.idxVal[idx][maN] ) / md / 0.015

    #'''
    def ma( self, idx, n ):
        if idx < n - 1:
            return
        self.idxVal[idx]['ma%s' % n] = sum( [float( self.kData[idx - i]['close'] ) for i in range( n )] ) / ( n * 1.0 )
    '''
    def ma( self, idx, n, m = 1 ):
        maN = 'ma%s' % n
        if idx == 0:
            self.idxVal[idx][maN] = float( self.kData[idx]['close'] )
        else:
            self.idxVal[idx][maN] = ( float( self.kData[idx]['close'] ) * m + self.idxVal[idx - 1][maN] * ( n - m ) ) / n
    '''
    def rsi( self, idx, n ):
        if idx < n:
            return
        upSum = 0
        dnSum = 0
        for var in [ float( self.kData[idx - i]['close'] ) - float( self.kData[idx - i - 1]['close'] ) for i in range( n ) ]:
            if var > 0:
                upSum += var
            else:
                dnSum += -var
        self.idxVal[idx]['rsi'] = upSum / ( upSum + dnSum ) * 100
        # sum([max(var,0)])
        if idx == 47:
            x = 1

    def boll( self, idx, n ):
        if idx < 2 * n - 2:
            return
        import decimal
        maN = 'ma%s' % n
        md = sum( [( float( self.kData[idx - i]['close'] ) - self.idxVal[idx - i][maN] ) * ( float( self.kData[idx - i]['close'] ) - self.idxVal[idx - i][maN] ) for i in range( n )] )
        md = md / ( n * 1.0 )
        md1 = float( decimal.Decimal( str( md ) ).sqrt() )
        self.idxVal[idx]['bollMb'] = self.idxVal[idx][maN]  #?? self.idxVal[idx - 1][maN]
        self.idxVal[idx]['bollUp'] = self.idxVal[idx]['bollMb'] + 2 * md1
        self.idxVal[idx]['bollDn'] = self.idxVal[idx]['bollMb'] - 2 * md1

    def macd( self ):
        pass

    def psy( self ):
        pass
    #ma,rsi,track,density-distribution

if __name__ == '__main__':
    import sqlite3
    mt4 = Mt4BakCsv( r'.\dm\mt4csv.db', r'c:\CLH11440.csv') #r'.\data\SPT_GLD-min1K-.csv') #CLG0-dayK-20100109.csv' )
    db = Db( 'mt4csv.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()

    #lumpy.object_diagram()
    #lumpy.class_diagram()

    db.cur.execute( 'select * from dayK where product="CLH1" order by date,time' )
    r = db.cur.fetchall()
    x = Idx( r )
    #平滑系数???
    db = Db( 'mt4.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()
    db.cur.execute( 'select * from MIN15K where product="SPT_GLD" AND DATE="2010-08-11" order by date,time' )
    r = db.cur.fetchall()
    cci = x.cci( r, 14 )
    cci = x.boll( r, 20 )

# 可以把你要装的package及所有的依赖项放到本地一个目录下，调用easy_install时指定命令行参数 -f <目录名>，它就会在这个目录下找安装文件。 
# 如果想删除通过easy_install安装的软件包，比如说：MySQL-python，可以执行命令： 
# easy_install -m MySQL-python 
# 此操作会从easy-install.pth文件里把MySQL-python的相关信息抹去，剩下的egg文件，你可以手动删除。 
