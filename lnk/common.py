# coding=utf-8

import os
import sys
import time
from datetime import datetime, timedelta

import django

prjPath = r'E:\GitHub\myapp\net\website\django\mysite1'
dataPath = r'D:\data'

#from net.website.django.mysite1.myapp.rules import Submarket
sys.path.append( prjPath )
django.setup()

import sqlite3 as db
#conn = db.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
conn = db.connect( django.conf.settings.DATABASES['default']['NAME'] ) #r"D:\data\slowdb\db.sqlite3")

#import mysql as db  #connector.paramstyle　
#import MySQLdb as db
#conn = db.connect( host='localhost', user='root', passwd='', db='myapp', charset='utf8' )

#from selenium import webdriver


from myapp.rules import Submarket, MapSubmarket2Table # net.website.django.mysite1.

from myapp.models import * #Product_, Product, KDaily, KMin, WatchList, Market, StockInfo, TradeRealTime

def arrangeCsvScan(dir):
    import scandir
    for path, subdirs, files in scandir.walk(dir):
        for fn in files:
            market,submarket,code,market,x = fn.split('.')
            if x<>'csv':
                sys.stdout.write(  'not csv file:' + fn + '\r\n' )
            #submarket = Submarket(market, code)
            os.rename( os.path.join(path,fn), os.path.join(path,market + '.' + submarket + '.' + code + '.' + 'csv') )

def arrangeCsv8Dict(prodDict8Submarket): 
    for key in prodDict8Submarket.keys():
        if key==None or key == '' or key == 'ERR':
            continue
        market = key[:2]
        for prod in prodDict8Submarket[key]:
            csvfn = r'D:\data\histcsv\ths\%s.%s.csv' % (market,prod.code)
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
    return


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


def execScript4Mysql(conn, script):
    sqlLst = script.split(';')
    cur = conn.cursor()
    for sql in sqlLst:
        if sql.strip()=='':
            continue
        cur.execute(sql)
    conn.commit()



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

def getWatchLst_ThsExport(fn):
    try:
        with open( fn ) as fp:  # HTTP Error 404: Not Found
            rslt = fp.readlines()
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    wtchL = []
    for ln in rslt[1:]:
        flds = ln.split('\t')
        if flds[0].isdigit():
            market = 'HK'
            code = flds[0]
        else:
            market = flds[0][:2]
            code = flds[0][2:]
        if market not in [ 'SZ', 'SH' ]: #, 'HK' ]:
            continue

        submarket = Submarket(market, code)
        if submarket=='' or submarket[2] <> 'S':
            continue

        wtchL.append( code+'.'+market )
    return wtchL
    '''
        p = Product.objects.get( code=code, market=market )
        if p==None:
            sys.stdout.write(  'product not found:' + code + '.' + market + '\r\n' )
            continue
        pWatch = WatchList(product=p, watchReason='')
        pWatch.save()
    '''
    #for prod in SSEProdLst:
    #    getAStockRealtime()

# watchLst: prodCode market


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


'''
t = time.clock()
#useMemDb()
print('usememdb time: %.03f' % (time.clock()-t) )


t = time.clock()
save2DiskDb()
print('save2DiskDb time: %.03f' % (time.clock()-t) )
'''
