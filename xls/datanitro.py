# coding=utf-8

import pandas as pd

from common import *
#import sqlite3 as db
#conn = db.connect(r'D:\data\slowdb\east.sqlite3')
#cur = conn.cursor()
'''
from net.website.django.mysite1.myapp.models import TradeRealTime
from xlwt.Utils import cellrange_to_rowcol_pair
'''


def getEastPrdLst():
    prdLst = []
    with open(r'd:\east.txt') as fp:
    #with open(r'd:\dzhEastPrdLst.txt') as fp:
        prdLst = fp.readlines()
    
    prdDict = {}
    colCode = []
    colName = []
    colMarket = []
    colSubmarket = []
    colId = []
    #rowNum = 1
    recLst = []
    for prd in prdLst[1:]:
        flds = prd.strip().split('\t')
        colId.append( flds[0] )
        colName.append( flds[1].decode('GBK') )
        colCode.append( flds[2] )
        colMarket.append( flds[3] )
        colSubmarket.append( Submarket(flds[3], flds[2]) )
        #prdDict[ flds[0] ] = flds
        #recLst.append( [ flds[2], flds[3], flds[1].decode('GBK'), Submarket(flds[3], flds[2]) ] )
        #rowNum += 1
        #CellRange( 'prodDict', 'A%d:D%d'%(rowNum, rowNum) ).value = prdDict[ flds[0] ]
    
    d={'name': pd.Series(colName, index=colId),
       'code': pd.Series(colCode, index=colId),
       'market': pd.Series(colMarket, index=colId),
       'submarket': pd.Series(colSubmarket, index=colId),
       }
    
    prdDf = pd.DataFrame( d )
    return prdDf


def calcWght_(dir, allPrd):
    cur = conn.cursor()
    import scandir

    for path, subdirs, files in scandir.walk(dir):
        for fn in files:
            market,code,x,y = fn.split('.')
            if market=='HK':
                code = '0' + code
            prodId=code + '.' + market
            if prodId not in globalData.prodMapId.keys():
                sys.stdout.write(  'code not found:' + prodId + '\r\n' )
                continue
            df = pd.read_csv( dir+fn, index_col=['pid', 'date'])
            df['wght'] = 1
            df['freeShr'] = 0  # million            # df['totShr'] = 0
            pWght = 1
            for d in df.date:
                wghtC = (c-bonus + pSell*sell)/(1+ sell+ incr + gift)  # 除权除息价＝(股权登记日的收盘价－每股所分红利现金额＋配股价×每股配股数) ÷ (1＋每股送红股数＋每股配股数)
                wght = c/wghtC
                
    
    allPrd['wght'] = pd.Series(1, allPrd.index)
    for prd in prdDf.code:
        pass
    for prd in allPrdWght.pid:
        prdWght = allPrdWght


def readHistCsv():
    t = time.clock()
    allPrd =  pd.DataFrame({})
    allPrdWght =  pd.DataFrame({})
    dfl = []
    dflWght = []
    for subM in [ 'HKS', 'HKSC' ]:
    #for subM in ['SZS', 'SZSC', 'SZSZ', 'SHS', 'SHSB', 'SZSB' ]:
    #for subM in ['SZS', 'SZSC', 'SZSZ', 'SHS', 'SHSB', 'SZSB', 'HKS', 'HKSC' ]:
        dfl.append( pd.read_csv( r'D:\data\histcsv\ths\%s.csv' % subM, index_col=['pid', 'y', 'm', 'date'], encoding='gbk') )
        dflWght.append( pd.read_csv( r'D:\data\weightcsv\ql\%s.wght.csv' % subM, index_col=['pid', 'date'], encoding='gbk') )
    allPrd = pd.concat(dfl).sort(ascending=False) #, ignore_index=True)
    allPrdWght = pd.concat(dflWght).sort(ascending=False)
    print('get allPrd time: %.03f' % (time.clock()-t) )

    return allPrd

