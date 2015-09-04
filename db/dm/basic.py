# coding=utf-8
import sys
sys.path.append("..")

from swampy.Lumpy import *
#lumpy = Lumpy()
#lumpy.make_reference()

import os
import datetime
import time

class DebugTool( object ):
    @classmethod
    def getStackFun( cls, which = None ):
        import traceback
        x = traceback.extract_stack()
        x.reverse()
        i = -1
        for level in x:
            i = i + 1
            if level[2] == '<module>':
                break
        return x[i - 1][2]

class VosTool( object ):
    day1Delta = datetime.date( 2000, 1, 2 ) - datetime.date( 2000, 1, 1 )
    logDir = '..\output'
    @classmethod
    def dateStrCalc( cls, dayStr, days, denominator = 1 ):
        e = dayStr.split( '-' )
        if len( e ) != 3:
            raise Exception
        localDay = datetime.date( int( e[0] ), int( e[1] ), int( e[2] ) ) + days * VosTool.day1Delta / denominator
        return '%s-%02i-%02i' % ( localDay.year, localDay.month, localDay.day )

    @classmethod
    def log( cls, info, fn = '' ):
        if '' == fn:
            fn = DebugTool.getStackFun()
        fp = open( os.path.join( cls.logDir, fn ), 'a' )
        fp.write( '%s: \r\n' % cls.timeTagStr() )
        fp.write( info )
        fp.close()

    @classmethod
    def timeTagStr( cls , format = '' ):
        now = datetime.datetime.now()
        if format == 'long':
            return '%04i%02i%02i%02i%02i%02i%06i' % ( now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond )
        else:
            return '%04i%02i%02i%02i%02i%02i' % ( now.year, now.month, now.day, now.hour, now.minute, now.second )

    @classmethod
    def launch( cls, appPath, maxSecs, winTitle ):
        wsh = win32com.client.Dispatch( "Wscript.Shell" )
        wsh.run( appPath )
        if not cls.waitWin( winTitle, maxSecs ):
            print( 'waitWin Fail: % s' % winTitle )
            return False

    @classmethod
    def waitWin( cls, WinName, seconds ):
        try:
            wsh = win32com.client.Dispatch( "Wscript.Shell" )
            i = 0
            while False == wsh.AppActivate( ' % s' % WinName ):
                time.sleep( 1 )
                i = i + 1
                if i > seconds:
                    print( 'overtime:%d' % seconds )
                    return False
            return True
        except:
            print( 'exception in waitWin' )
            return False

class F1ofMinF2:
    def __init__( self ):
        self.f1 = None
        self.f2 = None

    def step( self, f1, f2 ):
        if self.f1 == None:
            self.f1 = f1
            self.f2 = f2
        elif f2 < self.f2:
            self.f1 = f1
            self.f2 = f2

    def finalize( self ):
        return self.f1

class F1ofMaxF2:
    def __init__( self ):
        self.f1 = None
        self.f2 = None

    def step( self, f1, f2 ):
        if self.f1 == None:
            self.f1 = f1
            self.f2 = f2
        elif f2 > self.f2:
            self.f1 = f1
            self.f2 = f2

    def finalize( self ):
        return self.f1

