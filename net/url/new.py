# coding=utf-8

import pandas as pd

#import sqlite3 as db
#import mysql as db  #connector.paramstyle　
import MySQLdb as db
#conn = db.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
conn = db.connect( host='localhost', user='root', passwd='', db='myapp', charset='utf8' )

#from selenium import webdriver

prjPath = r'E:\GitHub\myapp\net\website\django\mysite1'
dataPath = r'D:\data'

import time
from datetime import datetime, timedelta
from net.url.dataSource import regDataFromUrl, dataFromUrl
import re
import codecs
import django
import sys
import os
#from net.website.django.mysite1.myapp.rules import Submarket
sys.path.append( prjPath )
django.setup()
from myapp.rules import Submarket, MapSubmarket2Table # net.website.django.mysite1.

from myapp.models import * #Product_, Product, KDaily, KMin, WatchList, Market, StockInfo, TradeRealTime


def execScript4Mysql(conn, script):
    sqlLst = script.split(';')
    cur = conn.cursor()
    for sql in sqlLst:
        if sql.strip()=='':
            continue
        cur.execute(sql)
    conn.commit()

def export2Txt(conn):
    fn = 'd:\product.txt'
    fp = open(fn, 'w')
    cur = conn.cursor()
    pAll = Product.object.all()
    for p in pAll:
        fp.write( p.code +  p.market )

def getHKProdLst_ifeng():
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
    sampleF = dataFromUrl(sampleUrl, 10)    #formatStr = re.findall(u"(.{18})000001(.{18}).*(.{18})平安银行(.{18})".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    formatStr = re.findall(u"((.{18})000001(.+?)平安银行(.{18}))".encode('GBK'), sampleF[:9999]) #codecs.decode(sampleF, 'GBK'))
    urlList=['http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1105&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1',  # fund
             'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1']  # stock
    prodDict = {}

    prodDict['FUND'] = []
    f = dataFromUrl(urlList[0], 10)
    # x=re.findall("(%s(\d{6})%s.*%s(.{2,}))%s" % (formatStr[0][0], formatStr[0][1], formatStr[0][2], formatStr[0][3]), f)
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
    return prodDict

def getAStockRealtime(stockLst):
    url = r'http://hq.sinajs.cn/list=%s' % stockLst
    formatStr = r'hq_str_(s[hz])(\d{6})="(.*)"'   #r'[(]{(.+?)}[)]'
    result = regDataFromUrl(url, 15, formatStr)
    res = []
    for prod in result:
        tmp = prod[2].split(',')
        tmp.append( prod[1] )
        tmp.append( prod[0].upper() )
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

def qryRealtime():
    batchQryProducts = ''
    numberPerQry = 850
    number = 0
    completeRslt = []
    for id in prodIdMap.keys():
        prod = prodIdMap[id]
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
        k1 = TradeRealTime( product=Product.objects.get( code=fLst[-2], market=fLst[-1] ), o=fLst[1], p=fLst[2], c=fLst[3], h=fLst[4], l=fLst[5], amt=fLst[9], vol=fLst[8], 
                            buy0v=fLst[10], buy0=fLst[11], buy1v=fLst[12], buy1=fLst[13], buy2v=fLst[14], buy2=fLst[15], buy3v=fLst[16], buy3=fLst[17], buy4v=fLst[18], buy4=fLst[19], 
                            sell0v=fLst[20], sell0=fLst[21], sell1v=fLst[22], sell1=fLst[23], sell2v=fLst[24], sell2=fLst[25], sell3v=fLst[26], sell3=fLst[27], sell4v=fLst[28], sell4=fLst[29], 
                            date=fLst[30], tick=fLst[30]+' '+fLst[31] )  
        newObjLst.append(k1) 
        #k1.save()
    TradeRealTime.objects.bulk_create( newObjLst )
# var hq_str_sh600316="洪都航空,18.21,18.63,19.42,19.55,17.50,19.40,19.42,12458213,231498170,8194,19.40,600,19.39,100,19.38,800,19.37,14900,19.36,2400,19.42,90600,19.43,3600,19.44,26000,19.45,4700,19.46,2015-09-08,15:04:09,00";

def tickDataFromCsv(fn, pid):
    #import contextlib
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    #objLst = []
    recLst = []
    for ln in rslt[1:]:
        fLst = ln.strip().split(',')
        recLst.append( [pid] + fLst[2:] + [ fLst[2][:10] ] )   # date: fLst[2][:10]
        #tickRec = TradeRealTime( product=p, tick=fLst[2], c=fLst[3], dealNum=fLst[4], tickAmt=fLst[5], tickVol=fLst[6], direction=fLst[7], 
        #                    buy0v=fLst[18], buy0=fLst[8], buy1v=fLst[19], buy1=fLst[9], buy2v=fLst[20], buy2=fLst[10], buy3v=fLst[21], buy3=fLst[11], buy4v=fLst[22], buy4=fLst[12], 
        #                    sell0v=fLst[23], sell0=fLst[13], sell1v=fLst[24], sell1=fLst[14], sell2v=fLst[25], sell2=fLst[15], sell3v=fLst[26], sell3=fLst[16], sell4v=fLst[27], sell4=fLst[17] )  
        #objLst.append(tickRec)
    #TradeRealTime.objects.bulk_create( objLst )
    return recLst

def tickDataFromCsv_(fn,code,market, conn):
    cur = conn.cursor()
    #import contextlib
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    pid = prodMapId[ code + '.' + market ].id
    #objLst = []
    recLst = []
    for ln in rslt[1:]:
        fLst = ln.strip().split(',')
        recLst.append( [pid] + fLst[2:] )
        #tickRec = TradeRealTime( product=pid, tick=fLst[2], c=fLst[3], dealNum=fLst[4], tickAmt=fLst[5], tickVol=fLst[6], direction=fLst[7], 
        #                    buy0v=fLst[18], buy0=fLst[8], buy1v=fLst[19], buy1=fLst[9], buy2v=fLst[20], buy2=fLst[10], buy3v=fLst[21], buy3=fLst[11], buy4v=fLst[22], buy4=fLst[12], 
        #                    sell0v=fLst[23], sell0=fLst[13], sell1v=fLst[24], sell1=fLst[14], sell2v=fLst[25], sell2=fLst[15], sell3v=fLst[26], sell3=fLst[16], sell4v=fLst[27], sell4=fLst[17] )  
        #objLst.append(tickRec)
    #TradeRealTime.objects.bulk_create( objLst )
    return recLst
    cur.executemany( 'insert into myapp_TradeRealTime (product_id, tick, c, dealNum, tickAmt, tickVol, direction, buy0, buy1, buy2, buy3, buy4, sell0, sell1, sell2, sell3, sell4, buy0v, buy1v, buy2v, buy3v, buy4v, sell0v, sell1v, sell2v, sell3v, sell4v ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', recLst )
    conn.commit()
    return

