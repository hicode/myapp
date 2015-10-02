# coding=utf-8

#import sqlite3
#conn = sqlite3.connect(r'D:\GitHub\myapp\net\website\django\mysite1\db.sqlite3')
#from selenium import webdriver

prjPath = r'E:\GitHub\myapp\net\website\django\mysite1'
dataPath = r'D:\data'

import time
from datetime import datetime
from net.url.dataSource import regDataFromUrl, dataFromUrl
import re
import codecs
import django
import sys
#from net.website.django.mysite1.myapp.rules import Submarket
sys.path.append( prjPath )
django.setup()
from myapp.rules import Submarket # net.website.django.mysite1.

from myapp.models import Product_, Product, KDaily, KMin, WatchList, Market, StockInfo, TradeRealTime

'''
sina level2

http://stock.gtimg.cn/data/get_hs_xls.php?id=rankfund&type=1&metric=name
http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr

http://app.finance.ifeng.com/hq/list.php?type=bond

http://app.finance.ifeng.com/hq/list.php?type=usstock
http://app.finance.ifeng.com/hq/list.php?type=hkstock&class=wl
http://app.finance.ifeng.com/hq/list.php?type=hkstock&class=gp
http://app.finance.ifeng.com/hq/list.php?type=hkstock

http://app.finance.ifeng.com/hq/list.php?type=fund&class=kf
http://app.finance.ifeng.com/hq/list.php?type=fund&class=fb
http://app.finance.ifeng.com/hq/list.php?type=fund

http://app.finance.ifeng.com/hq/list.php?type=stock_b&class=sb
http://app.finance.ifeng.com/hq/list.php?type=stock_b&class=hb
http://app.finance.ifeng.com/hq/list.php?type=stock_b
http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=qz
http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=gem
http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=sa
http://app.finance.ifeng.com/hq/list.php?type=stock_a&class=ha
http://app.finance.ifeng.com/hq/list.php?type=stock_a
'''

def getHKProdLst():
    url = r'http://app.finance.ifeng.com/hq/list.php?type=hkstock'  # ({val:"600000",val2:"浦发银行",val3:"pfyx"})
    formatStr = r'[(]{(.+?)}[)]'
    browser = webdriver.Chrome()
    browser.get(url)
    
    result = regDataFromUrl(url, 10, formatStr)
    prodLst = []
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    return prodLst

def getSSEProdLst():
    url = r'http://www.sse.com.cn/js/common/ssesuggestdata.js'  # ({val:"600000",val2:"浦发银行",val3:"pfyx"})
    formatStr = r'[(]{(.+?)}[)]'
    result = regDataFromUrl(url, 10, formatStr)
    prodLst = []
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    return prodLst

def getSZSEProdLst():
    sampleUrl = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1'
    sampleF = dataFromUrl(sampleUrl, 10)
    #formatStr = re.findall(u"(.{18})000001(.{18}).*(.{18})平安银行(.{18})".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    formatStr = re.findall(u"((.{18})000001(.+?)平安银行(.{18}))".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    urlList=['http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1105&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1',  # fund
             'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1']  # stock
    prodDict = {}

    prodDict['FUND'] = []
    f = dataFromUrl(urlList[0], 10)
    #x=re.findall("(%s(\d{6})%s.*%s(.{2,}))%s" % (formatStr[0][0], formatStr[0][1], formatStr[0][2], formatStr[0][3]), f)
    prodDict['FUND'] += re.findall("%s(\d{6})%s(.{2,}?)%s" % (formatStr[0][1], formatStr[0][2], formatStr[0][3]), f.decode('GBK'))
    #x1=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center'", f)
    #x2=re.findall(r"<td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)
    #x3=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)

    prodDict['STOCK'] = []
    f = dataFromUrl(urlList[1], 10)
    #x=re.findall("(%s(\d{6})%s.*%s(.{2,}))%s" % (formatStr[0][0], formatStr[0][1], formatStr[0][2], formatStr[0][3]), f)
    prodDict['STOCK'] += re.findall("%s(\d{6})%s(.{2,}?)%s" % (formatStr[0][1], formatStr[0][2], formatStr[0][3]), f.decode('GBK'))
    #x1=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center'", f)
    #x2=re.findall(r"<td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)
    #x3=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)

    '''
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    '''
    return prodDict

def getAStockRealtime(stockLst):
    url = r'http://hq.sinajs.cn/list=%s' % stockLst
    formatStr = r'hq_str_s[hz](\d{6})="(.*)"'   #r'[(]{(.+?)}[)]'
    result = regDataFromUrl(url, 15, formatStr)
    res = []
    for prod in result:
        tmp = prod[1].split(',')
        tmp.append(prod[0])
        res.append( tmp )
    return res

