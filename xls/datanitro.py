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

#'''
dfX = pd.read_excel(r'E:\GitHub\myapp\xls\del\myview1129.xlsx', 'Sheet4', index_col=None, na_values=['NA'])
topN = 200
dict = {}
cols = dfX.columns[11:]
#cols.reverse()
for col in cols:
    break
    tmp = dfX.sort(col)

    avgH = tmp[['LFY', 'TTM', 'PB', 'xLFY', 'xTTM', 'xPB']].tail(topN)
    avgH.columns = ['h_LFY', 'h_TTM', 'h_PB', 'h_xLFY', 'h_xTTM', 'h_xPB']
    avgH = avgH.sum()/topN

    avgL = tmp[['LFY', 'TTM', 'PB', 'xLFY', 'xTTM', 'xPB']].head(topN)
    avgL.columns = ['l_LFY', 'l_TTM', 'l_PB', 'l_xLFY', 'l_xTTM', 'l_xPB']
    avgL = avgL.sum()/topN

    dict[ str(col) ] = avgH.append( avgL )
#'''

#pd.DataFrame(dict).to_csv(r'D:\data\csvCalc\dailyTopPEB.csv')

#Cell("BB23").value = Cell("BB23").font.color

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
    for subM in ['SZS', 'SZSC', 'SZSZ', 'SHS', 'SHSB', 'SZSB', 'HKS', 'HKSC' ]:
    #for subM in [ 'HKS', 'HKSC' ]:
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
    allPrd['swapRt'] = None
    allPrd['swapRtChng'] = None
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
            swapRtChngL = []
            totShareL = []
            #free = 0
            #tot = 0 
            iGrp = 0
            pFree,free=None,None
            for i in dfWght.index: # for dk in grp:
                #pFree = free #freeShareL += [ grp['freeShare'].iat[ iGrp ] ] * iGrp
                #pTot = tot #totShareL += [ grp['totShare'].iat[ iGrp ] ] * iGrp

                pFree = free
                x, y, date, gift, sell, pSell, bonus, incr, tot, free = dfWght.iloc[i] #, p = dfWght.iloc[i]
                if (grp['date'].tail(1)>=date).values[0]:  # k线数据日期在权息数据日期之后
                    break
                iGrp = grp['date'].index[ grp['date']<date ]  # 除权日之前的K线数据的index
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
                if pFree==None:
                    swapRtChng = 1
                else:
                    swapRtChng = free / ( pFree*(1 + sell + incr + gift) )  # free = newfree + pFree * (1 + sell + incr + gift)

                swapRtChngL += [swapRtChng] * copyLen

            copyLen = len(grp) - len(wghtL)
            wghtL += [wght] * copyLen
            freeShareL += [free] * copyLen
            swapRtChngL += [swapRtChng] * copyLen
            totShareL += [tot] * copyLen
            # grp['wght'][i] =  wght


            #grp['wght'] = wghtL
            #grp['freeShare'] = freeShareL
            #grp['swapRtChngL'] = swapRtChngL
            #grp['totShare'] = totShareL
            allPrd['wght'][pid] = wghtL  #[:len(wghtL)] = wghtL
            allPrd['freeShare'][pid] = freeShareL  #[:len(wghtL)] = freeShareL
            allPrd['swapRtChng'][pid] = swapRtChngL  #[:len(wghtL)] = swapRtChngL
            allPrd['totShare'][pid] = totShareL  #[:len(wghtL)] = totShareL
            #allPrd.to_csv(r"D:\data\csvCalc\allprd1.csv")

    allPrd_divi = allPrd.copy()
    allPrd_divi['o'] = allPrd['o']/allPrd['wght']
    allPrd_divi['h'] = allPrd['h']/allPrd['wght']
    allPrd_divi['l'] = allPrd['l']/allPrd['wght']
    allPrd_divi['c'] = allPrd['c']/allPrd['wght']
    allPrd_divi['p'] = allPrd['p']/allPrd['wght']
    #allPrd_divi['swapRt'] = (allPrd['vol']/allPrd['freeShare']) / 100

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



