# coding=utf-8

#import sqlite3
#conn = sqlite3.connect(r'D:\GitHub\myapp\net\website\django\mysite1\db.sqlite3')
#from selenium import webdriver

import time
from net.url.dataSource import regDataFromUrl, dataFromUrl
import re
import codecs
import django
import sys
sys.path.append(r'E:\GitHub\myapp\net\website\django\mysite1')
django.setup()

from myapp.models import Product, KDaily, KMin, WatchList, Market

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
    
    result = regDataFromUrl(url, formatStr)
    prodLst = []
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    return prodLst

def getSSEProdLst():
    url = r'http://www.sse.com.cn/js/common/ssesuggestdata.js'  # ({val:"600000",val2:"浦发银行",val3:"pfyx"})
    formatStr = r'[(]{(.+?)}[)]'
    result = regDataFromUrl(url, formatStr)
    prodLst = []
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    return prodLst

def getSZSEProdLst():
    sampleUrl = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1'
    sampleF = dataFromUrl(sampleUrl)
    #formatStr = re.findall(u"(.{18})000001(.{18}).*(.{18})平安银行(.{18})".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    formatStr = re.findall(u"((.{18})000001(.+?)平安银行(.{18}))".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    urlList=['http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1105&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1',
             'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1']
    prodLst = []
    for url in urlList:
        f = dataFromUrl(url)
        #x=re.findall("(%s(\d{6})%s.*%s(.{2,}))%s" % (formatStr[0][0], formatStr[0][1], formatStr[0][2], formatStr[0][3]), f)
        prodLst += re.findall("%s(\d{6})%s(.{2,}?)%s" % (formatStr[0][1], formatStr[0][2], formatStr[0][3]), f.decode('GBK'))
        #x1=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center'", f)
        #x2=re.findall(r"<td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)
        #x3=re.findall(r" align='center' >(\d{6})</td><td  class='cls-data-td'  align='center' >(.{2,}?)</td><td  class='cls-data-td'  ali", f)
    '''
    for prod in result:
        prodLst.append( re.findall( r':"(.+?)"', prod ) )
    '''
    return prodLst

def getAStockRealtime(stockLst):
    url = r'http://hq.sinajs.cn/list=%s' % stockLst
    formatStr = r'hq_str_s[hz](\d{6})="(.*)"'   #r'[(]{(.+?)}[)]'
    result = regDataFromUrl(url, formatStr)
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

def qryRealtim(prodLst):
    batchQryProducts = ''
    numberPerQry = 850
    number = 0
    completeRslt = []
    for prod in prodLst:
        number += 1
        if number == 1 :
            batchQryProducts = prod.market + prod.code
        else :
            batchQryProducts += (',' + prod.market + prod.code)
            if number == numberPerQry :
                completeRslt += getAStockRealtime( batchQryProducts )
                number = 0
    else:
        if number <> 0:
                completeRslt += getAStockRealtime( batchQryProducts )
    
    for item in completeRslt:
        #if item[-1]=='000033':  #var hq_str_sz000033="";
        #    a=1
        if len(item)<12:
            continue
        k1 = KDaily( code=item[-1], market='', o=item[1], p=item[2], c=item[3], h=item[4], l=item[5], amt=item[9], vol=item[8], date=item[-4]) 
        k1.save()

def getHist(proDict):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d
    import sqlite3
    con = sqlite3.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
    cur = con.cursor()
    for key in prodDict:
        market = key
        if key == u'SH':
            market=u'ss'
        i=0
        for prod in prodDict[key]:
            t = time.clock()
            url = "http://ichart.yahoo.com/table.csv?s=%s&a=01&b=01&c=1990&d=08&e=31&f=2015&g=d" % ( prod + '.' + market )
            f = dataFromUrl(url).strip()
            print('dataFromUrl time: %.03f' % (time.clock()-t) )
            lines = f.split('\n')
            histRec = []
            for ln in lines[1:]:
                item = ln.split(',')
                if len(item)<7:
                    continue
                histRec.append( [ prod, key ] + item )
                #kd = KDaily( code=prod, market=market, o=item[1], c=item[4], h=item[2], l=item[3], vol=item[5], date=item[0], adjC = item[6])
                #kd.save() 
            #t=time.clock()
            cur.executemany( "insert into myapp_KDaily(code, market, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?,?)", histRec )
            con.commit()
            #print('executemany time: %.03f' % (time.clock()-t) )
    return

def prepareTrading():
    global marketLst
    marketLst = Market.objects.using('default').all()
    global prodLst 
    prodLst = Product.objects.using('default').all()
    global prodDict 
    prodDict = {}
    for market in marketLst:
        prodDict[ market.name ] = []
    for prod in prodLst:
        prodDict[ prod.market.upper() ].append( prod.code )


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

#getHKProdLst()

marketLst = []
prodLst = []
prodDict = {}

prepareTrading()

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

t = time.clock()
getHist(prodLst)
print('getHist time: %.03f' % (time.clock()-t) )

for prod in prodLst:
    prod.save(using='default')  ## ??? !!! 

t = time.clock()
useMemDb()
print('usememdb time: %.03f' % (time.clock()-t) )

'''
l1 = getSSEProdLst()
for item in l1:
    p1=Product(code=item[0],companyName=item[1],market='SH')
    p1.save()

prodLst = Product.objects.all()

#from django.db import transaction
#transaction.set_autocommit(autocommit=False)
l2 = getSZSEProdLst()
#transaction.Atomic()
for item in l2:
    p2=Product(code=item[0],companyName=item[1],market='SZ')
    p2.save()
#transaction.commit()
'''

t = time.clock()
qryRealtim(prodLst)
print('qryRealtim time: %.03f' % (time.clock()-t) )

t = time.clock()
save2DiskDb()
print('save2DiskDb time: %.03f' % (time.clock()-t) )

KLst = KDaily.objects.all()
KLst_ = KDaily.objects.using('default1').all()


getAStockRealtime('sz002594,sh510900,sz160125')