def getTickData(conn):
    cur = conn.cursor()
    dateLst = ['20150901', '20150902', '20150907', '20150908', '20150909', '20150910', '20150911', '20150914', '20150915', '20150916', '20150917', '20150918', '20150921', '20150922', '20150923', '20150924', '20150925', '20150928', '20150929', '20150930']
    for id in prodIdMap.keys():
        p = prodIdMap[id]
        if p.submarket == None or p.submarket.strip == '':
            continue
        if p.submarket[2] <> 'S':
            continue
        for d in dateLst:
            if p.market <> 'SH' and p.market <> 'SZ':
                continue
            fn = r'D:\data\tick\%s\ProcessFile\Stk_Tick\%s\%s%s_%s.csv' % (d, d, p.market.lower(), p.code, d)
            if not os.path.isfile(fn):
                continue
            recLst = tickDataFromCsv(fn, id)
            cur.executemany( 'insert into myapp_TradeRealTime (product_id, dt, c, dealNum, tickAmt, tickVol, direction, buy0, buy1, buy2, buy3, buy4, sell0, sell1, sell2, sell3, sell4, buy0v, buy1v, buy2v, buy3v, buy4v, sell0v, sell1v, sell2v, sell3v, sell4v, date ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', recLst )
            conn.commit()

def getTickData_(conn):
    cur = conn.cursor()
    import scandir

    dateLst = ['20150901', '20150902', '20150907', '20150908', '20150909', '20150910', '20150911']
    fileDict = {}
    for d in dateLst:
        #for dir in 
        dir = 'D:\\data\\tick\\%s\\ProcessFile\\Stk_Tick\\%s\\' % (d, d)
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
            recDict[p] += tickDataFromCsv_(f,p[2:],p[0:2].upper())
        #cur.executemany( 'insert into myapp_TradeRealTime (product_id, tick, c, dealNum, tickAmt, tickVol, direction, buy0, buy1, buy2, buy3, buy4, sell0, sell1, sell2, sell3, sell4, buy0v, buy1v, buy2v, buy3v, buy4v, sell0v, sell1v, sell2v, sell3v, sell4v ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ', recDict[p] )
        #conn.commit()
    return recDict


def getDzhTickData():
    fn = r'D:\dzh365data\sz\TEMP\002594.L2D'
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.read('rb')
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''

def workYesterday( d=datetime.now() ):
    weekday = d.strftime('%w') # if today is Sunday or Monday
    sunday=6  # sqlite3: 0
    monday=0  # sqlite3: 1
    if weekday == sunday:
        return (datetime.now()- timedelta(2)).strftime('%Y-%m-%d')  # Friday for Sunday
    elif weekday == monday:
        return (datetime.now()- timedelta(3)).strftime('%Y-%m-%d')  # Friday for Monday
    else:
        return (datetime.now()- timedelta(1)).strftime('%Y-%m-%d')

def getHist(prodDict8Submarket, conn, timeout):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d 
    global newBeforeHistBegin, newAfterHistEnd

    cur = conn.cursor()
    qryEndDate = "&d=%02d&e=%02d&f=%d" % ( datetime.now().month-1, datetime.now().day, datetime.now().year )
    qryDate = "a=0&b=1&c=1989%s&g=d" % (qryEndDate)
    workYesterdayStr = workYesterday()
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        market = key[:2]
        #if market == u'SZ':
        #    pass
        if key[2]<>'S' and key[2]<>'I':
            continue
        tblName = 'myapp_kdaily_' + MapSubmarket2Table( key )
        for prod in prodDict8Submarket[key]:
            if 'yahoo' in prod.maskSite.split('.'):
                continue

            if prod.dateHistEnd == None:
                dateHistEnd = '1900-01-01'
            else:
                dateHistEnd = prod.dateHistEnd.strftime('%Y-%m-%d')
            if dateHistEnd >= workYesterdayStr:
                continue

            #qryDate = "a=0&b=1&c=1989%s&g=d" % (qryEndDate)
            '''
            if prod.dateHistEnd == None:
                qryDate = "a=0&b=01&c=1989%s&g=d" % (qryEndDate)
            elif dateHistEnd >= workYesterdayStr:
                continue
            else:
                qryDate = "a=%s&b=%s&c=%s%s&g=d" % ( int(dateHistEnd[5:7])-1, dateHistEnd[-2:], dateHistEnd[:4], qryEndDate )
            '''

            csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\HistCsv\%s.%s.csv' % (market,prod.code)
            t = time.clock()
            if market=='HK' and prod.code[0]=='0':
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code[1:] + '.' + market, qryDate )
            elif market == 'SH':
                #market=u'ss'
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + 'ss', qryDate )
            else:
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + market, qryDate )
            print('start get url: %s, dataFromUrl start time: %s\r\n' % (url, datetime.now()) )
            f = dataFromUrl(url, waittime=timeout)
            if f=='url not found':
                prod.maskSite += 'yahoo.'
                prod.save()
                continue 
            elif f=='':
                continue
            with open(csvfn, 'w') as fp:
                fp.write( f )
            print('dataFromUrl time: %.03f\r\n' % (time.clock()-t) )
            lines = f.split('\n')
            histRec = []
            if prod==None:
                continue
            for ln in lines[1:]:
                fLst = ln.split(',')
                if len(fLst)<7:
                    continue
                #if prod.dateHistEnd==None
                #if fLst[0] <= prod.dateHistEnd.strftime('%Y-%m-%d'):
                #    if fLst[0] >= prod.dateHistBegin.strftime('%Y-%m-%d'):
                #        continue;
                if fLst[0]<=dateHistEnd:
                    break 
                histRec.append( [ prod.id ] + fLst )
                #kd = KDaily( code=prod, market=market, o=fLst[1], c=fLst[4], h=fLst[2], l=fLst[3], vol=fLst[5], date=fLst[0], adjC = fLst[6])
                #kd.save() 
            #t=time.clock()
            if histRec == []:
                continue
            else:
                newAfterHistEnd = True
                if prod.dateHistEnd == None:
                    newBeforeHistBegin = True
            try:
                #cur.executemany( "insert into %s(product_id, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?)" % tblName, histRec )
                cur.executemany(    "insert into %s(product_id, date, o, h, l, c, vol, adjC)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s)", histRec )
                #cur.executemany( "insert into myapp_KDaily(code, market, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?,?)", histRec )
            except db.Error,e:
                sys.stdout.write(  'except while executemany insert:' + prod.code+'.'+market + ' Error: ' + str(e) + '\r\n' )
            conn.commit()
            #print('executemany time: %.03f' % (time.clock()-t) )
    return

