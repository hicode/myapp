# coding=utf-8
#-*- coding utf8 -*-
#889531705
#dpb3rvn
#if8gaim
from dm.basic import *

class DataCollection(object):
    pass

class SoftData( DataCollection ):
    appPath = ''
    def launch( self ):
        pass
    def check( self ):
        pass

class WebData( DataCollection ):
    pass

class HyMT4Data( SoftData ):
    appPath = r"C:\Program Files\licai18\BootLoad.exe"
    def getData( self ):
        pass

class StructTxt( object ):
    struc = None
    title = []
    dataGot = {}
    def read( self, fn ):
        fp = open( fn )
        data = fp.read()
        fp.close()

class CsvTxt( StructTxt ): # use csv module instead
    # ??? this class could use csv module instead

    # !!!!!!!!!!!!!!!!!!!! dt format check and convert!!!!!!!!!!!!!!
    fType = 1  # 1: SPT_GLD-MIN1K.CSV    2: EU.TXT  (1st line is the title line, contains product name)
    def transData2Db( self, fn ):  # titleLn whether exist the title line in 1st line
        # !!! auto check and identify the format\product\span of data file
        import csv
        import os.path
        reader = csv.reader( open( fn ) )
        if self.fType==1:
            fnl = os.path.split( fn )[1].split( '-' )
            for rowid, row in enumerate( reader ):
                rec = {}
                rec['product'] = fnl[0]
                #rec['date'] = row[0].replace('.','-')  # '%s-%s-%s' % (row[0][:4], row[0][4:6], row[0][6:])
                #rec['time'] = '%s:00' % row[1] # '%s:%s:%s' % (row[1][:2], row[1][2:4], row[1][4:])
                rec['dt'] = '%s %s:00'%(row[0].replace('.','-'), row[1])
                rec['o'] = row[2]
                rec['h'] = row[3]
                rec['l'] = row[4]
                rec['c'] = row[5]
                rec['amount'] = row[6]
                self.db.newRec( fnl[1], rec )
        elif self.fType==2:
            for rowid, row in enumerate( reader ):
                if rowid==0:
                    continue
                rec = {}
                rec['product'] = row[0]
                #rec['date'] = '%s-%s-%s' % (row[1][:4], row[1][4:6], row[1][6:])
                #rec['time'] = '%s:%s:%s' % (row[2][:2], row[2][2:4], row[2][4:])
                rec['dt'] = '%s-%s-%s %s:%s:%s'%(row[1][:4], row[1][4:6], row[1][6:], row[2][:2], row[2][2:4], row[2][4:])
                rec['o'] = row[3]
                rec['h'] = row[4]
                rec['l'] = row[5]
                rec['c'] = row[6]
                rec['amount'] = row[7]
                self.db.newRec( 'min1k', rec )
        else:
            print('error csv file type: %i' % self.fType)
        self.db.conn.commit()

class Mt4BakCsv( CsvTxt, Mt4ErMap ):
    dbName='tradeData.db'
    def __init__( self, fn, dbn = '', fType = 1 ):
        self.fType = fType
        if dbn:
            self.dbName=dbn  # 'mt4csv.db'
        Mt4ErMap.__init__( self, self.dbName )
        if fn:
            self.cascade2Db()
            self.transData2Db( fn )

class dataUnit( object ):
    def __init__( self, dict ):
        self.dt = dict['dt']
        self.h = dict['h']
        self.o = dict['o']
        self.l = dict['l']
        self.c = dict['c']
        self.amount = dict['amount']

