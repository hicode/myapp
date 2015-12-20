# coding=utf-8

import pandas as pd

frml_AHis = '=EM_HQ("%s",Aidx!B1:B32,"1991-01-01","2015-11-28","Period=1,AdjustFlag=1,PriceType=1,Layout1=0,Layout2=0,Order=0,DateType=0,Market=CNSESH")'
frml_HKHis = '=EM_HQ("%s",HKidx!B1:B17,"1991-01-01","2015-11-28","Period=1,AdjustFlag=1,PriceType=1,Layout1=0,Layout2=0,Order=0,DateType=0,Market=CNSESH,type=8,year=2015")'
frml_USHis = '=EM_HQ("%s",USidx!B1:B11,"1991-01-01","2015-11-28","Period=1,AdjustFlag=1,PriceType=1,Layout1=0,Layout2=0,Order=0,DateType=0,Market=CNSESH,type=8,year=2015")'
ACols = ['pid', 'date', 'p', 'o', 'h', 'l', 'c', 'chng', 'chngPc', 'vol', 'amt', 'avg', 'turn', 'stat', 'mrgn', 'tot', 'free1', 'free', 'gugai', 'haiwai', 
         'limit', 'nolimit', 'h', 'b', 'nolimitfree', 'totMktVal', 'shixian', 'diviR', 'ttm', 'psTtm', 'peFuture', 'peForecast', 'peLyr', 'freeMktVal']
HKCols = ['pid', 'date', 'p', 'o', 'h', 'l', 'c', 'chng', 'chngPc', 'vol', 'amt', 'avg', 'turn', 
         'totMktVal', 'diviR', 'ttm', 'psTtm', 'peLyr', 'freeMktVal']
mktDct = {'SH':['A', frml_AHis, r'D:\data\choice\his\sh.csv', ACols],
          'SZ':['A', frml_AHis, r'D:\data\choice\his\sz.csv', ACols],
          'HK':['HK', frml_HKHis, r'D:\data\choice\his\hk.csv', HKCols],
          'A':['US', frml_USHis, r'D:\data\choice\his\a.csv', ],
          'N':['US', frml_USHis, r'D:\data\choice\his\n.csv', ],
          'O':['US', frml_USHis, r'D:\data\choice\his\o.csv', ]}



dzh_idx = ("PREV_CLOSE,CLOSE,OPEN,HIGH,LOW,AVG,CHG,CHG_PCT,ACUM_CHG_PCT,VOL,AMT,TRN_RT,TICK,"
"POSN_RT_OF_IDVL_INVSTR,POSN_RT_OF_MD_INVSTR,POSN_RT_MJR_SHRHLD,POSN_RT_OF_SUP_LRG_SHRHLD,FLOAT_SHRS,MN_POSN,SUP_LRG_SHRHLD_POSN,MJR_SHRHLD_POSN,POSN_OF_MD_INVSTR,POSN_OF_IDVL_INVSTR,RT_OF_MN_POSN,"
"LRG_NET_CAPTL_INF,SUP_LRG_SHRHLD_NET_CAPTL_INF,MJR_SHRHLD_NET_CAPTL_INF,MD_INVSTR_NET_CAPTL_INF,IDVL_INVSTR_NET_CAPTL_INF,MN_NET_CAPTL_INF_OF_FDS,PROP_OF_MN_NET_CAPTL_INF_OF_FDS_TO_AMT,"
"NET_B_AMT_OF_MARG_TDG,NET_S_AMT_OF_SHRT_S,MARG_TDG_BAL,BAL_OF_SHRT_S,"
"PE_TTM,PE_LFY,PE_MRQ,PE_TTM_DED_NRI,PE_LFY_DED_NRI,PE_MRQ_DED_NRI,PB,PS_TTM,PS_LFY,PS_MRQ,PCF_LFY,PCF_TTM,FLOAT_MKT_CAP,TOT_MV,"
"BETA_52W,BETA_24M,BETA_60M,ADJ_BETA_52W,ADJ_BETA_24M,ADJ_BETA_60M,ANNL_VLT_52W,ANNL_VLT_24M,ANNL_VLT_60M,CFCT_OF_DTMN_52W,CFCT_OF_DTMN_24M,CFCT_OF_DTMN_60M,"
"TOT_EQTY_SHRS,FLOAT_A_SHRS,RSTR_A_SHRS,TOT_A_SHRS,FLOAT_B_SHRS,RSTR_B_SHRS,TOT_B_SHRS,FLOAT_H_SHRS,RSTR_H_SHRS,TOT_H_SHRS,OTHR_FLOAT_SHRS,TOT_FLOAT_SHRS,TOT_RSTR_SHRS,NON_TRDB_SHRS_BFF_SHR_REF_BEF_SHR_REF,FREE_FLT_EQTY,"
"DLT_EPS_UPD_NUM_OF_SHRS,BAS_EPS,FULLY_DLT_EPS,BAS_EPS_EX_NRI,FULLY_DLT_EPS_EX_NRI,BVPS,ADJ_BVPS_ED_SHRS_OTSTND,ADJ_BVPS_UPD_NUM_OF_SHRS,UDTRB_PRF_PER_SHR,CAP_RSV_PER_SHR,SUR_RSV_PER_SHR,RTND_EARN_PER_SHR,S_PER_SHR,TOT_REV_PER_SHR,OPR_PRF_PER_SHR,EBITDA_PER_SHR,EBIT_PER_SHR,NET_CF_PER_SHR,CFO_PER_SHR,NET_CFO_PER_SHR,STK_DIV_PER_SHR"
)