def getHist2Csv(prodDict8Submarket, timeout):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d 
    qryEndDate = "&d=%02d&e=%02d&f=%d" % ( datetime.now().month-1, datetime.now().day, datetime.now().year )
    qryDate = "a=0&b=1&c=1989%s&g=d" % (qryEndDate)
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        market = key[:2]
        if key[2]<>'S' and key[2]<>'I':
            continue

        for prod in prodDict8Submarket[key]:
            if 'yahoo' in prod.maskSite.split('.'):
                continue
            csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\HistCsv\%s.%s.csv' % (market,prod.code)
            if os.path.isfile(csvfn):
                continue

            if market=='HK' and prod.code[0]=='0':
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code[1:] + '.' + market, qryDate )
            elif market == 'SH':
                #market=u'ss'
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + 'ss', qryDate )
            else:
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + market, qryDate )
            print('start get url: %s, dataFromUrl start time: %s\r\n' % (url, datetime.now()) )
            f = dataFromUrl(url, waittime=timeout)
            if f=='url not found':
                prod.maskSite += 'yahoo.'
                prod.save()
                continue 
            elif f=='':
                continue
            with open(csvfn, 'w') as fp:
                fp.write( f )
            print('dataFromUrl time: %.03f\r\n' % (time.clock()-t) )
    return

def getHistFromCsv(prodDict8Submarket, conn):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d 
    global newBeforeHistBegin, newAfterHistEnd

    cur = conn.cursor()
    workYesterdayStr = workYesterday()
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        market = key[:2]
        if key[2]<>'S' and key[2]<>'I':
            continue
        tblName = 'myapp_kdaily_' + MapSubmarket2Table( key )
        for prod in prodDict8Submarket[key]:
            if prod.dateHistEnd == None:
                dateHistEnd = '1900-01-01'
            else:
                dateHistEnd = prod.dateHistEnd.strftime('%Y-%m-%d')
            if dateHistEnd >= workYesterdayStr:
                continue

            csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\HistCsv\%s.%s.csv' % (market,prod.code)
            if os.path.isfile(csvfn):
                with open(csvfn) as fp:
                    f = fp.read() 
            else:
                continue
            lines = f.split('\n')
            histRec = []
            for ln in lines[1:]:
                fLst = ln.split(',')
                if len(fLst)<7:
                    continue
                if fLst[0]<=dateHistEnd:
                    break 
                #fLst[0] = datetime.strptime(fLst[0], '%Y-%m-%d')
                #for i in range(len(fLst[1:])):
                #    fLst[i+1] = float(fLst[i+1]) 
                histRec.append( [ int(prod.id) ] + fLst )
            if histRec == []:
                continue
            else:
                newAfterHistEnd = True
                if prod.dateHistEnd == None:
                    newBeforeHistBegin = True
            try:
                #sql = "insert into %s(product_id, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?)" % tblName
                #sql = "insert into myapp_kdaily_cns(product_id, date, o, h, l, c, vol, adjC) values (%s,%s,%s,%s,%s,%s,%s,%s)"  # % tblName
                cur.executemany(    "insert into %s(product_id, date, o, h, l, c, vol, adjC)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s)", histRec )
                #cur.executemany( "insert into myapp_KDaily(code, market, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?,?)", histRec )
            except db.Error,e:
                sys.stdout.write(  'except while executemany insert:' + prod.code+'.'+market + ' Error: ' + str(e) + '\r\n' )
            conn.commit()
    return


from django.core.exceptions import ObjectDoesNotExist
def getQianLongDailyRpt(fn, conn): #, market):
    cur = conn.cursor()
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''

    histRec = []
    tblName = 'myapp_kdaily_cns'
    dateStr = os.path.split(fn)[1]
    dateStr = dateStr.split('.')[0]
    dateStr = dateStr[:4] + '-' +dateStr[4:6] + '-' +dateStr[6:]
    for ln in rslt[1:]:
        if ln.strip()=='':
            continue
        fld = ln.split('\t')   #  DZH: 1code 4c 6v 10p 11o 12h 13l                      # QL:: 2code 4c 6o 7v 9h 10l  
        if fld[4].strip(' -')=='': #.isdigit() and fld[9].strip().isdigit() and fld[4].strip().isdigit() and fld[10].strip().isdigit() ):
            continue 
        if fld[1][1]=='6':
            market='SH'
        else:
            market='SZ'
        code = fld[1].strip(" '")
        p = prodMapId[ code + '.' + market ]    # p = Product.objects.get(id=prod_id)        #except ObjectDoesNotExist:
        if code=='600000':
            pass
        #if code in prodDict8Submarket[ Submarket( market, code) ]:
        #    continue
        if p.dateHistBegin==None or ( dateStr > p.dateHistEnd.strftime('%Y-%m-%d') or dateStr < p.dateHistBegin.strftime('%Y-%m-%d') ):
            histRec.append( [ p.id ] + [dateStr, fld[11], fld[12], fld[13], fld[4], fld[6], fld[4]] )   # set adjc = c 
        else:
            continue 
    try:
        cur.executemany( "insert into %s(product_id, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?)" % tblName, histRec )
        #cur.executemany( "insert into myapp_KDaily(code, market, date, o, h, l, c, vol, adjC) values (?,?,?,?,?,?,?,?,?)", histRec )
    except db.Error,e:
        sys.stdout.write(  'except while executemany insert:' + ' Error: ' + str(e) + '\r\n' )
    conn.commit()

# select * from myapp_kdaily_cns where strftime('%Y.%m.%d', [date])='1899.12.30'  