class Idx():
    kData = None
    idxVal = []
    ma_par=(5,10,30,160)
    ma_par=(5,14,20)
    cci_par=(14)
    rsi_par=(14)
    psy_par=(14)
    boll_par=(14,20)
    def __init__( self, set, db=None ):
        import sqlite3
        if db:
            conn=sqlite3.connect(db)
            cur=con.getcursor()
            cur.exectue()
            for rec in cur.fetchall():
                set=None
        self.kData = set
        for idx, unit in enumerate( set ):
            self.idxVal.append( {} )
            self.idxVal[-1]['date'] = unit['date']
            #self.ma( idx, 5 )
            self.ma( idx, 14 )
            self.ma( idx, 20 )
            self.rsi( idx, 14 )#14 )
            self.cci( idx, 14 )#14 )
            self.cci1( idx, 14 )#14 )
            self.boll( idx, 20 )#20 )

    def cci( self, idx, n ):
        self.idxVal[idx]['_tp'] = ( float( self.kData[idx]['h'] ) + float( self.kData[idx]['l'] ) + float( self.kData[idx]['c'] ) ) / 3.0
        if idx >= n - 1:
            self.idxVal[idx]['_ma_tp'] = sum( [float( self.idxVal[idx - i]['_tp'] ) for i in range( n )] ) / ( n * 1.0 )
        if idx >= 2 * n - 2:
            md = sum( [ abs( self.idxVal[idx - i]['_tp'] - float( self.idxVal[idx - i]['_ma_tp'] ) ) for i in range( n ) ] )
            md = md / ( n * 1.0 )
            self.idxVal[idx]['cci'] = ( self.idxVal[idx]['_tp'] - self.idxVal[idx]['_ma_tp'] ) / md / 0.015

    def cci1( self, idx, n ):
        if idx >= 2 * n - 2:
            tp = ( float( self.kData[idx]['h'] ) + float( self.kData[idx]['l'] ) + float( self.kData[idx]['c'] ) ) / 3.0
            maN = 'ma%s' % n
            md = sum( [ abs( self.idxVal[idx - i][maN] - float( self.kData[idx - i]['c'] ) ) for i in range( n ) ] ) / ( n * 1.0 )
            self.idxVal[idx]['cci0'] = ( tp - self.idxVal[idx][maN] ) / md / 0.015

    #'''
    def ma( self, idx, n ):
        if idx < n - 1:
            return
        self.idxVal[idx]['ma%s' % n] = sum( [float( self.kData[idx - i]['c'] ) for i in range( n )] ) / ( n * 1.0 )
    '''
    def ma( self, idx, n, m = 1 ):
        maN = 'ma%s' % n
        if idx == 0:
            self.idxVal[idx][maN] = float( self.kData[idx]['c'] )
        else:
            self.idxVal[idx][maN] = ( float( self.kData[idx]['c'] ) * m + self.idxVal[idx - 1][maN] * ( n - m ) ) / n
    '''
    def rsi( self, idx, n ):
        if idx < n:
            return
        upSum = 0
        dnSum = 0
        for var in [ float( self.kData[idx - i]['c'] ) - float( self.kData[idx - i - 1]['c'] ) for i in range( n ) ]:
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
        md = sum( [( float( self.kData[idx - i]['c'] ) - self.idxVal[idx - i][maN] ) * ( float( self.kData[idx - i]['c'] ) - self.idxVal[idx - i][maN] ) for i in range( n )] )
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
    mt4 = Mt4BakCsv(r'D:\TDDOWNLOAD\auto\EU\eu.txt', fType=2 )
    #mt4 = Mt4BakCsv( r'.\data\SPT_GLD-min1K-.csv') #CLG0-dayK-20100109.csv' )
    db = Db( 'mt4csv.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()
    db.cur.execute( 'select * from min15K where product="SPT_GLD" order by dt' )
    r = db.cur.fetchall()
    x = Idx( r )
    #平滑系数???
    db = Db( 'mt4.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()
    db.cur.execute( 'select * from MIN15K where product="SPT_GLD" AND DATE="2010-08-11" order by dt' )
    r = db.cur.fetchall()
    cci = x.cci( r, 14 )
    cci = x.boll( r, 20 )

# 可以把你要装的package及所有的依赖项放到本地一个目录下，调用easy_install时指定命令行参数 -f <目录名>，它就会在这个目录下找安装文件。 
# 如果想删除通过easy_install安装的软件包，比如说：MySQL-python，可以执行命令： 
# easy_install -m MySQL-python 
# 此操作会从easy-install.pth文件里把MySQL-python的相关信息抹去，剩下的egg文件，你可以手动删除。 