# 数据库结构规则: _tblstru表存储各表表名和字段名,_tblkeys...
# 初始化: 如果db文件名为空则新建内存数据库, 如果文件不存在则创建db,存在则打开db并建立conn
class Db( object ):
    _dbFile = ''
    dbSchema = {}
    cur = None
    conn = None
    code = ''
    def __init__( self, fn = '', code = '' ):
        def string( para ):
            return str( para )

        def timeRound( timeStr, span ):  # 01:02, 2009-01-02 01:02:03
            if span <= 60:
                l = timeStr.split( ":" )
                min = '%02i' % ( int( l[1] ) / span * span )
                return '%s:%s' % ( l[0], min )
            elif span <= 60 * 24:
                # only fit for 01:02, not consider 2009-01-02 01:02:03 yet 
                span = span / 60
                l = timeStr.split( ":" )
                hour = '%02i' % ( int( l[0] ) / span * span )
                return '%s:%s' % ( hour, l[1] )

        import sqlite3
        newDbFile = True
        if fn:
            self._dbFile = fn
            if os.path.exists( fn ):
                newDbFile = False
                print 'db file found, to be read: %s' % fn
            else:
                print 'db file not exists, to be creat: %s' % fn
            self.conn = sqlite3.connect( fn )
        else:
            self.conn = sqlite3.connect( ':memory:' )
        self.cur = self.conn.cursor()
        self.conn.text_factory = str
        self.conn.create_function( "string", 1, string )
        self.conn.create_function( "timeRound", 2, timeRound )
        self.conn.create_aggregate( "F1ofMaxF2", 2, F1ofMaxF2 )
        self.conn.create_aggregate( "F1ofMinF2", 2, F1ofMinF2 )
        #self.conn.create_function( "md5", 1, md5sum )
        if newDbFile == True:
            self.cur.execute( 'create table if not exists _tblstru(_tblname text, f0 text, f1 text default Null, f2 text default Null, f3 text default Null, f4 text default Null, f5 text default Null, f6 text default Null, f7 text default Null, f8 text default Null, f9 text default Null, f10 text default Null, f11 text default Null, f12 text default Null, f13 text default Null, f14 text default Null, f15 text default Null)' )
            self.cur.execute( 'create table if not exists _tblkeys(_tblname text, f0 text, f1 text default Null, f2 text default Null, f3 text default Null, f4 text default Null, f5 text default Null, f6 text default Null, f7 text default Null, f8 text default Null, f9 text default Null, f10 text default Null, f11 text default Null, f12 text default Null, f13 text default Null, f14 text default Null, f15 text default Null)' )
        self.code = code
        self._getDbSchema()
    def __del__( self ):
        # self.cur.execute( 'commit' )
        self.conn.commit()
        if self._dbFile == '':
            self.persist()
        self.cur.close()
        self.conn.close()
    def persist( self ):
        pass
    def newTbl( self, name, struc ):
        colRecInserted = '"%s"' % name
        struCols = '_tblname'
        self.dbSchema[ name ] = []
        struCreated = ''
        i = 0
        for fld in struc:
            self.dbSchema[ name ].append( fld )

            struCreated = '%s, "%s" text' % ( struCreated, fld )
            colRecInserted = '%s,"%s"' % ( colRecInserted, fld )
            struCols = '%s,f%s' % ( struCols, i )
            i = i + 1
        self.cur.execute( 'create table "%s"(%s)' % ( name, struCreated[1:] ) )
        self.cur.execute( 'insert into _tblstru (%s) values(%s)' % ( struCols, colRecInserted ) )
        self.conn.commit()
    def newRec( self, tblName, rec ):
        recInserted = ''
        cols = ''
        for fld in rec:
            recInserted = '%s,"%s"' % ( recInserted , rec[fld] )
            cols = '%s,"%s"' % ( cols, fld )
        self.cur.execute( 'insert into "%s" (%s) values(%s)' % ( tblName, cols[1:], recInserted[1:] ) )
    def _getDbSchema( self ):  # get schema of database
        self.cur.execute( 'select * from _tblstru' )
        for rec in self.cur.fetchall():
            tblName = rec[0]
            if self.code:
                tblName = rec[0].decode( 'utf-8' )
            self.dbSchema[ tblName ] = []

            fldLst = list( set( rec[1:] ) )
            fldLst.sort()
            fldLst.remove( None )
            for fld in fldLst:
                if self.code:
                    self.dbSchema[ tblName ].append( fld.decode( 'utf-8' ) )
                else:
                    self.dbSchema[ tblName ].append( fld )

    @classmethod
    def testMe( cls ):
        symbol = 'RHAT'
        db = cls( r'.\data\testPySqlite.db' )
        db.cur.execute( "select * from stocks where symbol = '%s'" % symbol )
        x = db.cur.fetchall()
        # Create table
        db.cur.execute( '''create table if not exists stocks (date text, trans text, symbol text, qty real, price real)''' )
        # Insert a row of data
        db.cur.execute( """insert into stocks values ('%s','BUY','RHAT',100,35.14)""" % VosTool.timeTagStr() )
        # Never do this -- insecure!
        db.cur.execute( "select * from stocks where symbol = '%s'" % symbol )
        y = db.cur.fetchall()
        # Do this instead
        t = ( symbol, )
        db.cur.execute( 'select * from stocks where symbol=?', t )
        z = db.cur.fetchall()
        print 'x got is: %r' % x
        print 'y got is: %r' % y
        print 'z got is: %r' % z

        import locale
        encoding = locale.getdefaultlocale()[1]
        from codecs import decode

        db.conn.text_factory = str
        db.cur.execute( "create table if not exists person(lastname, firstname)" )
        db.cur.execute( "insert into person(lastname,firstname) values(%s,%s)" % ( 'three', 'zhang' ) )
        db.cur.execute( "insert into person(lastname,firstname) values(%s,%s)" % ( 'four', 'li' ) )
        db.cur.execute( "select * from person" )
        temp = db.cur.fetchall()
        print temp
        '''
        print str( 'the first record' ).decode( encoding ) + str( temp[0][1] ).decode( encoding ) + str( temp[0][0] ).decode( encoding )
        print str( 'the second record' ).decode( encoding ) + str( temp[1][1] ).decode( encoding ) + str( temp[1][0] ).decode( encoding )
        assert str( temp[0][1] ).decode( encoding ) + str( temp[0][0] ).decode( encoding ) == str( "zhangsan" ).decode( encoding )
        '''