def priceAdjust(conn):
    cur = conn.cursor()
    # backward adjust price = real-price / rationFrwd
    cur.execute( "update myapp_kdaily_cns set ratioFrwd=c/adjC" ) # where errInfo isnull;" ) # , c=adjC;  # some adjC isnull lead to fail of update" )
    cur.execute( "update myapp_kdaily_hks set ratioFrwd=c/adjC" ) # where errInfo isnull;" ) # , c=adjC;  # some adjC isnull lead to fail of update" )
    cur.execute( "update myapp_product set ratioFrwdBegin = (select ratioFrwd from myapp_kdaily_cns where myapp_kdaily_cns.product_id = myapp_product.id and myapp_kdaily_cns.date = myapp_product.dateHistBegin ) where market='SZ'" )
    cur.execute( "update myapp_product set ratioFrwdBegin = (select ratioFrwd from myapp_kdaily_cns where myapp_kdaily_cns.product_id = myapp_product.id and myapp_kdaily_cns.date = myapp_product.dateHistBegin ) where market='SH'" )
    cur.execute( "update myapp_product set ratioFrwdBegin = (select ratioFrwd from myapp_kdaily_hks where myapp_kdaily_hks.product_id = myapp_product.id and myapp_kdaily_hks.date = myapp_product.dateHistBegin ) where market='HK'" )
    conn.commit()

    submarketLst, prodIdMap, prodMapId, prodDict8Submarket = prepareTrading()
    # price of history data from yahoo is forward adjust price
    # backward adjust price = real-price * ratioBack,  ratioBack = 1st rationFrwd / rationFrwd
    for key in prodDict8Submarket:
        tblName = MapSubmarket2Table( key ).lower()
        if tblName <> 'cns' and tblName <> 'hks':
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


def postImportData(conn):
    cur = conn.cursor()
    
    # move/append new data to internal no-update table, ratioFrwd may change ??

    # mark time boundary of data imported
    if newAfterHistEnd:
        cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_cns where myapp_product.id = myapp_kdaily_cns.product_id group by product_id) where market='SZ'" )
        cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_cns where myapp_product.id = myapp_kdaily_cns.product_id group by product_id) where market='SH'" )
        cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_hks where myapp_product.id = myapp_kdaily_hks.product_id group by product_id) where market='HK'" )
        #cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_hki where myapp_product.id = myapp_kdaily_hki.product_id group by product_id) where submarket='HKI'" )
        cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_cni where myapp_product.id = myapp_kdaily_cni.product_id group by product_id) where submarket='SZI'" )
        cur.execute( "update myapp_product set dateHistBegin = (select min(date) from myapp_kdaily_cni where myapp_product.id = myapp_kdaily_cni.product_id group by product_id) where submarket='SHI'" )

    if newBeforeHistBegin:
        cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_cns where myapp_product.id = myapp_kdaily_cns.product_id group by product_id) where market='SZ'" )
        cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_cns where myapp_product.id = myapp_kdaily_cns.product_id group by product_id) where market='SH'" )
        cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_hks where myapp_product.id = myapp_kdaily_hks.product_id group by product_id) where market='HK'" )
        #cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_hki where myapp_product.id = myapp_kdaily_hki.product_id group by product_id) where submarket='HKI'" )
        cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_cni where myapp_product.id = myapp_kdaily_cni.product_id group by product_id) where submarket='SZI'" )
        cur.execute( "update myapp_product set dateHistEnd =   (select max(date) from myapp_kdaily_cni where myapp_product.id = myapp_kdaily_cni.product_id group by product_id) where submarket='SHI'" )

    #cur.execute( "update myapp_product set dateHistEnd = '' where dateHistEnd isnull" )

    # mark time boundary of data imported


    conn.commit()



def csv2Db(path,conn):
    for file in path:
        cur = conn.cursor()
        #f = sys.read(file)
        conn.commit()

def prepareTrading():
    #marketLst = Product.objects.values_list('market',flat=True).distinct()
    #typeLst = Product.objects.values_list('type',flat=True).distinct()
    #marketLst = Market.objects.using('default').all()
    submarketLst = Product.objects.values_list('submarket',flat=True).distinct()
    prodAll = Product.objects.using('default').all()   # all product record
    #prodDict = {}                       # {market: {type: [code, ]} }           #prodDict8Market = {}        
    prodDict8Submarket = {}
    # prodDictNoHist8Submarket = {}
    # prodDictWithHist8Submarket = {}
    prodMapId = {}                       # {code+market: product_id}
    prodIdMap = {}                       # {product_id: code+market}
    for submarket in submarketLst:
        prodDict8Submarket[ submarket ] = []
        # prodDictNoHist8Submarket[ submarket ] = []
        # prodDictWithHist8Submarket[ submarket ] = []
    for prod in prodAll:
        if prod.submarket == '' or prod.submarket == None:
            continue 
        if prod.submarket[2] <> 'S' and prod.submarket[2] <> 'I':
            continue 
        prodIdMap[prod.id] = prod # {'code':prod.code, 'market':prod.market, 'bHist':prod.bDataHist, 'dateHistBegin':prod.dateHistBegin, 'dateHistEnd':prod.dateHistEnd, 'type':prod.type, 'submarket': prod.submarket}
        prodMapId[prod.code+'.'+prod.market] = prod #{'id':prod.id, 'bHist':prod.bDataHist, 'dateHistBegin':prod.dateHistBegin, 'dateHistEnd':prod.dateHistEnd, 'type':prod.type, 'submarket': prod.submarket }
        prodDict8Submarket[ prod.submarket ].append( prod ) #{'id':prod.id, 'code':prod.code, 'market':prod.market, 'bHist':prod.bDataHist, 'dateHistBegin':prod.dateHistBegin, 'dateHistEnd':prod.dateHistEnd, 'type':prod.type, 'submarket': prod.submarket} )
        '''
        #prodDict[ prod.market ][prod.type].append( prod.code )
        if not prod.bDataHist:
            # prodDictNoHist8Submarket[ prod.submarket ].append( prod.code )
        else:
            # prodDictWithHist8Submarket[ prod.submarket ].append( prod.code )
        '''
    #return submarketLst, prodAll, prodIdMap, prodMapId, prodDict, prodDict8Submarket,                            prodDictNoHist8Submarket
    return submarketLst,           prodIdMap, prodMapId,           prodDict8Submarket #, prodDictWithHist8Submarket,prodDictNoHist8Submarket


def getWatchLst(fn):
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    for ln in rslt[1:]:
        flds = ln.split('\t')
        market = flds[0][:2]
        code = flds[0][2:]
        submarket = Submarket(market, code)
        if submarket=='' or submarket[2] <> 'S':
            continue
        p = Product.objects.get( code=code, market=market )
        if p==None:
            sys.stdout.write(  'product not found:' + code + '.' + market + '\r\n' )
            continue
        pWatch = WatchList(product=p, watchReason='')
        pWatch.save()
    #for prod in SSEProdLst:
    #    getAStockRealtime()