dzh_idx_n = ("前收盘价,收盘价,开盘价,最高价,最低价,平均价,涨跌,涨跌幅,累计涨跌幅,成交量,成交金额,换手率,区间成交笔数,"
"散户持仓比,中户持仓比,大户持仓比,超大户持仓比,流通股,主力持仓,超大户持仓,大户持仓,中户持仓,散户持仓,主力持仓比例,"
"大资金净流入额,超大户净流入额,大户净流入额,中户净流入额,散户净流入额,主力资金净流入,主力资金净流入占成交额比," 
"融资净买入额,融券净卖出额,融资余额,融券余额," 
"市盈率TTM,市盈率LFY,市盈率MRQ,市盈率TTM_扣除非经常性损益,市盈率LFY_扣除非经常性损益,市盈率MRQ_扣除非经常性损益,市净率,市销率TTM,市销率LFY,市销率MRQ,市现率LFY,市现率TTM,流通市值,总市值," 
"贝塔系数（52周）,贝塔系数（24个月）,贝塔系数（60个月）,调整贝塔系数（52周）,调整贝塔系数（24个月）,调整贝塔系数（60个月）,年化波动率（52周）,年化波动率（24个月）,年化波动率（60个月）,可决系数（52周）,可决系数（24个月）,可决系数（60个月）," 
"总股本,流通A股,限售A股,A股合计,流通B股,限售B股,B股合计,流通H股,限售H股,H股合计,其他已流通股,流通股合计,限售股合计,未流通股(股改前适用),自由流通股," 
"摊薄每股收益（最新股数）,基本每股收益,稀释每股收益,基本每股收益（扣除）,稀释每股收益（扣除）,每股净资产,调整后每股净资产（期末股数）,调整后每股净资产（最新股数）,每股未分配利润,每股资本公积金,每股盈余公积金,每股留存收益,每股销售收入,每股营业总收入,每股营业利润,每股息税折旧摊销前利润,每股息税前利润,每股净现金流量,每股经营性现金流量,每股经营现金流量净额,每股普通股股利"
)

'''
dfDct = {}
mkt='SH'
dfDct[mkt] = pd.read_csv( mktDct[mkt][2] )
del dfDct[mkt]['Unnamed: 0']
dfDct['SH'] = pd.read_csv( mktDct['SH'][2] )
dfPrd = dfDct['SH'] 
dfPrd['date'] = dfPrd['date'].str[:4] + dfPrd['date'].str[5:7] + dfPrd['date'].str[8:10]
'''

from common import *
#import sqlite3 as db
#conn = db.connect(r'D:\data\slowdb\east.sqlite3')
#cur = conn.cursor()
'''
from net.website.django.mysite1.myapp.models import TradeRealTime
from xlwt.Utils import cellrange_to_rowcol_pair
'''
reload(sys) 
sys.setdefaultencoding( "utf-8" )


def dStr(date):
    return '%04d%02d%02d' % (date.year, date.month, date.day)