class StructData( object ):
    _dbFile = ''
    dataGot = {}
    hisStru = []
    #structs = {}
    #conn = None
    _db = None
    dataGot = {}
    ''' It means no table name if tlb1/tbl2 is number, same rule for field name(add a character prefix for actual numeric table/field name while handling data)
    dataGot = {tbl1:{'title':[],
                     'keys': [],
                     'records':[[],
                                []
                               ]},
               tbl2:{}
              }
    '''
    tableNum = -1
    def __init__( self, dbFile = '' ):
        self._dbFile = dbFile
    def addTbl( self, name = '' ):
        if name:
            if name in self.dataGot.keys():
                return
            tblName = name
        self.tableNum = self.tableNum + 1
        tblName = self.tableNum
        self.dataGot[ tblName ] = {}
        self.dataGot[ tblName ]['title'] = []
        self.dataGot[ tblName ]['records'] = []
    def alterTblName( self, oldName, newName ):
        if newName in self.dataGot.keys():
            if self.dataGot[oldName]['title'] != self.dataGot[newName]['title']:
                print 'same name for tow different table'
                raise Exception
            for rec in self.dataGot[oldName]['records']:
                self.dataGot[newName]['records'].append( rec )
        else:
            self.dataGot[newName] = self.dataGot[oldName]
        del self.dataGot[oldName]
    def newCol( self, tblName, name = '' ):
        fldName = name
        if name == '':
            fldName = len( self.dataGot[ tblName ]['title'] )
        self.dataGot[ tblName ]['title'].append( fldName )
    def defKey( self, tblName, keyLst = [] ):
        if keyLst == []:
            print 'please specify key columns'
            return False
        if self.dataGot[ tblName ].has_key( 'keys' ) and self.dataGot[ tblName ]['keys'] != []:
            print 'key columns already exist'
            return False
        if set( keyLst ) <= set( self.dataGot[ tblName ]['title'] ):
            self.dataGot[ tblName ]['keys'] = keyLst
            if self._db:
                struCreated = ''
                keys = ''
                for fld in self.dataGot[tblName]['title']:
                    struCreated = '%s, "%s" text' % ( struCreated, fld )
                    if fld in keyLst:
                        keys = '%s,"%s"' % ( keys, fld )
                tmpName = '_tmp%s' % VosTool.timeTagStr()
                self._db.cur.execute( 'create table "%s"(%s, primary key(%s))' % ( tmpName, struCreated[1:], keys[1:] ) )
                self._db.cur.execute( 'insert into "%s" select * from "%s"' % ( tmpName, tblName ) )
                self._db.cur.execute( 'alter table "%s" rename to "%s"' % ( tblName, '%s_%s_bak' % ( tblName, VosTool.timeTagStr() ) ) )
                self._db.cur.execute( 'alter table "%s" rename to "%s"' % ( tmpName, tblName ) )
        else:
            print 'key columns specified not found'
            return False
    def addRec( self, tblName ):
        self.dataGot[ tblName ]['records'].append( [] )
    def addFldData( self, tblName, data, recId = -1 ):
        self.dataGot[ tblName ]['records'][recId].append( data )
    def save2Db( self, keyLst = {}, code = '' ):
        self._db = Db( self._dbFile, code )
        from codecs import encode, decode
        tblLst = self.dataGot.keys()
        noName = True
        for tbl in tblLst:
            if type( tbl ) != type( 0 ):
                noName = False
                break
        for tbl in tblLst:
            tblName = ''
            if not noName:
                tblName = tbl
            tblExist = False
            fldLst = list( set( self.dataGot[tbl]['title'] ) )
            fldLst.sort()
            for stru in self._db.dbSchema:
                if fldLst == self._db.dbSchema[stru]:
                    if not noName and tbl != stru:
                        continue
                    tblName = stru
                    tblExist = True
                    if noName:
                        self.alterTblName( tbl, tblName )
                    self._db.cur.execute( 'select * from _tblkeys where _tblname="%s"' % tblName )
                    rslt = self._db.cur.fetchall()
                    if rslt:
                        self.dataGot[tblName]['keys'] = rslt[0][1:]
                    break
            keyIdLst = []
            if tblExist == False:
                if noName:
                    tblName = '_t%s' % VosTool.timeTagStr( 'long' )
                    self.alterTblName( tbl, tblName )
                colRecInserted = '"%s"' % tblName
                struCols = '_tblname'
                struCreated = ''
                i = 0
                for fld in self.dataGot[tblName]['title']:
                    struCreated = '%s, "%s" text' % ( struCreated, fld )
                    colRecInserted = '%s,"%s"' % ( colRecInserted, fld )
                    struCols = '%s,f%s' % ( struCols, i )
                    i = i + 1
                self._db.cur.execute( 'create table "%s"(%s)' % ( tblName, struCreated[1:] ) )
                self._db.cur.execute( 'insert into _tblstru (%s) values(%s)' % ( struCols, colRecInserted ) )

                if keyLst:
                    pass
                    ''' how???
                    self.defKey( tblName, keyLst )
                    for key in keyLst:
                        keyIdLst.append( self.dataGot[tblName]['title'].index( key ) )
                    '''
            elif self.dataGot[tblName].has_key( 'keys' ):
                for key in self.dataGot[tblName]['keys']:
                    keyIdLst.append( self.dataGot[tblName]['title'].index( key ) )
            for rec in self.dataGot[tblName]['records']:
                recExist = False
                cond = ''
                if keyIdLst:
                    i = 0
                    for fld in rec:
                        if i in keyIdLst:
                            cond = '%s and "%s"="%s"' % ( cond, self.dataGot[tblName]['title'][i], rec[i] )
                        i = i + 1
                    self._db.cur.execute( 'select * from "%s" where 1=1 %s' % ( tblName, cond[1:] ) )
                    if self._db.cur.fetchall():
                        recExist = True
                if recExist:
                    recUpdated = ''
                    i = 0
                    for fld in rec:
                        recUpdated = '%s,"%s"="%s"' % ( recUpdated , self.dataGot[tblName]['title'][i], fld )
                        i = i + 1
                    self._db.cur.execute( 'update "%s" set %s where 1=1 %s' % ( tblName, recUpdated[1:], cond[1:] ) )
                else:
                    # may seemed to simply using only one insert sentence to replace following code (self.dataGot[tblName]['title'] and rec)
                    recInserted = ''
                    cols = ''
                    i = 0
                    for fld in rec:
                        recInserted = '%s,"%s"' % ( recInserted , fld )
                        cols = '%s,"%s"' % ( cols, self.dataGot[tblName]['title'][i] )
                        i = i + 1
                    self._db.cur.execute( 'insert into "%s" (%s) values(%s)' % ( tblName, cols[1:], recInserted[1:] ) )
            #self._db.cur.execute( 'select count(*) from %s' % tblName )
            #r = self._db.cur.fetchall()
        self._db.conn.commit()

