zzzz = " 顶层人控/手工 次层半自动按钮  3层及以下自动 "  

from WindPy import w 
from datetime import *
w.start(showmenu=True) 
w.wsd("600000.SH","open,close", "2010-07-01",datetime.today(), "Fill=Previous") 
w.wsd("600000.SH,600004.SH","low", '20150716', datetime.today(), "Fill=Previous") 
w.tdaysoffset(-1)

# watch_list txt? excel!!! sheet ( watch list / position or both in the same sheet? )
import xlrd
from os.path import join
from xlwt.Workbook import Workbook

name='oil.xlsx'
path='C:\Users\Administrator\Desktop\ib'
data = xlrd.open_workbook(os.path.join(path,name))
table=data.sheet_by_name('0527')

row=table.row_values(0)
col=table.col_values(0)

from xlwt import Workbook
book=Workbook()
sheet1=book.add_sheet('0530')
book.add_sheet('sheet2')
sheet1.write(0,0,'A1')
sheet1.write(0,1,'B1')

book.save('simple2.xls')


import xlwt
import xlrd
from xlutils.copy import copy
from os.path import join

name='oil.xlsx'
path='C:\Users\Administrator\Desktop\ib'

#open existed xls file
oldWb = xlrd.open_workbook(join(path,name), on_demand=True)  #, formatting_info=True
#oldWbS = oldWb.sheet_by_index(0)
newWb = copy(oldWb)
newWs=newWb.add_sheet('150531')

#newWs = newWb.get_sheet(0)
inserRowNo = 0
newWs.write(inserRowNo, 0, "value1")
newWs.write(inserRowNo, 1, "value2")
newWs.write(inserRowNo, 2, "value3")

for rowIndex in range(inserRowNo, oldWbS.nrows):
    for colIndex in range(oldWbS.ncols):
        newWs.write(rowIndex + 1, colIndex, oldWbS.cell(rowIndex, colIndex).value) 
newWb.save('fileName.xls') 
print "save with same name ok" 


import datetime 
datetime.date.today().strftime("%y%m%d") 

# # get watch list from excel 

# type of focus: ( industry/concept,  reason for buying ,  reason for selling , prospect ) 
#                ( last average p with massive trade , last highest p, last lowest p, historical highest p, historical lowest p, minimum daily trading volume, max daily trading volume ) 
#                11 start buying  12 hold to wait profit 13 start to sell 
#                  111 getting loss 122 getting profit 
#                21 waiting chance to buy in (forget these following ?? :: PL of last time  / price of last trade ) 
#                31 waiting: * price fall enough  * holder being tortured enough  * seemed to go to hell   
#                41 reference relative star model signpost?  ( shiyinglv  zongshizhi ) 

# # export to zxg  
# # import 

# get_hist 

# import2DB 

# daily: getDay import2DB 

# analyze  
# # kpi 
# # wave period 

# asset-stat position cash profit debt    
# get account(position) from IB 