# watchLst: prodCode market
# realTimeTrading: prodCode price


'''
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
        p=Product(source='dzh', code=fLst[0], type='', market=market, name=fLst[1].decode('GBK'), submarket = Submarket(market, fLst[0]), maskSite='.' )   #, bDataHist=False
        recLst.append(p)
    Product.objects.bulk_create( recLst )






def dataCheck(conn):
    # wrong data
    cur = conn.cursor()

    cur.execute( "update myapp_product set errInfo = 'price=0' where id in (select distinct(product_id) from myapp_kdaily_cns where adjc = NULL or adjc=0 or o=0 or h=0 or l=0 or c=0)" )  # for sqlite3: adjc isnull
    cur.execute( "update myapp_product set errInfo = 'price=0' where id in (select distinct(product_id) from myapp_kdaily_hks where adjc = NULL or adjc=0 or o=0 or h=0 or l=0 or c=0)" )  # for sqlite3: adjc isnull
    conn.commit()




def redundant(conn):
    cur = conn.cursor()

    #cur.execute( "update myapp_product set dateHistEnd = '' where dateHistEnd isnull" )

    # weekday, week, month, year
    #'''
    cur.execute( "update myapp_kdaily_cns set weekday = weekday(date), week = weekofyear(date), month = month(date), year = year(date);" )
    cur.execute( "update myapp_kdaily_hks set weekday = weekday(date), week = weekofyear(date), month = month(date), year = year(date);" )
    # cur.execute( "update myapp_kdaily_cns set weekday = strftime('%w', date), week = strftime('%W', date), month = strftime('%m', date), year = strftime('%Y', date);" )  # sqlite3
    cur.execute( 'insert into myapp_kdaily_cns_tmp select * from myapp_kdaily_cns' ) # order by product_id, date asc;' ) #
    cur.execute( 'insert into myapp_kdaily_hks_tmp select * from myapp_kdaily_hks' ) # order by product_id, date desc;' )

    #cur.execute('insert into myapp_kdaily select * from  myapp_kdaily_cns_tmp where adjC=0 or vol=0 or c=0;')
    #cur.execute('insert into myapp_kdaily select * from  myapp_kdaily_hks_tmp where adjC=0 or vol=0 or c=0;')
    cur.execute( 'delete from myapp_kdaily_cns_tmp where vol=0 or c=0;' ) #  and o=h and o=l and o=c;' ) #   record that vol=0 is invalid holiday data; record that c=0 is error data
    #cur.execute( 'delete from myapp_kdaily_cni_tmp where adjC=0 or vol=0 or c=0;' ) #  and o=h and o=l and o=c;' )
    cur.execute( 'delete from myapp_kdaily_hks_tmp where vol=0 or c=0;' ) #  and o=h and o=l and o=c;' )  # 
    #cur.execute( 'delete from myapp_kdaily_hki_tmp where adjC=0 or vol=0 or c=0;' ) #  and o=h and o=l and o=c;' )
    conn.commit()

    cur.execute( 'ALTER  TABLE  myapp_kdaily_hks_tmp DROP id;' )
    cur.execute( 'ALTER  TABLE  myapp_kdaily_hks_tmp ADD id int( 11 ) NOT NULL  FIRST;' )
    cur.execute( 'ALTER  TABLE  myapp_kdaily_hks_tmp MODIFY COLUMN  id int( 11 ) NOT NULL  AUTO_INCREMENT,ADD PRIMARY  KEY(id);' )
    cur.execute( 'ALTER  TABLE  myapp_kdaily_cns_tmp DROP id;' )
    cur.execute( 'ALTER  TABLE  myapp_kdaily_cns_tmp ADD id int( 11 ) NOT NULL  FIRST;' )
    cur.execute( 'ALTER  TABLE  myapp_kdaily_cns_tmp MODIFY COLUMN  id int( 11 ) NOT NULL  AUTO_INCREMENT,ADD PRIMARY  KEY(id);' )
    conn.commit()

    #cur.execute( 'update myapp_kdaily_cns_tmp set a.p=b.c from myapp_kdaily_cns_tmp a, myapp_kdaily_cns_tmp b where a.product_id=b.product_id and a.id=b.id+1' )
    cur.execute( "update myapp_kdaily_cns_tmp set h=h*adjC/c, l=l*adjC/c, o=o*adjC/c, amt=c, c=adjC, adjC=amt;" ) # where errInfo isnull;" ) # , c=adjC;  # some adjC isnull lead to fail of update" )
    cur.execute( 'update myapp_kdaily_cns_tmp a, myapp_kdaily_cns_tmp b set a.p=b.c where a.product_id=b.product_id and a.id=b.id+1' )
    cur.execute( "update myapp_kdaily_hks_tmp set h=h*adjC/c, l=l*adjC/c, o=o*adjC/c, amt=c, c=adjC, adjC=amt;" ) # where errInfo isnull;" ) # , c=adjC;  # some adjC isnull lead to fail of update" )
    cur.execute( 'update myapp_kdaily_hks_tmp a, myapp_kdaily_hks_tmp b set a.p=b.c where a.product_id=b.product_id and a.id=b.id+1' )

    cur.execute( "update myapp_kdaily_cns_tmp set chngPerc = 100*(c-p)/p;" )
    cur.execute( "update myapp_kdaily_hks_tmp set chngPerc = 100*(c-p)/p;" )

    cur.execute( 'update myapp_kdaily_cns_tmp set p=0 where ISNULL(p);' )  # because load file to table will fail if the p is null
    cur.execute( 'update myapp_kdaily_hks_tmp set p=0 where ISNULL(p);' )
    cur.execute( 'update myapp_kdaily_cns_tmp set chngPerc = 100*(c-o)/o where ISNULL(p);' )  # because load file to table will fail if the p is null
    cur.execute( 'update myapp_kdaily_hks_tmp set chngPerc = 100*(c-o)/o where ISNULL(p);' )

    # ??:: 高阴涨>低阳跌   cp关系在chng字段 ??
    cur.execute( "update myapp_kdaily_hks_tmp set kt = 11 where c>p and c>=o;" )
    cur.execute( "update myapp_kdaily_hks_tmp set kt = 10 where c>p and c<o;" )
    cur.execute( "update myapp_kdaily_hks_tmp set kt = 1 where c<=p and c>o;" )
    cur.execute( "update myapp_kdaily_hks_tmp set kt = 0 where c<=p and c<=o;" )
    cur.execute( "update myapp_kdaily_cns_tmp set kt = 11 where c>p and c>=o;" )
    cur.execute( "update myapp_kdaily_cns_tmp set kt = 10 where c>p and c<o;" )
    cur.execute( "update myapp_kdaily_cns_tmp set kt = 1 where c<=p and c>o;" )
    cur.execute( "update myapp_kdaily_cns_tmp set kt = 0 where c<=p and c<=o;" )

    # update myapp_kdaily set type=0 where today's idxType
    # A股参考指标 上证指数/深综指 算术 涨幅平均    kt呢？  或自动根据相关度选择确定参考指标


    #'''
    # cur.execute( 'ALTER TABLE myapp_kdaily_cns RENAME TO myapp_kdaily_cns2; ALTER TABLE myapp_kdaily_cns_tmp RENAME TO myapp_kdaily_cns;' )
    # cur.execute( "insert into myapp_kdaily_cns select id, p, o, h, l, c, chngPerc, adjC, amt, vol, product_id, date, pDate,  strftime('%w', date) weekday, strftime('%W', date) week, strftime('%m', date) month, strftime('%Y', date) year from myapp_kdaily_cns_tmp;" )
    conn.commit()

    statement =" select * from myapp_kdaily_cns_tmp into outfile 'myapp_kdaily_cns_tmp.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
    cur.execute( statement )
    statement =" select * from myapp_kdaily_hks_tmp into outfile 'myapp_kdaily_hks_tmp.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
    cur.execute( statement )

    #cur.execute("insert into myapp_productposition(product_id, hYear, lYear) select product_id, max(h), min(l) from myapp_kdaily_cns_tmp where year=2015 and month<6 group by product_id;")
    #conn.commit()