class App( object ):
    appName = ''
    _dbFile = ''

# 根据模型对数据库进行调整,
class ERMap( object ):
    entityDict = {}
    db = None
    def __init__( self, dict = {}, dbf = '' ):
        if dict:
            self.entityDict = dict
        if dbf:
            self.db = Db( dbf )
    def cascade2Db( self ):  # apply structure definition in entityDictionary to database. Need detail strategy, 
                             # simply create new table at present
        for e in self.entityDict:
            if self.db.dbSchema.has_key( e ):
                continue
            self.db.newTbl( e, self.entityDict[e] )
        # whether remove table not found in entityDict
        # how to deal the structure difference 
    def compareDictWithDb( self ): # 
        pass

class Mt4ErMap( ERMap ):
    title0 = ['product', 'date', 'time', 'close', 'sequence', 'logtime', 'amount']
    title = ['product', 'date', 'time', 'open', 'high', 'low', 'close', 'amount']
    entityDict = {'real':title0,
                  'min1K':title,
                  'min5K':title,
                  'min15K':title,
                  'min30K':title,
                  'hour1K':title,
                  'hour4K':title,
                  'dayK':title,
                  'weekK':title,
                  'monthK':title,
                 }
    def __init__( self, dbf = '' ):
        ERMap.__init__( self, dbf = dbf )