def calcWght(dir, allPrd):
    cur = conn.cursor()
    import scandir

    allPrd['wght'] = None # pd.Series(1, allPrd.index)
    allPrd['freeShare'] = None
    allPrd['totShare'] = None
    allPrd['p'] = None
    grped = allPrd.groupby(level=0) #'pid'
    for pid, group in grped:
        grp = group.reset_index()
        p = grp.iloc[grp.index[:-1]+1]['c']
        p[len(p)+1] = None
        p.index = grp.index
        #p.iat[-1]=None  #,'c'
        #allPrd[pid, level=0]
        allPrd['p'][pid]=p   #[:-1] = p  # allPrd[:-1, ['p']] = p
        grp['p'] = p # [:-1] = p
        grp['wght'] = 1 # pd.Series(1, allPrd.index)
        grp['freeShare'] = None
        grp['totShare'] = None

        code,market = pid.split('.')
        fPath = dir+market+'.'+code+'.wght.csv'
        if os.path.exists(fPath):
            dfWght = pd.read_csv( fPath ).sort(ascending=False).reset_index() #.query('date>20120101') #, index_col=['pid', 'date'])
            # grp = grp.set_index('date')            dfWght['p'] = grp.loc[ dfWght['date'].values ]['p'].values            grp = grp.reset_index()
            #dfWght['wght'] = 1
            #df['freeShr'] = 0  # million            # df['totShr'] = 0
        
            wght = grp['wght'][0]
            wghtL = []
            freeShareL = []
            totShareL = []
            #free = 0
            #tot = 0 
            iGrp = 0
            for i in dfWght.index: # for dk in grp:
                #pFree = free #freeShareL += [ grp['freeShare'].iat[ iGrp ] ] * iGrp
                #pTot = tot #totShareL += [ grp['totShare'].iat[ iGrp ] ] * iGrp
    
                x, y, date, gift, sell, pSell, bonus, incr, tot, free = dfWght.iloc[i] #, p = dfWght.iloc[i]
                if (grp['date'].tail(1)>=date).values[0]:
                    break
                iGrp = grp['date'].index[ grp['date']<date ]
                #grp['freeShare'].iat[ iGrp ] = free
                #grp['totShare'].iat[ iGrp ] = tot
    
                if len(iGrp)==0:    #  000001.sz 20071231 非交易日 无P
                    continue
                copyLen = iGrp[0]-len(wghtL)
                c = grp['c'][ iGrp[0] ]  # p = grp['p'][ iGrp[0] ]
                wghtL += [wght] * copyLen
                freeShareL += [free] * copyLen
                totShareL += [tot] * copyLen
                # grp['wght'][i] =  wght
    
                diviC = (c - bonus + pSell*sell) / (1 + sell + incr + gift)  #diviC = (p - bonus + pSell*sell) / (1 + sell + incr + gift)
                wght = wght * ( c / diviC )  # wght = wght * ( p / diviC )

            copyLen = len(grp) - len(wghtL)
            wghtL += [wght] * copyLen
            freeShareL += [free] * copyLen
            totShareL += [tot] * copyLen
            # grp['wght'][i] =  wght
    
    
            #grp['wght'] = wghtL
            #grp['freeShare'] = freeShareL
            #grp['totShare'] = totShareL
            allPrd['wght'][pid] = wghtL  #[:len(wghtL)] = wghtL
            allPrd['freeShare'][pid] = freeShareL  #[:len(wghtL)] = freeShareL
            allPrd['totShare'][pid] = totShareL  #[:len(wghtL)] = totShareL
            #allPrd.to_csv(r"D:\data\csvCalc\allprd1.csv")


    allPrd_divi = allPrd.copy()
    allPrd_divi['o'] = allPrd['o']/allPrd['wght']
    allPrd_divi['h'] = allPrd['h']/allPrd['wght']
    allPrd_divi['l'] = allPrd['l']/allPrd['wght']
    allPrd_divi['c'] = allPrd['c']/allPrd['wght']
    allPrd_divi['p'] = allPrd['p']/allPrd['wght']

    return allPrd, allPrd_divi

    '''
    pidL = allPrd.index.get_level_values(0).unique()
    for prd in prdDf.code:
        pass
    for prd in allPrdWght.pid:
        prdWght = allPrdWght

    for path, subdirs, files in scandir.walk(dir):
        for fn in files:
            market,code,x,y = fn.split('.')
            if market=='HK':
                code = '0' + code
                #continue
            prodId=code + '.' + market
            #if prodId not in globalData.prodMapId.keys():
            #    sys.stdout.write(  'code not found:' + prodId + '\r\n' )
            #    continue
            df = pd.read_csv( dir+fn, index_col=['pid', 'date'])
            df['wght'] = 1
            df['freeShr'] = 0  # million            # df['totShr'] = 0

            pWght = 1
            for d in df.date:
                wghtC = (c-bonus + pSell*sell)/(1+ sell+ incr + gift)  # 除权除息价＝(股权登记日的收盘价－每股所分红利现金额＋配股价×每股配股数) ÷ (1＋每股送红股数＋每股配股数)
                wght = c/wghtC
    '''



