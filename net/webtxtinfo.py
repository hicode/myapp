# coding=utf-8
#-*- coding utf8 -*-
from sgmllib import SGMLParser
import os
import urllib
from basic import *

class WebTxtInfo( SGMLParser, App ):
    _srcUrl = ''
    htmlData = ''
    structData = None
    def __init__( self, fn = '' ):  #, url ):
        SGMLParser.__init__( self )
        if fn:
            fp = open( fn )
            self.htmlData = fp.read()
            fp.close()
        else:
            urllink = urllib.urlopen( self._srcUrl )
            self.htmlData = urllink.read()
            urllink.close()
            fn = DebugTool.getStackFun()
            fp = open( os.path.join( '.\data', '%s-%s.html' % ( fn , VosTool.timeTagStr() ) ), 'w' )
            fp.write( self.htmlData )
            fp.close()

    def reset( self ):
        SGMLParser.reset( self )
        #self.dataGot = {}

    def analyseData( self, keyLst = {}, code = '' ):
        self.structData = StructData( self._dbFile )
        self.feed( self.htmlData )
        self.structData.save2Db( keyLst, code )
        self.structData = None

class SzseQz( WebTxtInfo ):
    _dbFile = r'.\data\szqz.db'
    _srcUrl = r"http://www.szse.cn/main/disclosure/news/qzjygkxx/"

class StockQ( WebTxtInfo ):
    _dbFile = r'.\data\stockq.db'
    _srcUrl = r"http://stockq.cn/"  #http://www.stockq.org/"
    inTable = False
    inHead = False
    inRecord = False
    inField = False
    curTblName = ''
    titleLst = []
    curFieldVal = ''
    headFieldType = ''

    def start_table( self, attrs ):
        for attr in attrs:
            if attr[0] == 'class' and attr[1] == 'marketdatatable':
                break
        else:
            return
        self.inTable = True
        self.curTblName = ''
        self.structData.addTbl()
    def end_table( self ):
        self.curTblName = ''
        self.inTable = False
    def start_tr( self, attrs ):
        if self.inTable != True: return
        for attr in attrs:
            if attr[0] == 'class' and attr[1] in ['row1', 'row2']:
                self.inRecord = True
                self.structData.addRec( self.curTblName )
                break
        else:
            self.inHead = True
    def end_tr( self ):
        if self.inTable != True: return
        if self.inHead == True:
            if self.headFieldType == 'fld':
                self.structData.alterTblName( self.structData.tableNum, self.curTblName )
            self.inHead = False
            self.headFieldType = ''
        elif self.inRecord == True:
            self.inRecord = False
        else:
            print 'error format found, am i in head or in record?'
            raise Exception
    def start_td( self, attrs ):
        if self.inTable != True: return
        self.inField = True
        if self.inHead == True:
            self.curFieldVal = ''
            for attr in attrs:
                if attr[0] == 'class' and attr[1] in ['tabletitle', 'aa', 'style5']:
                    self.headFieldType = 'tbl'
                    break
            else:
                    self.headFieldType = 'fld'
        elif self.inRecord == True:
            pass
        else:
            print 'error format found, am i in head or in record?'
            raise Exception
    def end_td( self ):
        if self.inTable != True: return
        #self.curFieldVal = self.curFieldVal[1:]
        if self.inHead == True:
            if self.headFieldType == 'tbl':
                self.curTblName = self.curFieldVal.replace( '\\', '' )
                self.curTblName = self.curTblName.replace( '/', '' )
                self.curTblName = self.curTblName.replace( ' ', '' )
                self.curTblName = self.curTblName.replace( '(', '' )
                self.curTblName = self.curTblName.replace( ')', '' )
                self.curTblName = self.curTblName.replace( '%', '' )
                if self.curTblName == '':
                    print 'table name is empty, please check logic of data analyse'
                    raise Exception
            else:
                self.structData.newCol( self.structData.tableNum, self.curFieldVal )
                '''
                if self.curTblName == '':
                else:
                    self.structData.newCol( self.curTblName, self.curFieldVal )
                '''
        elif self.inRecord == True:
            self.structData.addFldData( self.curTblName, self.curFieldVal )
        else:
            print( 'what is this data: %s' % text )
        self.inField = False
        self.curFieldVal = ''
    def handle_data( self, text ):
        if self.inTable != True: return
        if not text.strip(): return
        self.curFieldVal = '%s%s' % ( self.curFieldVal, text.strip() )  #%s|%s