def save2DiskDb():
    '''
    prodLst1 = Product.objects.using('default1').all()
    marketLst1 = Market.objects.using('default1').all()
    kDailyLst1 = KDaily.objects.using('default1').all()
    kMinLst1 = KMin.objects.using('default1').all()
    watchLst1 = WatchList.objects.using('default1').all()
    '''

    tblLst = []
    tblLst.append( Product.objects.all() )
    tblLst.append( Market.objects.all() )
    tblLst.append( KDaily.objects.all() )
    tblLst.append( KMin.objects.all() )
    tblLst.append( WatchList.objects.all() )

    Product.objects.using('default1').raw("delete * from myapp_product")
    Market.objects.using('default1').raw("delete * from myapp_market")
    KDaily.objects.using('default1').raw("delete * from myapp_kdaily")
    KMin.objects.using('default1').raw("delete * from myapp_kmin")
    WatchList.objects.using('default1').raw("delete * from myapp_watchlist")
    #for prod in prodLst1:
    for tbl in tblLst:
        for rec in tbl:
            rec.save(using='default1')  ## ??? !!! 

def copyDiskDb2Memo():
    '''
    prodLst1 = Product.objects.using('default1').all()
    marketLst1 = Market.objects.using('default1').all()
    kDailyLst1 = KDaily.objects.using('default1').all()
    kMinLst1 = KMin.objects.using('default1').all()
    watchLst1 = WatchList.objects.using('default1').all()
    '''
    tblLst = []
    tblLst.append( Product.objects.using('default1').all() )
    tblLst.append( Market.objects.using('default1').all() )
    tblLst.append( KDaily.objects.using('default1').all() )
    tblLst.append( KMin.objects.using('default1').all() )
    tblLst.append( WatchList.objects.using('default1').all() )
    
    #for prod in prodLst1:
    for tbl in tblLst:
        for rec in tbl:
            rec.save(using='default')  ## ??? !!! 

    p = Product.objects.all()
    m = Market.objects.all()
    k = KDaily.objects.all()
    kM = KMin.objects.all()
    w = WatchList.objects.all()

def useMemDb():
    f = open('myapp.sql')
    sql = f.read()
    #cur = django.db.connections['default1'].cursor()
    mem = django.db.connections['default1']
    django.db.connections['default1'] = django.db.connections['default']
    django.db.connections['default'] = mem
    cur = django.db.connection.cursor()
    cur.executescript(sql)
    copyDiskDb2Memo()

def qryRealtime(prodLst):
    batchQryProducts = ''
    numberPerQry = 850
    number = 0
    completeRslt = []
    for prod in prodLst:
        number += 1
        if number == 1 :
            batchQryProducts = prod.market.lower() + prod.code
        else :
            batchQryProducts += (',' + prod.market.lower() + prod.code)
            if number == numberPerQry :
                completeRslt += getAStockRealtime( batchQryProducts )
                number = 0
    else:
        if number <> 0:
                completeRslt += getAStockRealtime( batchQryProducts )
    newObjLst = []
    for fLst in completeRslt:
        #if fLst[-1]=='000033':  #var hq_str_sz000033="";
        #    a=1
        if len(fLst)<12:
            continue
        k1 = TradeRealTime( product=Product.objects.get( code=fLst[-1] ), o=fLst[1], p=fLst[2], c=fLst[3], h=fLst[4], l=fLst[5], amt=fLst[9], vol=fLst[8], 
                            buy0v=fLst[10], buy0=fLst[11], buy1v=fLst[12], buy1=fLst[13], buy2v=fLst[14], buy2=fLst[15], buy3v=fLst[16], buy3=fLst[17], buy4v=fLst[18], buy4=fLst[19], 
                            sell0v=fLst[20], sell0=fLst[21], sell1v=fLst[22], sell1=fLst[23], sell2v=fLst[24], sell2=fLst[25], sell3v=fLst[26], sell3=fLst[27], sell4v=fLst[28], sell4=fLst[29], 
                            date=fLst[30], tick=fLst[30]+' '+fLst[31] )  
        newObjLst.append(k1) 
        #k1.save()
    TradeRealTime.objects.bulk_create( newObjLst )
