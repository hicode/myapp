import pandas as pd

from common import *
#import sqlite3 as db
#conn = db.connect(r'D:\data\slowdb\east.sqlite3')
#cur = conn.cursor()
'''
from net.website.django.mysite1.myapp.models import TradeRealTime
from xlwt.Utils import cellrange_to_rowcol_pair
'''

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
x=len(prdDf.code)+1
'''
CellRange('prodDict', 'A2:A%d'%x).value = prdDf.index
CellRange('prodDict', 'B2:B%d'%x).value = prdDf.name
CellRange('prodDict', 'C2:C%d'%x).value = prdDf.code
CellRange('prodDict', 'D2:D%d'%x).value = prdDf.market
CellRange('prodDict', 'E2:E%d'%x).value = prdDf.submarket
'''

t = time.clock()
allPrd =  pd.DataFrame({})
dfl = []
for subM in ['SHS', 'SZS', 'SZSC', 'SZSZ']:
    dfl.append( pd.read_csv( r'D:\data\histcsv\ths\%s.csv' % subM, index_col=['pid', 'y', 'm', 'date'], encoding='gbk') )
    break
allPrd = pd.concat(dfl) #, ignore_index=True)
print('get allPrd time: %.03f' % (time.clock()-t) )

#c930 = allPrd.xs( 20150930, level='date' )
c930 = allPrd.query( "date==20150930" )

df15 = allPrd[ allPrd['o']==2015 ]
df15G = df15.groupby( df15['pid'] )
h15 = df15G['h'].max()
ih = df15G['h'].idxmax()
hd15 = df15.iloc[ih]['date']

df10 = allPrd[ allPrd['y']=='2015' and allPrd['m']=='10']
df10G = df10.groupby( df10['pid'] )
h10 = df10G['h'].max()
ih = df10G['h'].idxmax()
hd10 = df10.iloc[ih]['date']

df1019 = allPrd[ allPrd['y']=='2015' and allPrd['date']>='20151019']
df1019G = df1019.groupby( df1019['pid'] )
l1019 = df1019G['l'].min()
il = df1019G['l'].idxmin()
ld1019 = df1019.iloc[il]['date']


#dfQ3 = allPrd[ allPrd['m']=='07' ] + allPrd[ allPrd['m']=='08' ] + allPrd[ allPrd['m']=='09' ] 
dfQ3 = allPrd[ allPrd['m']=='07' or allPrd['m']=='08' or allPrd['m']=='09' ] 
dfQ3G = dfQ3.groupby( dfQ3['pid'] )
lQ3 = dfQ3G['l'].min()
il = dfQ3G['l'].idxmin()
ldQ3 = dfQ3.iloc[il]['date']

pass

def groupK(dfD, fld):  # conn, 
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
