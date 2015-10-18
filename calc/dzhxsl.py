# coding=utf-8

IdxOffclNLst_rl_Dzh = ['开盘价_实时', '最高价_实时', '最低价_实时', '最新价_实时', '成交量_实时', '成交金额_实时', '买一价_实时', '买一量_实时', '买二价_实时', '买二量_实时', '买三价_实时', '买三量_实时', '买四价_实时', '买四量_实时', '买五价_实时', '买五量_实时', '卖一价_实时', '卖一量_实时', '卖二价_实时', '卖二量_实时', '卖三价_实时', '卖三量_实时', '卖四价_实时', '卖四量_实时', '卖五价_实时', '卖五量_实时', '涨跌_实时', '涨跌幅_实时', '均价_实时', '量比_实时', '委比_实时', '昨收价_实时', '持仓_实时', '结算价_实时', '昨结算_实时']
IdxNLst_rl_Dzh = ['o', 'h', 'l', 'c', 'v', 'a', 'pb1', 'vb1', 'pb2', 'vb2', 'pb3', 'vb3', 'pb4', 'vb4', 'pb5', 'vb5', 'ps1', 'vs1', 'ps2', 'vs2', 'ps3', 'vs3', 'ps4', 'vs4', 'ps5', 'vs5', '涨跌_实时', '涨跌幅_实时', 'average', 'volRatio', '委比_实时', 'p', '持仓_实时', '结算价_实时', '昨结算_实时']
IdxLst_rl_Dzh = ['OPEN_PRC_RT', 'HIGH_PRC_RT', 'LOW_PRC_RT', 'LST_PRC_RT', 'VOL_RT', 'AMT_RT', 'BID_1_PRC_RT', 'BID_1_VOL_RT', 'BID_2_PRC_RT', 'BID_2_VOL_RT', 'BID_3_PRC_RT', 'BID_3_VOL_RT', 'BID_4_PRC_RT', 'BID_4_VOL_RT', 'BID_5_PRC_RT', 'BID_5_VOL_RT', 'ASK_1_PRC_RT', 'ASK_1_VOL_RT', 'ASK_2_PRC_RT', 'ASK_2_VOL_RT', 'ASK_3_PRC_RT', 'ASK_3_VOL_RT', 'ASK_4_PRC_RT', 'ASK_4_VOL_RT', 'ASK_5_PRC_RT', 'ASK_5_VOL_RT', 'CHG_RT', 'CHG_PCT_RT', 'AVG_PRC_RT', 'QTY_RLTV_RT_RT', 'RT_OF_BUY_VOL_TO_SELL_VOL_RT', 'PREV_CLOSE_RT', 'OI_RT', 'STLMT_PRC_RT', 'PREV_STLMT_PRC_RT']

import xlwt


f = xlwt.Workbook()
sh = f.add_sheet(u'dzh')
sh.write(1,0, '600094.SH')
sh.write(0,1, 'LST_PRC_RT')
sh.write(1,1, '=DPD($A2,B$1)')
f.save('testdzh.xlsx')

#写excel
def write_excel():
  f = xlwt.Workbook() #创建工作簿
 
  '''
    创建第一个sheet:
    sheet1
  '''
  sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
  row0 = [u'业务',u'状态',u'北京',u'上海',u'广州',u'深圳',u'状态小计',u'合计']
  column0 = [u'机票',u'船票',u'火车票',u'汽车票',u'其它']
  status = [u'预订',u'出票',u'退票',u'业务小计']
 
  #生成第一行
  for i in range(0,len(row0)):
    sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
 
  #生成第一列和最后一列(合并4行)
  i, j = 1, 0
  while i < 4*len(column0) and j < len(column0):
    sheet1.write_merge(i,i+3,0,0,column0[j],set_style('Arial',220,True)) #第一列
    sheet1.write_merge(i,i+3,7,7) #最后一列"合计"
    i += 4
    j += 1
 
  sheet1.write_merge(21,21,0,1,u'合计',set_style('Times New Roman',220,True))
 
  #生成第二列
  i = 0
  while i < 4*len(column0):
    for j in range(0,len(status)):
      sheet1.write(j+i+1,1,status[j])
    i += 4
 
  f.save('demo1.xlsx') #保存文件
 
if __name__ == '__main__':
  #generate_workbook()
  #read_excel()
  write_excel()