def fromRedundant():
    import mysql.connector
    cnx = mysql.connector.connect(user='root', database='myapp')
    execScript4Mysql(cnx,    #sqlite3:  cur.executescript(
'''
delete from myapp_productposition;
insert into myapp_productposition(product_id, hYear, lYear) select product_id, max(h), min(l) from myapp_kdaily_cns_tmp where year=2015 group by product_id;  # ???  and month<9

delete from myapp_periodHL_;
insert into myapp_periodHL_(product_id, h, l) select product_id, max(h), min(l) from myapp_kdaily_cns_tmp where year=2015 and month>5 group by product_id;
update myapp_productposition set h3Mon=(select h from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);
update myapp_productposition set l3Mon=(select l from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);

delete from myapp_periodHL_;
insert into myapp_periodHL_(product_id, h, l) select product_id, max(h), min(l) from myapp_kdaily_cns_tmp where year=2014 group by product_id;
update myapp_productposition set h2Year=(select h from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);
update myapp_productposition set l2Year=(select l from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);

delete from myapp_periodHL_;
insert into myapp_periodHL_(product_id, h, l) select product_id, max(h), min(l) from myapp_kdaily_cns_tmp where year=2013 group by product_id;
update myapp_productposition set h3Year=(select h from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);
update myapp_productposition set l3Year=(select l from myapp_periodHL_ where myapp_productposition.product_id=myapp_periodHL_.product_id);

update myapp_productposition set c=(select c from myapp_kdaily_cns_tmp where myapp_productposition.product_id=myapp_kdaily_cns_tmp.product_id and myapp_kdaily_cns_tmp.date='2015-10-09');

update myapp_productposition set per2H = hyear / c;
update myapp_productposition set per2l = c / l3mon;
'''  # update myapp_productposition set per2l = c / lyear;
)
    #create view prodPos as select a.code, a.market, b.* from myapp_product a, myapp_productposition b where a.id=b.product_id
    #select  *, per2l*per2h space from prodpos where per2l*per2h>2.5 and c/l3year<1.2 and l3mon<lyear order by per2l;


def _addPreClose(conn):
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




def preTreatment(conn):
    pass



def groupK(fn, fld):  # conn, 
    t = time.clock()
    #dfD = pd.read_sql_query('select * from myapp_kDaily_cns_tmp where product_id = 8838 ', conn)
    #dfD = pd.read_sql_query('select product_id,date,p,o,h,l,c,vol,year,month,week from myapp_kDaily_cns_tmp', conn)
    dfD = pd.read_csv( fn )
    #dfD = pd.read_csv( r'C:\Users\Administrator\Desktop\myapp_kdaily_hks_tmp.csv' )
    print('read_sql_query time: %.03f' % (time.clock()-t) )
    
    t = time.clock()
    grouped = dfD.groupby([dfD['product_id'], dfD['year'], dfD[fld]])
    h=grouped['h'].max()
    l=grouped['l'].min()
    o=grouped['o'].first()
    p=grouped['p'].first()
    c=grouped['c'].last()
    vol=grouped['vol'].sum()
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
    rsltDf = pd.DataFrame(startD).join( [pd.DataFrame(p), pd.DataFrame(o), pd.DataFrame(h), pd.DataFrame(l), pd.DataFrame(c), pd.DataFrame(hD), pd.DataFrame(lD), pd.DataFrame(vol) ] )
    print('group month time: %.03f' % (time.clock()-t) )
    return rsltDf



#getWatchLst(r'D:\data\ths\export.txt')
#create view watchl as select code,name,market,watchreason from myapp_product, myapp_watchlist where myapp_watchlist.product_id=myapp_product.id 

fnLst = ['D:\data\codeBook\SH150926.SNT', 'D:\data\codeBook\SZ150926.SNT', 'D:\data\codeBook\HK150926.SNT', 'D:\data\codeBook\HI150926.SNT']
t = time.clock()
#getDzhCodeLst(fnLst[0], 'SH')
#getDzhCodeLst(fnLst[1], 'SZ')
#getDzhCodeLst(fnLst[2], 'HK')
#getDzhCodeLst(fnLst[3], 'HK')
print('getDzhCodeLst time: %.03f' % (time.clock()-t) )



#getHKProdLst_ifeng()