class Mt4XlsData( Mt4ErMap ):
    def __init__( self, fn = '' ):
        Mt4ErMap.__init__( self, 'mt4csv.db') #-new.db' )
        if fn:
            from win32com.client import Dispatch
            self.xls = Dispatch( 'Excel.Application' )
            #self.xls.Visible = 1
            fn = os.path.abspath( fn )
            self.xls.DisplayAlerts = False
            self.book = self.xls.Workbooks.Open( fn )  # absolute path
            self.xls.DisplayAlerts = False
            self.cascade2Db()
            self.transData2Db()
            self.xls.Save()
            self.xls.Quit()
    def transData2Db( self ):
        import pywintypes
        timeDiff = 8
        shtLst = []
        for i in range( 1, self.book.Sheets.Count ):
            shtLst.append( self.book.Sheets( i ).Name.lower() )
            if shtLst[-1] in ( 'product', 'sheet1' ):
                shtLst.remove( shtLst[-1] )
        shtLst.sort()
        for i, sht in enumerate( shtLst ):
            localDate = '%s-%s-%s' % ( sht[:4], sht[4:6], sht[6:8] )
            if int( sht[-2:] ) < 8:
                localDate = VosTool.dateStrCalc( localDate, -1 )
            for row in range( 2, self.book.Sheets( sht ).UsedRange.Rows.Count ):
                rec = {}
                rec['date'] = localDate
                try:
                    rec['product'] = self.book.Sheets( sht ).Cells( row, 1 ).Text
                    rec['close'] = self.book.Sheets( sht ).Cells( row, 2 ).Text
                    rec['time'] = self.book.Sheets( sht ).Cells( row, 6 ).Text
                except pywintypes.com_error, ex:
                    if ex[0] in [-2147417846, -2147418111]:
                        VosTool.log( 'excel busy', 'dealmt4xls' )
                        time.sleep( 2.0 )
                        try:
                            rec['product'] = self.book.Sheets( sht ).Cells( row, 1 ).Text
                            rec['close'] = self.book.Sheets( sht ).Cells( row, 2 ).Text
                            rec['time'] = self.book.Sheets( sht ).Cells( row, 6 ).Text
                        except pywintypes.com_error, ex:
                            if ex[0] in [-2147417846, -2147418111]:
                                VosTool.log( 'excel busy', 'dealmt4xls' )
                                time.sleep( 2.0 )
                                try:
                                    rec['product'] = self.book.Sheets( sht ).Cells( row, 1 ).Text
                                    rec['close'] = self.book.Sheets( sht ).Cells( row, 2 ).Text
                                    rec['time'] = self.book.Sheets( sht ).Cells( row, 6 ).Text
                                except pywintypes.com_error, ex:
                                    if ex[0] in [-2147417846, -2147418111]:
                                        VosTool.log( 'excel busy', 'dealmt4xls' )
                                        time.sleep( 2.0 )
                                        rec['product'] = self.book.Sheets( sht ).Cells( row, 1 ).Text
                                        rec['close'] = self.book.Sheets( sht ).Cells( row, 2 ).Text
                                        rec['time'] = self.book.Sheets( sht ).Cells( row, 6 ).Text
                for e in rec:
                    if '#N/A' == rec[e]:
                        print sht, row, rec
                        break
                else:
                  try:
                    if rec['time'].find( ' ' ) >= 0:
                        rec['date'], rec['time'] = rec['time'].split( ' ' )
                    else:  # the time error is supposed to less than 1 hour
                      try:
                        hour = int( rec['time'].split( ':' )[0] )
                        if int( sht[-2:] ) != ( hour + timeDiff ) % 24:
                            if ( int( sht[-2:] ) == 7 ) and ( hour == 0 ):
                                rec['date'] = VosTool.dateStrCalc( localDate, 1 )
                            elif  ( int( sht[-2:] ) == 8 ) and ( hour == 23 ):
                                rec['date'] = VosTool.dateStrCalc( localDate, -1 )
                            else:
                                print sht, row, rec
                                #raise Exception
                      except:
                          x = 1
                    if len( rec['time'] ) != 5:
                        l = rec['time'].split( ':' )
                        rec['time'] = '%02i:%02i' % ( int( l[0] ), int( l[1] ) )
                    rec['sequence'] = row
                    rec['logtime'] = sht
                    self.db.newRec( 'real', rec )
                  except:
                      x = 1
            self.db.conn.commit()
            if i < len( shtLst ) - 1:
                self.xls.DisplayAlerts = False
                self.book.Sheets( sht ).Delete()
    def getKData( self, srcName, destName ):
        # do something to check data
        getSqlStr = "Select product, date, time, F1ofMinF2(close,rowid) as open, max(close) as high, min(close) as low, F1ofMaxF2(close,rowid) as close, sum(amount) as amount From %s group by product,date,time" % srcName
        self.db.cur.execute( 'insert into %s(product,date,time,open,high,low,close,amount) %s' % ( destName, getSqlStr ) )
        self.db.conn.commit()

    def aggrKData( self, srcName, destName, scale ):
        # do something to check data
        getSqlStr = "Select product, date, timeRound(time,%i) as time, F1ofMinF2(open,rowid) as open, max(high) as high, min(low) as low, F1ofMaxF2(close,rowid) as close, sum(amount) as amount From %s group by product,date,timeRound(time,%i)" % ( scale, srcName, scale )
        self.db.cur.execute( 'insert into %s(product,date,time,open,high,low,close,amount) %s' % ( destName, getSqlStr ) )
        self.db.conn.commit()

        #self.db.cur.execute( 'insert into min1K(product,date,time,open,high,low,close) %s' % getSqlStr )
        #self.db.cur.execute( 'update min1K set open=%s.close from %s where %s.rowid=min1K.open'%(srcName,srcName,srcName) )
        #self.db.conn.commit()

    def getKData1( self, srcName, destName, scale = 1 ):
        # do something to check data
        #getSqlStr = 'Select product, date, time, min(rowid) as open, max(close) as high, min(close) as low, max(rowid) as close, sum(amount) as amount From %s group by product,date,time' % ( srcName )
        #if scale != 1:
        secs = scale * 60
        getSqlStr = "Select product, date, %i*((strftime('%%s',time)%%86400)/%i) as time, min(rowid) as open, max(close) as high, min(close) as low, max(rowid) as close, sum(amount) as amount From %s group by product,date,%i*((strftime('%%s',time)%%86400)/%i)" % ( secs, secs, srcName, secs, secs )
        self.db.cur.execute( 'create temp table _tmp as %s' % getSqlStr )
        sql1 = 'select _tmp.product as product, _tmp.date as date, _tmp.time as time, %s.close as open, _tmp.high as high, _tmp.low as low, _tmp.close as close, _tmp.amount as amount from _tmp,%s where _tmp.open=%s.rowid' % ( srcName, srcName, srcName )
        self.db.cur.execute( 'create temp table _tmp1 as %s' % sql1 )
        self.db.conn.commit()
        #self.db.cur.execute( 'select product,date from _tmp1 limit 200' )
        #r = self.db.cur.fetchall()
        #self.db.cur.execute( 'select count(*) from _tmp1' )
        #r = self.db.cur.fetchall()

        #sql2 = 'select _tmp1.product as product, _tmp1.date as date, _tmp1.time/3600||":"||_tmp1.time/60 as time, _tmp1.open as open, _tmp1.high as high, _tmp1.low as low, %s.close as close, _tmp1.amount as amount  from _tmp1,%s where _tmp1.close=%s.rowid' % ( srcName, srcName, srcName )
        sql2 = 'select _tmp1.product as product, _tmp1.date as date, _tmp1.time/3600 as h, (_tmp1.time%3600)/60 as m, _tmp1.open as open, _tmp1.high as high, _tmp1.low as low, real.close as close, _tmp1.amount as amount  from _tmp1,real where _tmp1.close=real.rowid'
        self.db.cur.execute( 'create temp table _tmp2 as %s' % sql2 )
        sql3 = 'select product, date, h || ":" || m as time, open, high, low, close, amount from _tmp2'
        self.db.cur.execute( 'insert into %s(product,date,time,open,high,low,close,amount) %s' % ( destName, sql3 ) )
        self.db.conn.commit()

        #self.db.cur.execute( 'insert into min1K(product,date,time,open,high,low,close) %s' % getSqlStr )
        #self.db.cur.execute( 'update min1K set open=%s.close from %s where %s.rowid=min1K.open'%(srcName,srcName,srcName) )
        #self.db.conn.commit()

