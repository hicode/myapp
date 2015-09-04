#-*- coding utf8 -*-
#889531705
#dpb3rvn
#if8gaim
from basic import *

class DataCollection():
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
    def __init__( self, fn = '' ):
        Mt4ErMap.__init__( self, 'mt4csv.db' )
        if fn:
            self.cascade2Db()
            self.transData2Db( fn )

class dataUnit( object ):
    def __init__( self, dict ):
        self.date = dict['date']
        self.time = dict['time']
        self.high = dict['high']
        self.open = dict['open']
        self.low = dict['low']
        self.close = dict['close']
        self.amount = dict['amount']

class Idx():
    kData = {}
    idxVal = {}
    def __init( self, set ):
        self.kData = set
        for idx, unit in enumerate( set ):
            self.ma( idx, 5 )
            self.ma( idx, 14 )
            self.ma( idx, 20 )
            self.rsi( idx, 14 )
    @staticmethod
    def cci( set, n ):
        if len( set ) < n:
            return False
        rslt = []
        for idx, unit in enumerate( set ):
            unitIdx = {}
            rslt.append( unitIdx )
            unitIdx['date'] = unit['date']
            unitIdx['tp'] = ( float( unit['high'] ) + float( unit['low'] ) + float( unit['close'] ) ) / 3.0
            if idx >= n - 1:
                unitIdx['ma'] = sum( [float( set[idx - i]['close'] ) for i in range( n )] ) / ( n * 1.0 )
            if idx >= 2 * n - 2:
                unitIdx['md'] = sum( [ abs( rslt[idx - i]['ma'] - float( set[idx - i]['close'] ) ) for i in range( n ) ] ) / ( n * 1.0 )
                unitIdx['cci'] = ( unitIdx['tp'] - unitIdx['ma'] ) / unitIdx['md'] / 0.015
        return rslt
    @staticmethod
    def cci_1( set, n ):
        if len( set ) < n:
            return False
        rslt = []
        for idx, unit in enumerate( set ):
            unitIdx = {}
            rslt.append( unitIdx )
            unitIdx['date'] = unit['date']
            unitIdx['tp'] = ( float( unit['high'] ) + float( unit['low'] ) + float( unit['close'] ) ) / 3.0
            if idx >= n - 1:
                unitIdx['ma_tp'] = sum( [float( rslt[idx - i]['tp'] ) for i in range( n )] ) / ( n * 1.0 )
            if idx >= 2 * n - 2:
                unitIdx['md'] = sum( [ abs( rslt[idx - i]['tp'] - float( rslt[idx - i]['ma_tp'] ) ) for i in range( n ) ] ) / ( n * 1.0 )
                unitIdx['cci'] = ( unitIdx['tp'] - unitIdx['ma_tp'] ) / unitIdx['md'] / 0.015
        return rslt

    @staticmethod
    def ma( idx, n ):
        if idx >= n - 1:
            self.idxVal[idx]['ma%s' % n] = sum( [float( self.kData[idx - i]['close'] ) for i in range( n )] ) / ( n * 1.0 )
    @staticmethod
    def rsi( idx, n ):
        if idx >= n:
            upSum = 0
            dnSum = 0
            for var in [self.kData[idx - i]['close'] - self.kData[idx - i - 1]['close'] for i in range( n )]:
                if var > 0:
                    upSum += var
                else:
                    dnSum += -var
            self.idxVal[idx]['rsi'] = upSum / ( upSum + dnSum ) * 100
    @staticmethod
    def macd():
        pass
    @staticmethod
    def psy():
        pass
    @staticmethod
    def boll( set, n ):
        if len( set ) < n:
            return False
        import decimal
        rslt = []
        for idx, unit in enumerate( set ):
            unitIdx = {}
            rslt.append( unitIdx )
            unitIdx['date'] = unit['date']
            if idx >= n - 1:
                unitIdx['ma'] = sum( [float( set[idx - i]['close'] ) for i in range( n )] ) / ( n * 1.0 )
            if idx >= 2 * n - 2:
                _md = sum( [( float( set[idx - i]['close'] ) - rslt[idx - i]['ma'] ) * ( float( set[idx - i]['close'] ) - rslt[idx - i]['ma'] ) for i in range( n )] ) / ( n * 1.0 )
                unitIdx['md'] = float( decimal.Decimal( str( _md ) ).sqrt() )
                unitIdx['mb'] = unitIdx['ma']  #?? rslt[idx - 1]['ma']
                unitIdx['up'] = unitIdx['mb'] + 2 * unitIdx['md']
                unitIdx['dn'] = unitIdx['mb'] - 2 * unitIdx['md']
        return rslt
    #ma,rsi,track,density-distribution

if __name__ == '__main__':
    import sqlite3
    #mt4 = Mt4BakCsv( r'.\data\CLG0-dayK-20100109.csv' )
    db = Db( 'mt4csv.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()
    db.cur.execute( 'select * from dayK where product="CLG0" order by date,time' )
    r = db.cur.fetchall()
    cci = Idx.cci( r, 14 )
    cci = Idx.cci_1( r, 14 )
    cci = Idx.boll( r, 20 )

    db = Db( 'mt4.db' )
    db.conn.row_factory = sqlite3.Row
    db.cur = db.conn.cursor()
    db.cur.execute( 'select * from MIN15K where product="CLG0" AND DATE="2010-01-05" order by date,time' )
    r = db.cur.fetchall()
    cci = Idx.cci( r, 14 )
    cci = Idx.boll( r, 20 )