'''
t = time.clock()

l1 = getSSEProdLst()
for item in l1:
    p1=Product_(code=item[0], type='STOCK', market='SH', bDataHist=False, name=item[1], submarket = Submarket('SH', item[0]), maskSite='.' )
    #p1=Product_(code=item[0], type='stock', market=Market.objects.get(name='SH'), bDataHist=False, name=item[1], maskSite='.' )
    p1.save()

#prodLst = Product_.objects.all()

#from django.db import transaction
#transaction.set_autocommit(autocommit=False)
l2 = getSZSEProdLst()
#transaction.Atomic()
for key in l2:
    for item in l2[key]:
        p2=Product_(code=item[0],name=item[1],type=key, market='SZ', bDataHist=False, submarket = Submarket('SZ', item[0]), maskSite='.')
        #p2=Product_(code=item[0],name=item[1],type=key, market=Market.objects.get(name='SZ'), bDataHist=False, maskSite='.')
        p2.save()
#transaction.commit()
print('getSSEProdLst|getSZSEProdLst time: %.03f' % (time.clock()-t) )
'''

'''
cur = connHis.cursor()
statement =" select * from myapp_kdaily_cns_tmp into outfile 'myapp_kdaily_cns_tmp.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
statement =" select * from myapp_kdaily_hks into outfile 'myapp_kdaily_hks_tmp.csv' fields terminated by ',' " # optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'; 
cur.execute( statement )
'''

def group():
    t = time.clock()
    dfW = groupK(r'd:\myapp_kdaily_cns_tmp.csv', 'week') #connHis, 
    print('groupK time: %.03f' % (time.clock()-t) )
    t = time.clock()
    #dfW.to_sql('myapp_kweek', connHis, if_exists='append')
    dfW.to_csv('myapp_cns_kweek.csv', encoding='utf-8', index=True)
    print('to_sql time: %.03f' % (time.clock()-t) )
    
    dfM = groupK(r'd:\myapp_kdaily_cns_tmp.csv', 'month')  #connHis, 
    t = time.clock()
    #dfM.to_sql('myapp_kmonth', connHis, if_exists='append')
    dfM.to_csv('myapp_cns_kmonth.csv', encoding='utf-8', index=True)
    print('to_sql time: %.03f' % (time.clock()-t) )
    
    
    t = time.clock()
    dfW = groupK(r'd:\myapp_kdaily_hks_tmp.csv', 'week') #connHis, 
    print('groupK time: %.03f' % (time.clock()-t) )
    t = time.clock()
    #dfW.to_sql('myapp_kweek', connHis, if_exists='append')
    dfW.to_csv('myapp_hks_kweek.csv', encoding='utf-8', index=True)
    print('to_sql time: %.03f' % (time.clock()-t) )
    
    dfM = groupK(r'd:\myapp_kdaily_hks_tmp.csv', 'month')  #connHis, 
    t = time.clock()
    #dfM.to_sql('myapp_kmonth', connHis, if_exists='append')
    dfM.to_csv('myapp_hks_kmonth.csv', encoding='utf-8', index=True)
    print('to_sql time: %.03f' % (time.clock()-t) )

fromRedundant()

#group()

newBeforeHistBegin = False  # 假定每次数据入库后不会缺少dateHistBefore前时间段的数据，即dateHistBefore一旦产生后不会再变更
newAfterHistEnd = False

t = time.clock()
postImportData(conn)
print('postImportData time: %.03f' % (time.clock()-t) )

t = time.clock()
submarketLst, prodIdMap, prodMapId, prodDict8Submarket = prepareTrading()
print('prepareTrading time: %.03f' % (time.clock()-t) )

#'''
t = time.clock()
for i in range(11):
    getHist2Csv( prodDict8Submarket, 10+10*(i/2) )
print('getHist2Csv time: %.03f' % (time.clock()-t) )


t = time.clock()
newBeforeHistBegin = False
newAfterHistEnd = False
getHistFromCsv(prodDict8Submarket, conn)
postImportData(conn)
submarketLst, prodIdMap, prodMapId, prodDict8Submarket = prepareTrading()
print('getHistFromCsv time: %.03f' % (time.clock()-t) )

# getDzhCodeLst time: 55.077
# getSSEProdLst|getSZSEProdLst time: 139.763
# prepareTrading time: 0.937

t = time.clock()
for i in range(21):
    #continue
    newBeforeHistBegin = False
    newAfterHistEnd = False
    getHist( prodDict8Submarket, conn, 10+10*(i/2) )
    submarketLst, prodIdMap, prodMapId, prodDict8Submarket = prepareTrading()
    postImportData(conn)
print('getHist time: %.03f' % (time.clock()-t) )


t = time.clock()
priceAdjust(conn)
print('priceAdjust time: %.03f' % (time.clock()-t) )


fl = [r'D:\data\dailydzh\20150922.txt', r'D:\data\dailydzh\20150923.txt', r'D:\data\dailydzh\20150924.txt', r'D:\data\dailydzh\20150925.txt', r'D:\data\dailydzh\20150928.txt']
fl.sort()
#for f in fl:
t = time.clock()
#getQianLongDailyRpt(fl[-1], conn)
print('getQianLongDailyRpt time: %.03f' % (time.clock()-t) )
#postImportData(conn)
#fl = [u'D:\data\报价--深证Ａ股.txt', u'D:\data\报价--上证Ａ股.txt']
#getQianLongDailyRpt(fl[1], 'SH')

t = time.clock()
dataCheck(conn)
print('dataCheck time: %.03f' % (time.clock()-t) )


#for prod in prodAll:
#    prod.save(using='default')  ## ??? !!! 

t = time.clock()
redundant(conn)
print('redundant time: %.03f' % (time.clock()-t) )

fromRedundant()


t = time.clock()
getTickData(conn)
print('getTickData time: %.03f' % (time.clock()-t) )

t = time.clock()
qryRealtime()
print('qryRealtim time: %.03f' % (time.clock()-t) )

t = time.clock()
save2DiskDb()
print('save2DiskDb time: %.03f' % (time.clock()-t) )


getAStockRealtime('sz002594,sh510900,sz160125')
#'''

t = time.clock()
#useMemDb()
print('usememdb time: %.03f' % (time.clock()-t) )


def testMaskSite(prodDict8Submarket, timeout):
    qryEndDate = "&d=%02d&e=%02d&f=%d" % ( datetime.now().month-1, datetime.now().day, datetime.now().year )
    qryDate = "a=0&b=1&c=1989%s&g=d" % (qryEndDate)
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        market = key[:2]
        if key[2]<>'S' and key[2]<>'I':
            continue

        for prod in prodDict8Submarket[key]:
            if not('yaoo' in prod.maskSite.split('.')):
                continue

            csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\HistCsv\%s.%s.csv' % (market,prod.code)
            if market=='HK' and prod.code[0]=='0':
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code[1:] + '.' + market, qryDate )
            elif market == 'SH':
                #market=u'ss'
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + 'ss', qryDate )
            else:
                url = "http://ichart.yahoo.com/table.csv?s=%s&%s" % ( prod.code + '.' + market, qryDate )
            f = dataFromUrl(url, waittime=timeout)
            if f=='':
                continue
            if f=='url not found':
                continue
            prod.maskSite.replace('yahoo.', '')
            prod.save()
            with open(csvfn, 'w') as fp:
                fp.write( f )
    return    