# var hq_str_sh600316="洪都航空,18.21,18.63,19.42,19.55,17.50,19.40,19.42,12458213,231498170,8194,19.40,600,19.39,100,19.38,800,19.37,14900,19.36,2400,19.42,90600,19.43,3600,19.44,26000,19.45,4700,19.46,2015-09-08,15:04:09,00";

def tickDataFromCsv(fn,code,market):
    import sqlite3
    con = sqlite3.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
    cur = con.cursor()
    #import contextlib
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    p = Product.objects.get(code=code, market=market)
    #objLst = []
    recLst = []
    for ln in rslt[1:]:
        fLst = ln.strip().split(',')
        recLst.append( [p.id] + fLst[2:] )
        #tickRec = TradeRealTime( product=p, tick=fLst[2], c=fLst[3], dealNum=fLst[4], tickAmt=fLst[5], tickVol=fLst[6], direction=fLst[7], 
        #                    buy0v=fLst[18], buy0=fLst[8], buy1v=fLst[19], buy1=fLst[9], buy2v=fLst[20], buy2=fLst[10], buy3v=fLst[21], buy3=fLst[11], buy4v=fLst[22], buy4=fLst[12], 
        #                    sell0v=fLst[23], sell0=fLst[13], sell1v=fLst[24], sell1=fLst[14], sell2v=fLst[25], sell2=fLst[15], sell3v=fLst[26], sell3=fLst[16], sell4v=fLst[27], sell4=fLst[17] )  
        #objLst.append(tickRec)
    #TradeRealTime.objects.bulk_create( objLst )
    return recLst
    cur.executemany( 'insert into myapp_TradeRealTime (product_id, tick, c, dealNum, tickAmt, tickVol, direction, buy0, buy1, buy2, buy3, buy4, sell0, sell1, sell2, sell3, sell4, buy0v, buy1v, buy2v, buy3v, buy4v, sell0v, sell1v, sell2v, sell3v, sell4v ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', recLst )
    con.commit()
    return

def getTickData():
    dateLst = ['20150901', '20150902', '20150907', '20150908', '20150909', '20150910', '20150911']
    for p in prodAll:
        if p.type <> 'STOCK':
            continue
        for d in dateLst:
            if p.market <> 'SH' and p.market <> 'SZ':
                continue
            fn = r'D:\data\%s\ProcessFile\Stk_Tick\%s\%s%s_%s.csv' % (d, d, p.market.lower(), p.code, d)
            tickDataFromCsv(fn, p.code, p.market)


def getDzhTickData():
    fn = r'D:\dzh365data\sz\TEMP\002594.L2D'
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.read('rb')
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''

def getHist(prodDictNoHist8Submarket):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d
    import sqlite3
    con = sqlite3.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
    cur = con.cursor()
    prodDictWithHist = {}
    for key in prodDictNoHist8Submarket:
        prodDictWithHist[key] = []
        market = key[:2]
        if key == u'SH':
            market=u'ss'
        for type in prodDictNoHist8Submarket[key]:
            if type=='FUND':
                continue
            for prod in prodDictNoHist8Submarket[key][type]:
                t = time.clock()
                url = "http://ichart.yahoo.com/table.csv?s=%s&a=01&b=01&c=1990&d=09&e=12&f=2015&g=d" % ( prod + '.' + market )
                print('start get url: %s, dataFromUrl start time: %s' % (url, datetime.now()) )
                f = dataFromUrl(url, 10)
                if f=='':
                    continue
                csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\HistCsv\%s.%s.csv' % (prod,key)
                with open(csvfn, 'w') as fp:
                    fp.write( f )
                print('dataFromUrl time: %.03f' % (time.clock()-t) )
                lines = f.split('\n')
                histRec = []
                prod_id = prodMapId[prod+'.'+key]
                for ln in lines[1:]:
                    fLst = ln.split(',')
                    if len(fLst)<7:
                        continue
                    histRec.append( [ prod_id ] + fLst )
                    #kd = KDaily( code=prod, market=market, o=fLst[1], c=fLst[4], h=fLst[2], l=fLst[3], vol=fLst[5], date=fLst[0], adjC = fLst[6])
                    #kd.save() 
                #t=time.clock()
                cur.executemany( "insert into myapp_KDaily(product_id, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?)", histRec )
                #cur.executemany( "insert into myapp_KDaily(code, market, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?,?)", histRec )
                con.commit()
                #print('executemany time: %.03f' % (time.clock()-t) )
                prodDictWithHist[key].append(prod)
                '''
                p = Product.objects.get( code=prod, market=key )
                p.bDataHist=True
                p.save()
                '''
    for key in prodDictWithHist:
        for prod in prodDictWithHist[key]:
            p = Product.objects.get( code=prod, market=key )
            p.bDataHist=True
            p.save()
    return

