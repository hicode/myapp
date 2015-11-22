# coding=utf-8

from ctypes import *

from net.url.dataSource import regDataFromUrl, dataFromUrl

from common import * 
import globalData
from curses.ascii import isdigit


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


def getHist(prodDict8Submarket, conn, timeout):  # http://ichart.yahoo.com/table.csv?s=600000.SS&a=01&b=01&c=1990&d=08&e=30&f=2015&g=d 
    newBeforeHistBegin = False  # 假定每次数据入库后不会缺少dateHistBefore前时间段的数据，即dateHistBefore一旦产生后不会再变更
    newAfterHistEnd = False


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

    postImportData(conn, newAfterHistEnd, newBeforeHistBegin)
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
    newBeforeHistBegin = False  # 假定每次数据入库后不会缺少dateHistBefore前时间段的数据，即dateHistBefore一旦产生后不会再变更
    newAfterHistEnd = False

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


    t = time.clock()
    postImportData(conn, newAfterHistEnd, newBeforeHistBegin)
    print('postImportData time: %.03f' % (time.clock()-t) )
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
        p = globalData.prodMapId[ code + '.' + market ]    # p = Product.objects.get(id=prod_id)        #except ObjectDoesNotExist:
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
    postImportData(conn, newAfterHistEnd=True)  #　??:: newAfterHistEnd=True


def csv2Db(path,conn):
    for file in path:
        cur = conn.cursor()
        #f = sys.read(file)
        conn.commit()

def postImportData(conn, newAfterHistEnd=False, newBeforeHistBegin=False):
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

# move to common
# def getWatchLst_ThsExport(fn):
# def getDzhCodeLst(fn, market):



class weight_QL(Structure):
    _pack_ = 1
    _fields_ = [ ('date',c_int32), ('stckCntAsGift',c_int32), ('stckCnt4Sell',c_int32), ('p4Sell',c_int32), ('bonus',c_int32), ('stckCntofIncr',c_int32), ('stckOwnership',c_int32), ('freeStckCnt',c_int32), ('emptyMark',c_int32) ]


def getWeight_QL(fn, pid):
    try:
        recLst = []
        with open( fn, 'rb' ) as fp:  # HTTP Error 404: Not Found
            rec = weight_QL()
            while 0 <> fp.readinto( rec ):   # sizeof(head) is 20 ??set pack=1  # x = fp.read(16)
                if rec.emptyMark<>0:
                    print 'weight file error: emptyMark is not 0\r\n'
                year = rec.date >> 20
                mon = (rec.date%0x100000) / 0x10000    # (int)(((uint)(oneRow[0] << 12))>> 28);
                day = (rec.date&0xffff) >> 11
                recLst.append( [pid, '%04d-%02d-%02d' % (year, mon, day), rec.stckCntAsGift/100000.0, rec.stckCnt4Sell/100000.0, rec.p4Sell/1000.0, rec.bonus/10000.0, rec.stckCntofIncr/100000.0, rec.stckOwnership, rec.freeStckCnt ] )
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return recLst

def getQlData(conn):
    cur = conn.cursor()
    import scandir

    dirLst = [('sznse', 'sz'), ('shase', 'sh'), ('hkse','hk')]
    for d in dirLst:
        #for dir in 
        dir = 'D:\\qianlong1\\qijian\\QLDATA\\history\\%s\\weight\\' % d[0]
        market = d[1].upper()
        tblName = 'myapp_productweight'
        recLst = []
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                if market=='HK':
                    code = '0' + code
                prodId=code + '.' + market
                if prodId not in globalData.prodMapId.keys():
                    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                    continue
                recL = getWeight_QL(dir + fn, globalData.prodMapId[prodId].id)
                lines = ['pid,date,giftStck,sellStck,p4Sell,bonus,incrStck,totalStck,freeStck\r\n']
                recLst += recL
                for rec in recL:
                    ln = code + '.' + market
                    y,m,d = str(rec[1]).split('-')
                    ln += ',' + y+m+d   
                    for fld in rec[2:]: 
                        ln += ',' + str(fld)
                    ln += '\r\n'
                    lines.append( ln )
                with open(r'D:\data\weightcsv\ql\%s.%s.wght.csv' % (market, code), 'w') as fp:
                    fp.writelines( lines )

                submarket = Submarket(market, code)
        #cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", recLst )
        #cur.executemany( "insert into %s(product_id, date, bonus, giftStck, incrStck, sellStck, p4SellStck, freeStck, totalStck)" % tblName + " values (?,?,?,?,?,?,?,?,?)", recLst )
        #conn.commit()