def testXls():
    #excel simply write file 
    #a.py 
    from win32com.client import Dispatch
    xls = Dispatch( 'Excel.Application' )
    #xls.Visible = 1

    #rxls.py  simply read xls file
    book = xls.Workbooks.Open( r'D:\autotrade\data\MT4DDEDATA.xls' )  # absolute path 
    #n = book.ActiveSheet
    #print n.Name
    shtLst = []
    for i in range( 1, book.Sheets.Count ):
        shtLst.append( book.Sheets( i ).Name.lower() )
        if shtLst[-1] in ( 'product', 'sheet1' ):
            shtLst.remove( shtLst[-1] )
    shtLst.sort()

    book = xls.Workbooks.Open( r'D:\autotrade\data\1.xls' )  # absolute path 
    n = book.Sheets( 'sheet2' )
    m = n.Cells( 1, 6 ).Value
    m = n.Cells( 1, 6 ).Value
    m = n.Cells( 1, 6 ).Value
    book.Sheets( 1 ).Cells( 2, 2 ).Value = 22.2
    book.Sheets( 2 ).Cells( 3, 3 ).Value = 33.3
    book.Sheets( 3 ).Cells( 4, 4 ).Value = 44.4
    m = n.Cells( 1, 6 ).Value
    m = n.Cells( 1, 6 ).Value
    xls.Cells( 11, 2 ).Value = 123456
    #book.close()
    print m

    xls.Workbooks.Add()
    xls.Cells( 31, 1 ).Value = 2
    book = xls.Workbooks( 2 )
    xls.Sheets.Add()
    sheet = xls.Sheets( 4 )
    sheet.Name = 'old3'
    sheet.Cells( 1, 1 ).Value = '123'
    sheet4 = xls.Sheets( 'Sheet4' )
    sheet4.Cells( 1, 1 ).Value = '123'
    book.SaveAs( r'.\data\2.xlsx' )
    n = book.ActiveSheet
    #book.SaveAs( Filename = '.\data\SPT_GLD1440.xls' )
    xls.Quit()