def csv2Db(path,con):
    for file in path:
        cur = con.cursor()
        #f = sys.read(file)
        con.commit()

def prepareTrading():
    marketLst = Product.objects.values_list('market',flat=True).distinct()
    submarketLst = Product.objects.values_list('submarket',flat=True).distinct()
    #marketLst = Market.objects.using('default').all()
    prodAll = Product.objects.using('default').all()
    prodDict = {}  #prodDict8Market = {}
    prodDict8Submarket = {}
    prodDict8Type = {}
    prodDictNoHist = {}
    prodDictNoHist8Submarket = {}
    prodMapId = {}
    prodIdMap = {}
    typeLst = Product.objects.values_list('type',flat=True).distinct()
    for submarket in submarketLst:
        prodDict8Submarket[ submarket ] = {}
        prodDictNoHist8Submarket[ submarket ] = []
    for market in marketLst:
        prodDict[ market ] = {}
        prodDictNoHist[ market ] = {}
        for type in typeLst:
            prodDict[ market ][type] = []
            prodDictNoHist[ market ][type] = []
    for prod in prodAll:
        prodIdMap[prod.id] = prod.code+'.'+prod.market
        prodMapId[prod.code+'.'+prod.market] = prod.id
        prodDict[ prod.market ][prod.type].append( prod.code )
        if not prod.bDataHist:
            prodDictNoHist[ prod.market ][prod.type].append( prod.code )
            prodDictNoHist8Submarket[ prod.submarket ].append( prod.code )
    #return submarketLst, prodAll, prodIdMap, prodMapId, prodDict, prodDict8Submarket, prodDictNoHist, prodDictNoHist8Submarket
    return submarketLst, prodAll, prodIdMap, prodMapId, prodDict, prodDict8Submarket,                  prodDictNoHist8Submarket


'''
def watch():
    for prod in SSEProdLst:
        getAStockRealtime()

# watchLst: prodCode market
# realTimeTrading: prodCode price


import threading 
def sayhello(): 
        print "hello world" 
        global t        #Notice: use global variable! 
        t = threading.Timer(5.0, sayhello) 
        t.start() 

def watchLst():
    prodLst = []
    #every10s
    for prod in prodLst:
        pass #getPrice（）
    
t = threading.Timer(5.0, sayhello) 
t.start() 



class SinaWeb:
    _itemLst=['name','dayOpen','preClose','latestPrice','dayHigh','dayLow','buy1','sell1','vol','amount',
          'buy1vol','buy1p','buy2vol','buy2p','buy3vol','buy3p','buy4vol','buy4p','buy5vol','buy5p','sell1vol','sell1p','sell2vol','sell2p','sell3vol','sell3p','sell4vol','sell4p','sell5vol','sell5p',
          'date','time']
    url = 'http://hq.sinajs.cn/list='  # ="南方香港,0.966,0.966,0.965,0.969,0.962,0.965,0.967,6616300,6396340.302,14300,0.965,57500,0.964,1300,0.963,52400,0.962,50000,0.961,74800,0.967,140598,0.968,104800,0.969,80100,0.970,108000,0.971,2015-08-06,15:05:25,00";
    formatStr = ''
    def getCurrent(self, stockLst):
        formatStr = r'="(.*)";'
        result = _request(url, stockLst, formatStr, _itemLst)
        for prod in result:
            prod.split(',')
        # send query request: url + stockLst + itemLst
        # analyse returned result
        # save to DB 
        return
    def getHist(self, stockLst, itemLst):
        # send query request: url + stockLst + itemLst
        # analyse returned result
        # save to DB 
        return

class _market:
    productLst = []
    def getProductLst(self):
        pass

class marketSH(_market, WebData):
  pass
'''

def getDzhCodeLst(fn, market):
    try:
        with open( fn ) as fp:  
            lines = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    recLst = []
    for ln in lines[2:]:
        fLst = ln.strip().split('\t')
        #recLst.append( [p.id] + fLst[2:] )
        p=Product_(source='dzh', code=fLst[0], type='', market=market, bDataHist=False, name=fLst[1].decode('GBK'), submarket = Submarket(market, fLst[0]) )
        recLst.append(p)
    Product_.objects.bulk_create( recLst )

