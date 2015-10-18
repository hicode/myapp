# coding=utf-8

import sys
import time
from datetime import datetime, timedelta

import sqlite3 as db
#conn = db.connect(r"E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3")
conn = db.connect(r"D:\data\slowdb\db.sqlite3")

#import mysql as db  #connector.paramstyle　
#import MySQLdb as db
#conn = db.connect( host='localhost', user='root', passwd='', db='myapp', charset='utf8' )

#from selenium import webdriver

import django

prjPath = r'E:\GitHub\myapp\net\website\django\mysite1'
dataPath = r'D:\data'

#from net.website.django.mysite1.myapp.rules import Submarket
sys.path.append( prjPath )
django.setup()

from myapp.rules import Submarket, MapSubmarket2Table # net.website.django.mysite1.

from myapp.models import * #Product_, Product, KDaily, KMin, WatchList, Market, StockInfo, TradeRealTime


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

'''
t = time.clock()
#useMemDb()
print('usememdb time: %.03f' % (time.clock()-t) )


t = time.clock()
save2DiskDb()
print('save2DiskDb time: %.03f' % (time.clock()-t) )
'''