if __name__ == '__main__':
    VosTool.log( 'afds' )
    #x = Mt4ErMap( 'test.db' )
    #x.cascade2Db()

    x = Mt4XlsData( )#'.\data\MT4DDEDATA-tmp.xls')#-new.xls' )  #'.\data\MT4DDEDATA--.xls' )
    #x = Mt4XlsData()
    lumpy.object_diagram()
    lumpy.class_diagram()

    x.getKData( 'real', 'min1K' )
    x.aggrKData( 'min1K', 'min5K', 5 )
    x.aggrKData( 'min5K', 'min15K', 15 )
    x.aggrKData( 'min15K', 'min30K', 30 )
    x.aggrKData( 'min30K', 'hour1K', 60 )
    x.aggrKData( 'hour1K', 'hour4K', 240 )

    s = 'a'
    print s
    s = u'aa啊'
    print s
    testXls()

    import win32ui
    import dde
    serv = dde.CreateServer()
    serv = Create( 'client' )
    conv = dde.CreateConversation( serv )
    servname = 'Excel'
    conv.ConnectTo( servname, 'sheet1' )
    conv.Request( 'a1' )

    # Db.testMe()
    # VosTool.log( '' )


'''
1 fill date
2 Select product,"date","time",min(rowid) as open, max(rowid) as close, max(close) as high, min(close) as low From MAIN.[real] group by product,"date","time"
  minmax(logtime)
3 open, close
sqlite的速度：升级版本，加内存

pywin32如何跳过重新打开一个xls文件的提示

code编码集合何处指定
initDb
关键字定义
阶段性数据/实时连续数据的不同特点和相应处理方式


code编码集合何处指定
initDb
关键字定义
阶段性数据 / 实时连续数据的不同特点和相应处理方式

知识相对论、思想相对论: 同构相对圈（系统）
'''
# 测试