#dataPath
fnLst = ['D:\data\SH.SNT', 'D:\data\SZ.SNT']
t = time.clock()
#getDzhCodeLst('D:\data\codeBook\SZ.SNT', 'SZ')
#getDzhCodeLst('D:\data\codeBook\SH.SNT', 'SH')
#getDzhCodeLst('D:\data\codeBook\HK.SNT', 'HK')
#getDzhCodeLst(u'D:\data\codeBook\HI恒生指数.SNT', 'HK')
print('getDzhCodeLst time: %.03f' % (time.clock()-t) )

#for p in Product_.objects.all():
#    if p.submarket not in ['', 'SHF', '']
#    p1 = Product

#getHKProdLst()

'''
l1 = getSSEProdLst()
for item in l1:
    p1=Product(code=item[0], type='STOCK', market='SH', bDataHist=False, name=item[1], submarket = Submarket('SH', item[0]) )
    #p1=Product(code=item[0], type='stock', market=Market.objects.get(name='SH'), bDataHist=False, name=item[1] )
    p1.save()

prodLst = Product.objects.all()

#from django.db import transaction
#transaction.set_autocommit(autocommit=False)
l2 = getSZSEProdLst()
#transaction.Atomic()
for key in l2:
    for item in l2[key]:
        p2=Product(code=item[0],name=item[1],type=key, market='SZ', bDataHist=False, submarket = Submarket('SZ', item[0]))
        #p2=Product(code=item[0],name=item[1],type=key, market=Market.objects.get(name='SZ'), bDataHist=False)
        p2.save()
#transaction.commit()
'''

submarketLst, prodAll, prodIdMap, prodMapId, prodDict, prodDict8Submarket, prodDictNoHist8Submarket = prepareTrading()

'''
from django.db import transaction
transaction.set_autocommit(autocommit=False)
#transaction.Atomic()
i=0
for item in prodLst:
    p2=Product(code=item.code,market=item.market)
    p2.save()
    i+=1
    if i>3:
        break
transaction.commit()
'''

#'''
t = time.clock()
getHist(prodDictNoHist8Submarket)
print('getHist time: %.03f' % (time.clock()-t) )

for prod in prodAll:
    prod.save(using='default')  ## ??? !!! 

t = time.clock()
useMemDb()
print('usememdb time: %.03f' % (time.clock()-t) )
#'''

def getTickData_():
    import sqlite3
    con = sqlite3.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
    cur = con.cursor()
    import scandir

    dateLst = ['20150901', '20150902', '20150907', '20150908', '20150909', '20150910', '20150911']
    fileDict = {}
    for d in dateLst:
        #for dir in 
        dir = 'D:\\data\\%s\\ProcessFile\\Stk_Tick\\%s\\' % (d, d)
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                market=fn[0:2]
                code=fn[2:8]
                prod=fn[0:8]
                if prod not in fileDict.keys():
                    fileDict[prod]=[]
                fileDict[prod].append(dir+fn)
    recDict = {}
    for p in fileDict.keys():
        #recLst=[]
        recDict[p] = []
        for f in fileDict[p]:
            recDict[p] += tickDataFromCsv(f,p[2:],p[0:2].upper())
        #cur.executemany( 'insert into myapp_TradeRealTime (product_id, tick, c, dealNum, tickAmt, tickVol, direction, buy0, buy1, buy2, buy3, buy4, sell0, sell1, sell2, sell3, sell4, buy0v, buy1v, buy2v, buy3v, buy4v, sell0v, sell1v, sell2v, sell3v, sell4v ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', recDict[p] )
        #con.commit()
    return redDict

t = time.clock()
x=getTickData_()
print('getTickData_ time: %.03f' % (time.clock()-t) )

t = time.clock()
getTickData()
print('getTickData time: %.03f' % (time.clock()-t) )

t = time.clock()
qryRealtime(prodAll)
print('qryRealtim time: %.03f' % (time.clock()-t) )

t = time.clock()
save2DiskDb()
print('save2DiskDb time: %.03f' % (time.clock()-t) )

KLst = KDaily.objects.all()
KLst_ = KDaily.objects.using('default1').all()


getAStockRealtime('sz002594,sh510900,sz160125')



# update myapp_product set errInfo = '1' where code in (select a.code from myapp_product_ a, myapp_product b where a.code = b.code and a.market = b.market) 
# update myapp_product_ set errInfo = '1' where code in (select code from myapp_product where myapp_product.code = myapp_product_.code and myapp_product.market = myapp_product_.market) 
# insert into myapp_product select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where a.errInfo = '' and submarket like 'S%I'
# insert into myapp_product(code, market, submarket, name, type, bDataHist, errInfo) select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where errInfo = '' and submarket like 'S%I'