wtchL = getWatchLst_ThsExport(r'D:\data\ths\zixuan1.txt')
wtchLAll = getWatchLst_ThsExport(r'D:\data\ths\zixuan.txt')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan1.txt')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan2')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan3')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan4')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan5')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan6')
wtchLAll += getWatchLst_ThsExport(r'D:\data\ths\zixuan7')
wtchLAll = list(set(wtchL))

t = time.clock()
allPrd =  pd.read_csv( r'D:\data\csvCalc\pdA_divi.csv', index_col=['pid', 'y', 'm', 'date'], encoding='gbk')
#allPrd = readHistCsv()
#allPrd, allPrd_divi = calcWght('D:\\data\\weightcsv\\ql\\', allPrd)
#allPrd.to_csv('D:\data\csvCalc\pdA.csv')
#allPrd_divi.to_csv('D:\data\csvCalc\pdA_divi.csv')
print('read allPrd csv time: %.03f' % (time.clock()-t) )

prdDf = getEastPrdLst()
x=len(prdDf.code)+1

'''
CellRange('prodDict', 'A2:A%d'%x).value = prdDf.index
CellRange('prodDict', 'B2:B%d'%x).value = prdDf.name
CellRange('prodDict', 'C2:C%d'%x).value = prdDf.code
CellRange('prodDict', 'D2:D%d'%x).value = prdDf.market
CellRange('prodDict', 'E2:E%d'%x).value = prdDf.submarket
'''

allPrd = allPrd.query('y==2015 or y==2014') # or y==2013 or y==2012')  # allPrd.xs('000001.SZ',level='pid')



dfmG = allPrd.groupby( level=['pid','y','m'] )
h15y = df15yG['h'].max()
h15y.name = 'h15y'
ih = df15yG['h'].idxmax()  
splitIdxVal = zip(*ih.values)
#hd15y = df15y.iloc[ih].date
#hd15y = pd.Series( ih.get_level_values(3), index=h15y.index)
#hd15y.name='hd15y'
#hd15y.index=h15y.index
grpDf = pd.DataFrame(h15y).join( [ pd.DataFrame( list(splitIdxVal[3]), index=h15y.index ) ] )






h15 lPost  hPost at930 l1019P h10m





df15y = allPrd.query('y==2015')  # allPrd.xs('000001.SZ',level='pid')
df15yG = df15y.groupby( level='pid' )
h15y = df15yG['h'].max()
h15y.name = 'h15y'
ih = df15yG['h'].idxmax()  
splitIdxVal = zip(*ih.values)
#hd15y = df15y.iloc[ih].date
#hd15y = pd.Series( ih.get_level_values(3), index=h15y.index)
#hd15y.name='hd15y'
#hd15y.index=h15y.index
grpDf = pd.DataFrame(h15y).join( [ pd.DataFrame( list(splitIdxVal[3]), index=h15y.index ) ] )


#c930 = allPrd.xs( 20150930, level='date' )
df930 = allPrd.query( "date==20150930" )
# grpDf = pd.DataFrame(grpDf).join( [pd.DataFrame(df930['c'], index=)] )


df10m = allPrd.query('y==2015' and 'm==10')
#df10m = allPrd[ allPrd['y']=='2015' and allPrd['m']=='10']
df10mG = df10m.groupby( level='pid' )
h10m = df10mG['h'].max()
h10m.name = 'h10m'
ih = df10mG['h'].idxmax()
hd10m = df10m.iloc[ih]['date']
hd10m.name='hd10m'
hd10m.index=h10m.index
grpDf = pd.DataFrame(grpDf).join( [pd.DataFrame(h10m), pd.DataFrame(hd10m) ] )