#'''
allPrdNoDivi = readHistCsv()
allPrdNoDivi, allPrd_divi = calcWght('D:\\data\\weightcsv\\ql\\', allPrdNoDivi)
allPrdNoDivi.to_csv('D:\data\csvCalc\pd.csv')
allPrd_divi.to_csv('D:\data\csvCalc\pd_divi.csv')
#'''

def fgrAllPrd( allPrdK, allPrdKM, allPrdKY, output ): # h15 lPost  hPost at930 l1019P h10m
    allPrdKM.set_index(['pid','y', 'm'], inplace=True)
    allPrdKY.set_index(['pid','y'], inplace=True)
    allPrdK.set_index(['pid','date'], inplace=True)

    HLy = {}
    for i in range(8):
        y = 2008+i
        HLy['H%4d'%y] = allPrdKY.query('y==2008')[['h','hDate']].reset_index().set_index('pid')
        HLy['H%4d'%y].columns = ['y','H%4d'%y,'hDate']
        HLy['L%4d'%y] = allPrdKY.query('y==2008')[['l','lDate']].reset_index().set_index('pid')
        HLy['L%4d'%y].columns = ['y','L%4d'%y,'lDate']
    '''
    H2008 = allPrdKY.query('y==2008')[['h','hDate']].reset_index().set_index('pid')
    H2008.columns = ['y','H2008','hDate']
    L2008 = allPrdKY.query('y==2008')[['l','lDate']].reset_index().set_index('pid')
    L2008.columns = ['y','L2008','lDate']
    L2009 = allPrdKY.query('y==2009')[['l','lDate']].reset_index().set_index('pid')
    L2009.columns = ['y','L2009','lDate']
    L2010 = allPrdKY.query('y==2010')[['l','lDate']].reset_index().set_index('pid')
    L2010.columns = ['y','L2010','lDate']
    L2011 = allPrdKY.query('y==2011')[['l','lDate']].reset_index().set_index('pid')
    L2011.columns = ['y','L2011','lDate']
    L2012 = allPrdKY.query('y==2012')[['l','lDate']].reset_index().set_index('pid')
    L2012.columns = ['y','L2012','lDate']
    L2013 = allPrdKY.query('y==2013')[['l','lDate']].reset_index().set_index('pid')
    L2013.columns = ['y','L2013','lDate']
    L2014 = allPrdKY.query('y==2014')[['l','lDate']].reset_index().set_index('pid')
    L2014.columns = ['y','L2014','lDate']
    H2015 = allPrdKY.query('y==2015')[['h','hDate']].reset_index().set_index('pid')
    H2015.columns = ['y','H2015','hDate']
    '''

    H8 = allPrdKM.query('y==2015 and m==8')[['h','hDate']].reset_index().set_index('pid')
    H8.columns = ['y','m','H8','hDate']

    _H456 = allPrdKM.query('(y==2015 and m==6) or (y==2015 and m==5) or (y==2015 and m==4)')[['h','hDate']]
    __H456 = _H456.groupby(level=0)['h'].max()
    #__H456.name = 'H456'
    H456 = pd.DataFrame({'H456':__H456}).reset_index().set_index('pid')

    _L789 = allPrdKM.query('(y==2015 and m==7) or (y==2015 and m==8) or (y==2015 and m==9) or (y==2015 and m==10)')[['l','lDate']]
    __L789 = _L789.groupby(level=0)['l'].min()
    #__L789.name = 'L789'
    L789 = pd.DataFrame({'L789':__L789}).reset_index().set_index('pid')

    _L1112 = allPrdKM.query('(y==2015 and m==11) or (y==2015 and m==12)')[['l','lDate']]
    __L1112 = _L1112.groupby(level=0)['l'].min()
    #__L1112.name = 'L1112'
    L1112 = pd.DataFrame({'L1112':__L1112}).reset_index().set_index('pid')

    _H10P = allPrdKM.query('(y==2015 and m==10) or (y==2015 and m==11) or (y==2015 and m==12)')[['h','hDate']]
    __H10P = _H10P.groupby(level=0)['h'].max()
    #__H10P.name = 'H10P'
    H10P = pd.DataFrame({'H10P':__H10P}).reset_index().set_index('pid')

    C930 = allPrdK.query('date==20150930')[['c']].reset_index().set_index('pid')
    C930.columns = ['date','C930']
    L820 = allPrdK.query('date==20150820')[['l']].reset_index().set_index('pid')
    L820.columns = ['date','L820']

    rcntKeyLowDay = ['1021', '1103']
    Ldt = {}
    for d in rcntKeyLowDay:
        d = '2015%4d'%d
        _Ldt = allPrdK.query('date==20151021 or date==20151022')[['l']]
        __Ldt = _Ldt.groupby(level=0)['l'].min()
        Ldt['L%4d'%d] = pd.DataFrame({'L%4d'%d:__Ldt}).reset_index().set_index('pid')

    _L1021 = allPrdK.query('date==20151021 or date==20151022')[['l']]
    __L1021 = _L1021.groupby(level=0)['l'].min()
    #__L1021.name = 'L1021'
    L1021 = pd.DataFrame({'L1021':__L1021}).reset_index().set_index('pid')

    _L1103 = allPrdK.query('date==20151102 or date==20151103 or date==20151104')[['l']]
    __L1103 = _L1103.groupby(level=0)['l'].min()
    #__L1103.name = 'L1103'
    L1103 = pd.DataFrame({'L1103':__L1103}).reset_index().set_index('pid')

    _L1116 = allPrdK.query('date==20151113 or date==20151116')[['l']]
    __L1116 = _L1116.groupby(level=0)['l'].min()
    #__L1116.name = 'L1116'
    L1116 = pd.DataFrame({'L1116':__L1116}).reset_index().set_index('pid')

    _L1215 = allPrdK.query('date==20151114 or date==20151115')[['l']]
    __L1215 = _L1215.groupby(level=0)['l'].min()
    #__L1215.name = 'L1215'
    L1215 = pd.DataFrame({'L1215':__L1215}).reset_index().set_index('pid')

    C = allPrdK.query('date==20151119')[['c']].reset_index().set_index('pid')
    C.columns = ['date','C']

    vDf = pd.concat( [ L12[['L12']], L13[['L13']], L14[['L14']], H8[['H8']], C930[['C930']], L820[['L820']], H456, L789, H10P, L1021, L1103, L1116, C ], axis=1, join='outer')
    vDf.to_csv(r'D:\data\csvCalc\vDf%s.csv'%output)
    #vDf = pd.merge(L12,L13,L14,H8,C930,L820,on='pid',how='outer')

    grped = allPrdKM.groupby(level=0) #'pid'
    for pid, group in grped:
        grp = group.reset_index()
        grp['h15'] = p # [:-1] = p
        grp['h15d'] = 1 # pd.Series(1, allPrdKM.index)
        grp['freeShare'] = None
        grp['totShare'] = None

        code,market = pid.split('.')
        iGrp = 0
        h15, h15D, lPost, lPostD, hPost, hPostD, at930, l1019P, l1019PD, h10m, h10mD = [None]*11
        h15, h15D, lPost, lPostD, hPost, hPostD, at930, l1019P, l1019PD, h10m, h10mD = [allPrdKY, None, None, None, None, None, None, None, None, None, None]
        for km in grp.index:
            h15, h15D, lPost, lPostD, hPost, hPostD, at930, l1019P, l1019PD, h10m, h10mD = [None, None, None, None, None, None, None, None, None, None, None]
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

    return allPrd, allPrd_divi

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
'''

t = time.clock()
allPrd =  pd.read_csv( r'D:\data\csvCalc\pdHK_divi.csv', index_col=['pid', 'y', 'm', 'date'], encoding='gbk')
#allPrdKM = pd.read_csv( r'D:\data\csvCalc\pdHK_divi_km.csv', index_col=['pid', 'y', 'm', 'date'], encoding='gbk')
#allPrdKY = pd.read_csv( r'D:\data\csvCalc\pdHK_divi_ky.csv', index_col=['pid', 'y', 'date'], encoding='gbk')

allPrdK = allPrd.sort().reset_index()
allPrdKM = pd.read_csv( r'D:\data\csvCalc\pdHK_divi_km.csv', index_col=['pid', 'date'] ).sort().reset_index()
allPrdKY = pd.read_csv( r'D:\data\csvCalc\pdHK_divi_ky.csv', index_col=['pid', 'date'] ).sort().reset_index()
allPrdView = fgrAllPrd(allPrdK, allPrdKM, allPrdKY, 'HK')

t = time.clock()
allPrd =  pd.read_csv( r'D:\data\csvCalc\pdA_divi.csv', index_col=['pid', 'y', 'm', 'date'], encoding='gbk')
#allPrdKM = pd.read_csv( r'D:\data\csvCalc\pdA_divi_km.csv', index_col=['pid', 'y', 'm', 'date'], encoding='gbk')
#allPrdKY = pd.read_csv( r'D:\data\csvCalc\pdA_divi_ky.csv', index_col=['pid', 'y', 'date'], encoding='gbk')

allPrdK = allPrd.sort().reset_index()
allPrdKM = pd.read_csv( r'D:\data\csvCalc\pdA_divi_km.csv', index_col=['pid', 'date'] ).sort().reset_index()
allPrdKY = pd.read_csv( r'D:\data\csvCalc\pdA_divi_ky.csv', index_col=['pid', 'date'] ).sort().reset_index()
allPrdView = fgrAllPrd(allPrdK, allPrdKM, allPrdKY, 'A')



print('read allPrd csv time: %.03f' % (time.clock()-t) )


def newTrend(curTr, k):
    newTr = {}
    newTr = {'up':not curTr['up'], 'h':None, 'l':None, 'bD':curTr['eD'], 'eD':k.date, 'c':k.c, 'bornStat':True, 'pTr':curTr}
    #newTr.sure = False
    #newTr.date = curTrend.endDate ## ?? k.date
    #newTr.up = not curTrend.up
    if curTr['up'] == True:
        newTr['h'] = curTr['h']
        newTr['l'] = k.l
        #newTr['eD'] = k.lDate
    else:
        newTr['l'] = curTr['l']
        newTr['h'] = k.h
        #newTr['eD'] = k.hDate
        #if K.l < curTrend.l :
        #    pass
    return newTr

def initTrend(k0):
    #1st trend ::              trendDict[prod].append( {Up:'', startD:'', startV:'', endV:'', bornStat:'close'} )  # pTrend    curTrend   IPO Price
    trRec = []
    firstTr={'up':None, 'h':k0.h, 'l':k0.l, 'bD':k0.date, 'eD':k0.date, 'c':k0.c, 'bornStat':False, 'pTr':None}
    # def first trend Up according to o/c price of first K 
    p=k0.p
    if k0.p == None:   # have IPO price
        p=k0.o
    if k0.c>p:     # no change means fall  
        firstTr['up'] = True
        #firstTr['eD'] = k0.hDate
    else:
        firstTr['up'] = False
        #firstTr['eD'] = k0.lDate
    trRec.append( firstTr )
    return trRec

def newMax(tr, k):
    if tr['up']==True:
        tr['h'] = k.h
        #tr['eD'] = k.hDate
    else:
        tr['l'] = k.l
        #tr['eD'] = k.lDate
    tr['eD'] = k.date
    if tr['bornStat']:
        if ( tr['up']==True and k.h>tr['pTr']['h']) or (tr['up']==False and k.l<tr['pTr']['l']):
            tr['bornStat'] = False

                    #elif k.l < sureTr['l']:  # newTr matured and become sureTr, old sureTr closed(keep in list and not referred by sureTr variable again at this day
                    #    newTr['bornStat'] = False
                    #    sureTr['eD'] = k.date
                    #    sureTr = newTr

        if ( tr['h'] / tr['l'] > 1.7 ) or ( tr['eD'] - tr['bD'] > 400 and tr['h'] / tr['l'] > 1.5):  # tr mature after enough space and space/time:
            #sureTr['bornStat']='close'
            #tr['pTr']['eD'] = k.date
            tr['bornStat'] = False
            #tr['pTr'] = tr


def _closeOldSureTr(newTr, k):
    newTr['bornStat'] = False
    sureTr = newTr
    if tr['up']==True:
        tr['h'] = k.h
        tr['eD'] = k.hDate
    else:
        tr['l'] = k.l
        tr['eD'] = k.lDate

#'''
def _getTrend(dfM):
    trendDict = {}
    grped = dfM.groupby('pid')  #level=0) #'pid'
    for prod, group in grped:    #for prod in dfM['pid']:
        pK=group.iloc[0]  # dfM[prod][0]
        trRec = initTrend( pK ) 
        trendDict[prod] = trRec
        #sureTr = trRec[0]  # latest sure trend
        newTr = trRec[0]  # newTr is latest trend, newTr may be not sure, i.e., it is may dead and become a period of sureTr. 
        # newTr == sureTr means max distance is continue increasing and no withdraw until latest day.   i.e., l or h of today is new max distance
        for i in range(len(group)-1): #for k in group[1:]: # dfM[prod][1:]:
            k = group.iloc[i+1]
            # should not: newTr['eD'] = k.date
            newTr['c'] = k.c
            if newTr['bornStat']:
                if newTr['up'] ==  False: # newtr is fall recent
                    if k.h > newTr['pTr']['h']:  # newTr dead, previous trend (sureTr) continue to grow
                        newMax(newTr['pTr'], k)
                        newTr = newTr['pTr']
                        trRec.pop()
                        continue
                    #elif k.l < sureTr['l']:  # newTr matured and become sureTr, old sureTr closed(keep in list and not referred by sureTr variable again at this day
                    #    newTr['bornStat'] = False
                    #    sureTr['eD'] = k.date
                    #    sureTr = newTr
                    #    newMax(newTr, k)
                    elif k.l < newTr['l']:
                        newMax(newTr, k)
                else:                # newtr is up trend
                    if k.l < newTr['pTr']['l']:  # newTr dead, previous trend (sureTr) continue to grow
                        newMax(newTr['pTr'], k)
                        newTr = newTr['pTr']
                        trRec.pop()
                        continue
                    #elif k.h > sureTr['h']:  # newTr matured and become sureTr, old sureTr closed(keep in list and not referred by sureTr variable again at this day
                    #    newTr['bornStat'] = False
                    #    sureTr['eD'] = k.date
                    #    sureTr = newTr
                    #    newMax(newTr, k)
                    elif k.h > newTr['h']:
                        newMax(newTr, k)
                if ( (newTr['h']-newTr['l']) / newTr['l'] > 1.5 ) or ( newTr['eD'] - newTr['bD'] > 200 and (newTr['h']-newTr['l']) / newTr['l'] > 1.25):  # newTr mature after enough space and space/time:
                    #sureTr['bornStat']='close'
                    newTr['pTr']['eD'] = k.date
                    newTr['bornStat'] = False
                    newTr['pTr'] = newTr
            else:  # sure2new or sureContinue
                if newTr['up'] ==  True: # up trend
                    if k.h > newTr['h']:
                        newMax(newTr, k)
                    if k.c < k.p:  # withdraw born new trend
                        newTr = newTrend(newTr, k) # newTr is the same with sureTr before call return
                        trRec.append( newTr )
                else:                # fall trend
                    if k.l < newTr['l']:
                        newMax(newTr, k)
                    if k.c > k.p:  # withdraw born new trend
                        newTr = newTrend(newTr, k) # newTr is the same with sureTr before call return
                        trRec.append( newTr )
        break
    return trendDict