def getQLData2OneFile(conn):
    cur = conn.cursor()
    import scandir

    dirLst = [('sznse', 'sz'), ('shase', 'sh'), ('hkse','hk')]
    head = 'pid,date,giftStck,sellStck,p4Sell,bonus,incrStck,totalStck,freeStck\r\n'
    recDict = {}
    for d in dirLst:
        dir = 'D:\\qianlong1\\qijian\\QLDATA\\history\\%s\\weight\\' % d[0]
        market = d[1].upper()
        recLst = []
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                if market=='HK':
                    code = '0' + code
                prodId=code + '.' + market
                if prodId not in globalData.prodMapId.keys():
                    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                    continue
                submarket = Submarket(market, code)
                if not( submarket in recDict.keys() ):
                    recDict[submarket] = []
                    recDict[submarket].append(head)

                recL = getWeight_QL(dir + fn, globalData.prodMapId[prodId].id)
                for rec in recL:
                    ln = code + '.' + market
                    y,m,d = str(rec[1]).split('-')
                    ln += ',' + y+m+d   
                    for fld in rec[2:]: 
                        ln += ',' + str(fld)
                    ln += '\r\n'
                    recDict[submarket].append( ln )
    for subM in recDict.keys():
        with open(r'D:\data\weightcsv\ql\%s.wght.csv' % subM, 'w') as fp:
            fp.writelines( recDict[subM] )


class dayK_THS_rec(Structure):
    _pack_ = 1
    _fields_ = [ ('date',c_uint32), ('o',c_uint32), ('h',c_uint32), ('l',c_uint32), ('c',c_uint32), ('amnt',c_uint32), ('vol',c_uint32) ] #,
    '''  
      ('rsv1',c_uint32) , ('rsv2',c_uint32), ('rsv3',c_uint32), ('rsv4',c_uint32), ('rsv5',c_uint32), ('rsv6',c_uint32), ('rsv7',c_uint32), ('rsv8',c_uint32), ('rsv9',c_uint32), ('rsv10',c_uint32),
      ('rsv11',c_uint32) , ('rsv12',c_uint32), ('rsv13',c_uint32), ('rsv14',c_uint32), ('rsv15',c_uint32), ('rsv16',c_uint32), ('rsv17',c_uint32), ('rsv18',c_uint32), ('rsv19',c_uint32), ('rsv20',c_uint32),
      ('rsv21',c_uint32) , ('rsv22',c_uint32), ('rsv23',c_uint32), ('rsv24',c_uint32), ('rsv25',c_uint32), ('rsv26',c_uint32), ('rsv27',c_uint32), ('rsv28',c_uint32), ('rsv29',c_uint32), ('rsv30',c_uint32),
      ('rsv31',c_uint32) , ('rsv32',c_uint32), ('rsv33',c_uint32), ('rsv34',c_uint32), ('rsv35',c_uint) ]
    '''


class tHS_FHeader(Structure):  # ?? BigEndianStructure
    _pack_ = 1
    _fields_ = [ ('sign', c_uint32), ('w1', c_uint16), ('recCount', c_uint32), ('headerLen', c_uint16), ('recLen', c_uint16), ('fldCount', c_uint16) ]   # header.RecordCount = reader.ReadUInt32() & 0xffffff;
    # ('fldCount', c_uint32)

def getValTHS(val):
    num = val & 0xfffffff  # 后28bit
    num2 = val >> 0x1c     # 前4bit
    if num2 & 7 == 0:      # 2/3/4bit为000
        return num
    num3 = pow(10.0, (num2&7))
    if (num2&8)<>0:        # 1bit is 1
        return num/num3
    return num * num3