class SinaVip( WebTxtInfo ):
    _dbFile = r'.\data\sinavip.db'
    _srcUrl = r"http://vip.stock.finance.sina.com.cn/forex/view/vDailyFX_More.php"
    inTable = False
    inHead = False
    inData = False
    inRecord = False
    #inHeadField = False
    inRecField = False
    curFieldVal = ''

    def start_table( self, attrs ):
        self.inTable = True
        self.structData.addTbl()
    def end_table( self ):
        self.inTable = False
    def start_thead( self, attrs ):
        if self.inTable != True: return
        self.inHead = True
    def end_thead( self ):
        if self.inTable != True: return
        self.inHead = False
    def start_tbody( self, attrs ):
        if self.inTable != True: return
        self.inData = True
    def end_tbody( self ):
        if self.inTable != True: return
        self.inData = False
    def start_tr( self, attrs ):
        if self.inTable != True: return
        if self.inHead:
            pass
        elif self.inData:
            self.inRecord = True
            self.structData.addRec( self.structData.tableNum )
        else:
            print( 'what is this data: %s, either in head or data of a table' % attrs )
            assert False
    def end_tr( self ):
        if self.inTable != True: return
        if self.inHead:
            pass
        elif self.inData:
            self.inRecord = False
        else:
            print( 'what type of data end is this, either in head or data of a table' )
            assert False
    def start_th( self, attrs ):
        if self.inTable != True: return
        self.curFieldVal = ''
    def end_th( self ):
        if self.inTable != True: return
        if self.inData:
            self.structData.addFldData( self.structData.tableNum, self.curFieldVal )
        elif self.inHead:
            self.structData.newCol( self.structData.tableNum, self.curFieldVal )
        else:
            print( 'what type of data is this, either in head or data of a table' )
        self.curFieldVal = ''
    def start_td( self, attrs ):
        if self.inTable != True: return
        assert self.inRecord
        self.inRecField = True
        self.curFieldVal = ''
    def end_td( self ):
        if self.inTable != True: return
        assert self.inRecField
        self.structData.addFldData( self.structData.tableNum, self.curFieldVal )
        self.curFieldVal = ''
        self.inRecField = False
    def handle_data( self, text ):
        if self.inTable != True:
            return
        if not text.strip():
            return
        self.curFieldVal = '%s%s' % ( self.curFieldVal, unicode( text ).strip() )  #%s|%s

'''
logic = {'table':{inTbl = True,
                'thead':{inhead = True,
                         'tr':{}
                         }
                'tbody':{indata = True,
                         'tr':{}
                         }
               }
      }
'''

if __name__ == '__main__':
    VosTool.log( 'afds' )

    #x = sinaVip( r'.\data\webdataSinaVip.txt' )
    x = SinaVip()
    x.analyseData( code = 'utf-8' )
    x = None

    x = StockQ()
    #x = StockQ( r'.\data\__init__-20091215224414.html' )
    x.analyseData()
    x = None

    x = SzseQz()
    x.analyseData()
    x = None


# 每次有新的数据源, 应先解析给出表结构, 
#    然后指定并记录保存每个表的关键字, 每个字段的语义(越大越好还是越小越好,单位, 常态范围, 异态?)
#表字段命名的特殊字符处理
#数据中的特殊字符处理
#定时自动任务的结果检查确认和重试
#数据项目数据字典可视化
# 广告真实法
# 美元瞬间崩溃应急分析：人民币汇率脱钩？/不变？或...？