def getHist_east():
    dfPrdLst = pd.read_excel(r'E:\GitHub\myapp\xls\choiceGlb.xlsx', 'ahu-lst', index_col=None, na_values=['NA'])
    dfDct = {}
    for mkt  in ['HK']: #'SH', 'SZ', 'HK']: #, 'A', 'N', 'O']:
        dfDct[mkt] = pd.DataFrame( {} )
        if os.path.isfile( mktDct[mkt][2] ):
            dfDct[mkt] = pd.read_csv( mktDct[mkt][2], index_col=['Unnamed: 0'] )
            #del dfDct[mkt]['Unnamed: 0']
            dfDct[mkt].columns = mktDct[mkt][3] #ACols
        dfl = [dfDct[mkt]]
        prdOfMkt = dfPrdLst.query('mkt=="%s"'%mkt)['id']
        shtName = mktDct[mkt][0]
        for prd in prdOfMkt:
            sttDate = '1991-01-01'
            if dfDct[mkt].columns <> []:
                if prd in dfDct[mkt]['pid'].values:
                    dbDate = str( dfDct[mkt].query('pid=="%s"'%prd)['date'].max() )
                    if datetime.now().weekday()==5:
                        latestWDay = datetime.now() + timedelta(days = -1)
                    elif datetime.now().weekday()==6:
                        latestWDay = datetime.now() + timedelta(days = -2)
                    else:
                        latestWDay = datetime.now()
                    if dbDate == '%04d%02d%02d' % (latestWDay.year, latestWDay.month, latestWDay.day):
                        continue
                    sttDate = '%s-%s-01' % (dbDate[:4], dbDate[4:6])
            endDate = '%s-%s-%s' % (datetime.now().year, datetime.now().month, datetime.now().day)
            frml = mktDct[mkt][1].replace('2015-11-28', endDate).replace('1991-01-01', sttDate)
            clear_sheet( shtName )
            Cell(shtName,1,1).formula = frml % prd
            recalc_sheet(shtName)
            Cell(shtName,1,7).value = prd
            Cell(shtName,1,8).value = mkt
            Cell(shtName,1,9).value = latestWDay 
            Cell(shtName,1,10).value = dbDate
            Cell(shtName,1,11).value = sttDate
            Cell(shtName,1,12).value = endDate
            Cell(shtName,1,13).value = 'frml%s'%frml
            time.sleep(5)
            errCntr = 0
            while True:
                statusCell = Cell(shtName,1,2).value 
                if statusCell == None:
                    break
                elif statusCell.strip() == "":
                    break
                elif statusCell.strip() in [u"数据下载中...", u"数据填充中...", u"正在初始化请求..."]:
                    continue
                else:
                    Cell(shtName,1,4).value = statusCell
                    recalc_sheet(shtName)
                    time.sleep(3)
                    errCntr += 1
                    if errCntr<5:
                        continue
                    else:
                        return dfDct

            l = Cell("A4").horizontal
            colNum = len(l)
            l = Cell("B1").vertical
            rowNum = len(l)

            #lastRow = last_cell_in_col(shtName, "A")[2:]

            tblCols = CellRange("A4:AG4").value
            tblCols[0] = 'date'

            tbl = CellRange("A5:AG%s" % rowNum).table
            #tblZip = zip(*tbl)
            #d = {}
            #for i in range(len(tblCols)):
            #    tblCols[i] = tblCols[i].replace(',','_').replace(' ','')
            #    #d[ tblCols[i] ] = tblZip[ i ]
            #dfPrd = pd.DataFrame( d )
            dfPrd = pd.DataFrame( tbl, columns=tblCols )

            '''
            #correctDate = dfPrd['date'].astype("S8")
            #correctDate = correctDate.str.replace(u"数据来源:东方财富Choice数据", 'errordate')
            errDateDf = dfPrd.query('date==u"数据来源:东方财富Choice数据"')
            correctDate = dfPrd['date']

            for i in errDateDf.index:
                preDate = correctDate.iloc[i-1]
                if preDate.weekday()==4:
                    correctDate.iloc[i] = preDate + timedelta(days = 3)
                else:
                    correctDate.iloc[i] = preDate + timedelta(days = 1)
            dfPrd['date'] = correctDate.astype("S8")
            '''
            dfPrd['date'] = dfPrd['date'].astype("S8")

            dfPrd['date'] = dfPrd['date'].str[:4] + dfPrd['date'].str[5:7] + dfPrd['date'].str[8:10]
            dfPrd.insert(0,'pid', prd)
            #save(r'E:\GitHub\myapp\xls\choiceGlb.xlsx')
            #save_copy(r'E:\GitHub\myapp\xls\choiceGlb_t.xlsx')
            #dfPrd = pd.read_excel(r'E:\GitHub\myapp\xls\choiceGlb.xlsx', 'As', index_col=None, na_values=['NA'])
            dfPrd.columns = mktDct[mkt][3] #ACols
            dfPrd.to_csv(r'D:\data\choice\his\%s.%s.csv' % (mkt,prd) )
            dfDct[mkt] = pd.concat( [dfDct[mkt], dfPrd] ).set_index(['pid','date']).sort().reset_index()
            #dfl.append(dfPrd)
        #dfDct[mkt] = pd.concat(dfl)


while True:
    dfDct = getHist_east()
    for mkt in dfDct.keys():
            dfDct[mkt].to_csv( mktDct[mkt][2] )
    time.sleep(30)