#'''

def getTrend(dfM):
    trRec = [] #trendDict = {}
    grped = dfM.groupby('pid')  #level=0) #'pid'
    for prod, group in grped:    #for prod in dfM['pid']:
        pK=group.iloc[0]  # dfM[prod][0]
        t = initTrend( pK ) 
        #trendDict[prod] = trRec
        newTr = t[0]  # newTr is latest trend, newTr may be not sure, i.e., it is may dead and become a period of sureTr.
        newTr['pid'] = prod
        trRec += t 
        # newTr == sureTr means max distance is continue increasing and no withdraw until latest day.   i.e., l or h of today is new max distance
        for i in range(len(group)-1): #for k in group[1:]: # dfM[prod][1:]:
            k = group.iloc[i+1]
            newTr['c'] = k.c
            #if k.date>=19920301:
            #    xxxx=1
            if newTr['bornStat']:
                if newTr['up'] ==  False: # newtr is fall recent
                    if k.h > newTr['pTr']['h']:  # newTr dead, previous trend (sureTr) continue to grow
                        newTr = newTr['pTr']
                        newTr['c'] = k.c
                        newMax(newTr, k)
                        trRec.pop()
                        continue
                    elif k.l < newTr['l']:
                        newMax(newTr, k)
                else:                # newtr is up trend
                    if k.l < newTr['pTr']['l']:  # newTr dead, previous trend (sureTr) continue to grow
                        newTr = newTr['pTr']
                        newTr['c'] = k.c
                        newMax(newTr, k)
                        trRec.pop()
                        continue
                    elif k.h > newTr['h']:
                        newMax(newTr, k)
            else:  # sure2new or sureContinue
                if newTr['up'] ==  True: # up trend
                    if k.h > newTr['h']:
                        newMax(newTr, k)
                    if k.c < k.p:  # withdraw born new trend
                        newTr = newTrend(newTr, k) # newTr is the same with sureTr before call return
                        newTr['pid'] = prod
                        trRec.append( newTr )
                else:                # fall trend
                    if k.l < newTr['l']:
                        newMax(newTr, k)
                    if k.c > k.p:  # withdraw born new trend
                        newTr = newTrend(newTr, k) # newTr is the same with sureTr before call return
                        newTr['pid'] = prod
                        trRec.append( newTr )
        #break
    return trRec #trendDict