df1019P = allPrd.query('date>=20151019')
#df1019P = allPrd[ allPrd['y']=='2015' and allPrd['date']>='20151019']
df1019PG = df1019P.groupby( level='pid' )
l1019P = df1019PG['l'].min()
il = df1019PG['l'].idxmin()
ld1019P = df1019P.iloc[il]['date']
ld1019P.name='ld1019P'
ld1019P.index=l1019P.index
grpDf = pd.DataFrame(grpDf).join( [pd.DataFrame(l1019P), pd.DataFrame(ld1019P) ] )


dfQ3 = allPrd.query('y==2015' and ('m==7' or 'm==8' or 'm==9'))
#dfQ3 = allPrd[ allPrd['m']=='07' ] + allPrd[ allPrd['m']=='08' ] + allPrd[ allPrd['m']=='09' ] 
#dfQ3 = allPrd[ allPrd['m']=='07' or allPrd['m']=='08' or allPrd['m']=='09' ] 
dfQ3G = dfQ3.groupby( level='pid' )
lQ3 = dfQ3G['l'].min()
il = dfQ3G['l'].idxmin()
ldQ3 = dfQ3.iloc[il]['date']
ldQ3.name='ldQ3'
ldQ3.index=lQ3.index
grpDf = pd.DataFrame(grpDf).join( [pd.DataFrame(lQ3), pd.DataFrame(ldQ3) ] )


pass


#cur.executemany( 'insert into myapp_product(source, code, type, market, name, submarket, masksite) values("dzh", ?, "", ?, ?, ?, ".") ', recLst )
#conn.commit()
#p=Product(source='dzh', code=fLst[0], type='', market=market, name=fLst[1].decode('GBK'), submarket = Submarket(market, fLst[0]), maskSite='.' )


#x = len(prdLst)+ 3
#CellRange('prodDict', 'A4:A%d'%x).value = prdLst

# get through xls plugin
trdStat = []
p = []
o = []


'''
prdDf = pd.DataFrame( {'stat': pd.Series(trdStat), 'p': pd.Series(p), 'o': pd.Series(o), index=prdLst} )
prdDf = pd.DataFrame( {'stat': pd.Series(trdStat), 'p': pd.Series(p), 'o': pd.Series(o), index=prdLst} )


conn = db.connect(r'E:\GitHub\myapp\net\website\django\mysite1\db.sqlite3')
cur = conn.cursor()
cur.execute( "select o from myapp_kdaily_cns where (product_id=281 or product_id=282) and date='2015-09-29'" )
CellRange("M1:M2").value=cur.fetchall()

Cell("M5").value=Cell("P5").value
Cell("M6").formula = "=DPD($A6,P$2)"
#Cell("M6").formula = '=DPD("000089.SZ","LST_PRC_RT")'

#Cell("B2").value = "Hello, World!"
#Cell(3,3).value = "33"


# To use a different worksheet, pass its name as the first argument of Cell/CellRange.
Cell("Sheet1", 2, 1)

# If Sheet1 is active, active_sheet() will return 'Sheet1'
# active_sheet('Sheet2') will set the active sheet to Sheet2.
# If Sheet1 is displayed, display_sheet() will return 'Sheet1'.
# display_sheet('Sheet2') will display Sheet2.

'''


'''
t = time.clock()
allPrd =  pd.DataFrame({})
dfl = []
for subM in ['SHS', 'SZS', 'SZSC', 'SZSZ']:
    for prodId in prdDf[prdDf.submarket==subM].index:
        #pd.read_csv(r'D:\data\histcsv\ths\%s.%s.csv'%(prodId.split('.')[1],prodId), index_col='date')
        x = prodId.split('.')
        #x = pd.read_csv( r'D:\data\histcsv\ths\%s.%s.%s.csv' % (x[1],subM,x[0]) ) #, index_col='Date', encoding='gbk')
        dfl.append( pd.read_csv( r'D:\data\histcsv\ths\%s.%s.%s.csv' % (x[1],subM,x[0]) , index_col=['pid','date'], encoding='gbk') )
allPrd = pd.concat(dfl) #, ignore_index=True)
print('get allPrd time: %.03f' % (time.clock()-t) )
'''