def exportMaskSite():
    maskRecLst = []
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        '''
        market = key[:2]
        if key[2]<>'S' and key[2]<>'I':
            continue
        '''

        for prod in prodDict8Submarket[key]:
            if '.' == prod.maskSite:
                continue
            maskRecLst.append( prod.code + '.' + prod.submarket + ':::' + prod.maskSite + '\r\n')

    csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\maskSite4Product.txt'
    with open(csvfn, 'w') as fp:
        fp.writelines( maskRecLst )
    return    

def recoverMaskSite():
    csvfn = r'E:\GitHub\myapp\net\website\django\mysite1\maskSite4Product.txt'
    with open(csvfn, 'r') as fp:
        rslt = fp.readlines( )
    for line in rslt:
        x = line.split(':::')
        CM = x[0].split('.')
        CM = CM[0] + '.' + CM[1][:2] # .split('.')
        mask = x[1].strip().strip('.').split('.')
        mask = '.' + '.'.join( set(mask) ) + '.'
        prodMapId[ CM ].maskSite = mask
        prodMapId[ CM ].save()

def calcIdx(conn):
    import talib
    import pandas as pd

    for key in prodDict8Submarket.keys():
        market = key[:2]
        for prod in prodDict8Submarket[key]:
            if prod.dateHistBegin == None:
                continue
            tblName = 'myapp_kdaily_' + MapSubmarket2Table( key )
            #if prod.id<1115:
            #    continue
            ###    ????????????  　read_table 
            dayk = pd.read_sql_query('select * from %s where product_id=%s' % (tblName, prod.id), conn)
            if len(dayk)==0:
                continue
            dayk['o'] = dayk.o.values.astype('float64')
            dayk['h'] = dayk.h.values.astype('float64')
            dayk['l'] = dayk.l.values.astype('float64')
            dayk['c'] = dayk.c.values.astype('float64')
            dayk['p'] = dayk.p.values.astype('float64')
            sma5 = talib.SMA( dayk.l.values, timeperiod=5)
            sma10 = talib.SMA( dayk.c.values, timeperiod=10)
            sma20 = talib.SMA( dayk.c.values, timeperiod=20)
            sma60 = talib.SMA( dayk.c.values, timeperiod=60)
    
            minv = talib.MIN(dayk.l.values)
            maxv = talib.MAX(dayk.h.values)
            floorv = talib.FLOOR(dayk.h.values)
            ceilv = talib.CEIL(dayk.l.values)
            
            cci14 = talib.CCI( dayk.h.values, dayk.l.values, dayk.c.values)
            cci = talib.CCI( dayk.h.values, dayk.l.values, dayk.c.values)
            bol20 = talib.BBANDS(dayk.c.values, timeperiod=20)
            rsi = talib.RSI(dayk.c.values)
            macd = talib.MACD(dayk.c.values, )
            df=pd.DataFrame(dayk.date)
            pidL = len(cci14)*[prod.id]
            df['product_id']=pd.Series(pidL)
            df['cci']=pd.Series(cci14)
            df.to_sql('myapp_productidx', conn, if_exists='append', index=False)


def trendSense(df):
    direction = ''
    idxL = ['1', '2', '3', '4']   # time sequence: L[0] is the earliest data, L[-1] is the latest data
    if idxL[0]<=idxL[1] and idxL[1]<=idxL[2] and idxL[2]<=idxL[3]  and idxL[0]<idxL[3]:
        direction = 'rise'
        # acceleration = ( (idxL[3]-idxL[0])/idxL[0] ) / ( 3 * (idxL[1]-idxL[0])/idxL[0] )
        acceleration = (idxL[3]-idxL[0]) / ( 3 * (idxL[1]-idxL[0]) )
    elif idxL[0]>=idxL[1] and idxL[1]>=idxL[2] and idxL[2]>=idxL[3]  and idxL[0]>idxL[3]:
        direction = 'fall'
        acceleration = (idxL[3]-idxL[0]) / ( 3 * (idxL[1]-idxL[0]) )

'''
技术筛选条件： 指标/时间段内极端？涨跌
筛选全历史中.1%时间段的机会特征, 1千个品种则每日都有机会？ 
  速度：   l is y0    (h-l)/(hDate-lDate)  基准速度：全历史段 / period 
 变速:  1.5倍为视觉显著可感？
 振荡：  10个基准时间单位内(振幅?) 5次穿越中值
每日变速/基准速度  (1.2,0.8) 
'''



def groupK_():
    import pandas as pd
    from datetime import datetime
    
    def strdate(int):   # ??intdate
        return datetime.strptime(str(int), '%Y%m%d')
    
    for id in prodIdMap.keys():
        p = prodIdMap[id]
        dayk1 = pd.read_sql_query('select * from dayK1 where market="%s"' % (p.code,p.market), conn)
        dates=map(strdate, dayk1.date.values)

        ts = pd.Series(dayk1.h.values, index=dates)
        tsh = ts.resample('W', how='max')
    
        ts = pd.Series(dayk1.l.values, index=dates)
        tsl = ts.resample('W', how='min')
    
        ts = pd.Series(dayk1.h.values, index=dates)
        tsh = ts.resample('W', how='max')



testMaskSite(prodDict8Submarket, 20)
#exportMaskSite()
#recoverMaskSite()
calcIdx(conn)


# update myapp_product set errInfo = '1' where code in (select a.code from myapp_product_ a, myapp_product b where a.code = b.code and a.market = b.market);
# update myapp_product_ set errInfo = '1' where code in (select code from myapp_product where myapp_product.code = myapp_product_.code and myapp_product.market = myapp_product_.market);
# insert into myapp_product(code, market, submarket, name, type, bDataHist, errInfo) select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where errInfo = '' and submarket like 'S%I';
# insert into myapp_product(code, market, submarket, name, type, bDataHist, errInfo) select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where submarket = 'SHI';
# insert into myapp_product(code, market, submarket, name, type, bDataHist, errInfo) select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where submarket like 'HKS%';select code, market, submarket, name, type, bDataHist, errInfo from myapp_product_ where submarket like 'HKS%';


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