#'''



allPrdK = pd.read_csv( r'D:\data\csvCalc\pdA_divi.csv', index_col=['pid', 'date'] ).sort().reset_index()


trendDict = getTrend( allPrdK )
#pd.DataFrame( trendDict['000001.SZ'] ).to_csv(r'd:\data\csvCalc\tr.csv')
pd.DataFrame( trendDict ).drop('pTr', axis=1).to_csv(r'd:\data\csvCalc\tr1107.csv')  #pd.DataFrame( trendDict ).pop('pTr').to_csv(r'd:\data\csvCalc\tr.csv')


allPrd = allPrd.query('y==2015 or y==2014') # or y==2013 or y==2012')  # allPrd.xs('000001.SZ',level='pid')
#allPrdK = allPrdK.query('y==2015 or y==2014 or y==2013 or y==2012 or y==2011 or y==2010 or y==2009 or y==2008 or y==2007 or y==2006 or y==2005 or y==2004 or y==2003') # or y==2013 or y==2012')
allPrdK = allPrdK.query('y==2015')
allPrdKY = allPrdK.query('y==2015')



prdDf = getEastPrdLst()
x=len(prdDf.code)+1

'''
CellRange('prodDict', 'A2:A%d'%x).value = prdDf.index
CellRange('prodDict', 'B2:B%d'%x).value = prdDf.name
CellRange('prodDict', 'C2:C%d'%x).value = prdDf.code
CellRange('prodDict', 'D2:D%d'%x).value = prdDf.market
CellRange('prodDict', 'E2:E%d'%x).value = prdDf.submarket
'''



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