def hisFromThs(fn, pid):
    #fn = r'C:\htzqzyb2\history\shase\day\600000.day'
    k1=dayK_THS_rec()
    try:
        recLst = []
        with open( fn, 'rb' ) as fp:  # HTTP Error 404: Not Found
            head = tHS_FHeader()
            fp.readinto( head )   # sizeof(head) is 20 ??set pack=1  # x = fp.read(16)
            fp.read( head.headerLen-sizeof(head) ) # read columnList
            head.recCount = head.recCount & 0xffffff
            for i in range(head.recCount):  #while fp.readinto(k1):
                _size = fp.readinto(k1)
                if i==head.recCount-1:
                    pass
                fp.read( head.recLen-sizeof(k1) ) # unused
                if k1.date==0 or k1.o==0 or k1.h==0 or k1.l==0 or k1.c==0 or k1.amnt==0 or k1.vol==0:
                    sys.stdout.write(  'error history record of pid_date:' + str(pid) + str(k1.date) + 'record:: ' + str(k1) + '\r\n' )
                    continue
                dateStr = '%04d-%s-%02d' % (k1.date/10000, str(k1.date)[4:6], k1.date%100)
                vol = getValTHS(k1.vol)
                amt = getValTHS(k1.amnt)
                if vol==0:
                    avg = None
                    vol = None
                else:
                    avg = amt*1.0/vol
                recLst.append( [pid, dateStr, getValTHS(k1.o), getValTHS(k1.h), getValTHS(k1.l), getValTHS(k1.c), amt, vol, avg, 0] )
    except IOError, e:
        sys.stdout.write(  'except while access file:' + fn + 'IOError: ' + str(e) + '\r\n' )
        return ''
    return recLst

def getTHSData(conn):
    cur = conn.cursor()
    import scandir

    dirLst = [('sznse', 'sz'), ('shase', 'sh'), ('hk','hk'), ('hk72','hk')]
    fileDict = {}
    for d in dirLst:
        #for dir in 
        dir = 'C:\\htzqzyb2\\history\\%s\\day\\' % d[0]
        market = d[1].upper()
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                #if code<>'600072':
                #    continue
                prodId=code + '.' + market
                if prodId not in globalData.prodMapId.keys():
                    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                    continue
                #fileDict[prodId] = (dir + fn, code, market)
                recLst = hisFromThs(dir + fn, globalData.prodMapId[prodId].id)
                lines = ['pid,y,m,d,date,o,h,l,c,amt,vol,avg,AdjC\r\n']  #fp.write('Date,Open,High,Low,Close,amt,vol,AdjC\r\n')
                for rec in recLst:
                    ln = code + '.' + market
                    y,m,d = str(rec[1]).split('-')
                    ln += ',' + y + ',' + m + ',' + d + ',' + y+m+d   
                    for fld in rec[2:]: 
                        ln += ',' + str(fld)
                    ln += '\r\n'
                    lines.append( ln )
                submarket = Submarket(market, code)
                with open(r'D:\data\histcsv\ths\%s.%s.%s.csv' % (market,submarket,code), 'w') as fp:
                    fp.writelines( lines )

                '''
                tblName = 'myapp_kdaily_' + MapSubmarket2Table( submarket )
                try:
                    #cur.executemany( "insert into %s(product_id, date, o, h, l, c, amt, vol, adjC)" % tblName + " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", recLst )
                    cur.executemany( "insert into %s(product_id, date, o, h, l, c, amt, vol, adjC)" % tblName + " values (?,?,?,?,?,?,?,?,?)", recLst )
                except db.Error,e:
                    sys.stdout.write(  'except while executemany insert:' + prodId + ' Error: ' + str(e) + '\r\n' )
                conn.commit()
                '''

def getTHSData2OneFile(conn):
    cur = conn.cursor()
    import scandir

    dirLst = [('sznse', 'sz'), ('shase', 'sh'), ('hk','hk'), ('hk72','hk')]
    fileDict = {}
    head = 'pid,y,m,d,date,o,h,l,c,amt,vol,avg,AdjC\r\n'  #fp.write('Date,Open,High,Low,Close,amt,vol,AdjC\r\n')
    recDict = {}
    for d in dirLst:
        #for dir in 
        dir = 'C:\\htzqzyb2\\history\\%s\\day\\' % d[0]
        market = d[1].upper()
        for path, subdirs, files in scandir.walk(dir):
            for fn in files:
                code=fn.split('.')[0]
                prodId=code + '.' + market
                if prodId not in globalData.prodMapId.keys():
                    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                    continue
                submarket = Submarket(market, code)
                if not( submarket in recDict.keys() ):
                    recDict[submarket] = []
                    recDict[submarket].append(head)

                recLst = hisFromThs(dir + fn, globalData.prodMapId[prodId].id)
                for rec in recLst:
                    ln = code + '.' + market
                    y,m,d = str(rec[1]).split('-')
                    ln += ',' + y + ',' + m + ',' + d + ',' + y+m+d   
                    for fld in rec[2:]: 
                        ln += ',' + str(fld)
                    ln += '\r\n'
                    recDict[submarket].append( ln )

    for subM in recDict.keys():
        with open(r'D:\data\histcsv\ths\%s.csv' % subM, 'w') as fp:
            fp.writelines( recDict[subM] )
