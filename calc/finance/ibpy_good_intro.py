#!/usr/bin/env python
from time import sleep

# LOAD the ib.ext and ib.opt Libraries
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message

posList=[]
accStat=[]
svrRplyStruct = ["key", "value", "currency", "accountName"]

# DEFINE a basic function to capture error messages
def error_handler(msg):
    print "Error", msg

# DEFINE a basic function to print the "raw" server replies
def replies_handler(msg):
    print "Server Reply:", msg
    accStat.append(msg)

# DEFINE a basic function to print the "parsed" server replies for an IB Request of "Portfolio Update" to list an IB portfolio position
def print_portfolio_position(msg):
    print "Position:", msg.contract.m_symbol, msg.contract.m_localSymbol, msg.position, msg.marketPrice, msg.contract.m_currency, msg.contract.m_secType
    s={}
    s['m_symbol']=msg.contract.m_symbol
    s['m_localSymbol']=msg.contract.m_localSymbol
    s['position']=msg.position
    s['marketPrice']=msg.marketPrice
    s['m_currency']=msg.contract.m_currency
    s['m_secType']=msg.contract.m_secType

    s['averageCost']=msg.averageCost
    s['marketValue']=msg.marketValue
    s['unrealizedPNL']=msg.unrealizedPNL
    s['realizedPNL']=msg.realizedPNL
    posList.append(s)

# Main code - adding "if __name__ ==" is not necessary

# Create the connection to IBGW with client socket id=1234
ibgw_conChannel = ibConnection(port=7496) #,clientId=1234)   #port=4001
ibgw_conChannel.connect()

# Map server replies for "Error" messages to the "error_handler" function
ibgw_conChannel.register(error_handler, 'Error')

# Map server replies to "print_portfolio_position" function for "UpdatePortfolio" client requests
ibgw_conChannel.register(print_portfolio_position, 'UpdatePortfolio')

# Map server "raw" replies to "replies_handler" function for "UpdateAccount" client requests
ibgw_conChannel.register(replies_handler, 'UpdateAccountValue')

#from ib.ext.Order import Order
#x=ibgw_conChannel.reqAllOpenOrders()


# Make client request for AccountUpdates (includes request for Portfolio positions)
ibgw_conChannel.reqAccountUpdates(1, '')

# Stop client request for AccountUpdates
ibgw_conChannel.reqAccountUpdates(0, '')

##### !!! todo list 
task = '''request all pending order status '''
historicalTrade = ''''''

sleep(5)

# Disconnect - optional
print 'disconnected', ibgw_conChannel.disconnect()

# "Position:", msg.contract.m_symbol, msg.contract.m_localSymbol, msg.position, msg.marketPrice, msg.contract.m_currency, msg.contract.m_secType
colNameLst = ["m_symbol", "m_localSymbol", "position", "marketPrice", "m_secType", "m_currency", 'averageCost', 'marketValue', 'unrealizedPNL', 'realizedPNL'] #, "exchange"]

name='oil.xlsx'
path='C:\Users\Administrator\Desktop\ib'

import datetime
todayStr = datetime.date.today().strftime("%y%m%d")


todotask = """ content such as formatting_info and picture can not be used !!!!!!!! """  #, formatting_info=True

# export account data of IB to excel
def exportAcct2NewXls():
    import xlrd
    from xlutils.copy import copy
    from os.path import join

    #open existed xls file
    oldWb = xlrd.open_workbook(join(path,name), on_demand=True)    #, formatting_info=True
    #oldWbS = oldWb.sheet_by_index(0)
    newWb = copy(oldWb)

    sheetAcct=newWb.add_sheet(todayStr+'Acct')
    row=0
    col=0
    for colName in svrRplyStruct:
        sheetAcct.write(row, col, colName)
        col=col+1
    for data in accStat:
        row=row+1
        col=0
        for colName in svrRplyStruct:
            sheetAcct.write(row, col, data.__getattribute__(colName))
            col=col+1

    sheetPos=newWb.add_sheet(todayStr+'Pos')
    row=0
    col=0
    for colName in colNameLst:
        sheetPos.write(row, col, colName)
        col=col+1
    for data in posList:
        row=row+1
        col=0
        for colName in colNameLst:
            sheetPos.write(row, col, data[colName])
            col=col+1

    newWb.save(todayStr + '.xls') #join(path, todayStr + name))
    newWb.save( join(path, todayStr + '.xls' ) ) #name))

watchList = []

def importWatchListFromSelFile():
    import struct 
    
    fSel=r'D:\zxg.sel' 
    fp=open(fSel) 
    lines1=fp.readlines()
    lines=lines1[0].split('\x07')
    buf=struct.pack('<H',len(lines)-1) 
    for ln in lines[1:]:
     # xb1--HK stock   x14--sh?  $--sz x11--sh stock
     if ln[1]=='6': 
      #buf=struct.pack('<H6c',7*255+11,ln[1:].strip()) 
      buf=struct.pack('<H6s',1*16*256+1*256+7,ln[1:].strip().encode()) 
     else: 
      buf=struct.pack('<H6s',2*16*256+1*256+7,ln[1:].strip().encode()) 
    
    fpSel.close() 

def importWatchListFromBlkFile():
    import struct 
    
    fBlk=r'D:\zxg.blk' 
    fp=open(fBlk) 
    lines1=fp.readlines()
    lines=lines1[0].split('\x00\x12')
    buf=struct.pack('<H',len(lines)-1) 
    #fpSel.write(buf) 
    for ln in lines[1:]:
     # USZ USH UHK 
     if ln[1]=='6': 
      #buf=struct.pack('<H6c',7*255+11,ln[1:].strip()) 
      buf=struct.pack('<H6s',1*16*256+1*256+7,ln[1:].strip().encode()) 
      #fpSel.write(buf) 
     else: 
      buf=struct.pack('<H6s',2*16*256+1*256+7,ln[1:].strip().encode()) 
      #fpSel.write(buf) 
    
    fBlk.close() 

#importWatchListFromSelFile()

#importWatchListFromBlkFile()

def updateAcctXls():
    import win32com.client
    xlsApp=win32com.client.Dispatch("Excel.Application")
    xlsApp.Visible=False 
    xlsBook=xlsApp.Workbooks.Open(r'C:\\temp\\mysheet0627.xls')  #"C:\Users\Administrator\Desktop\ib\rec\150612.xls")
    xlsSheetPos=xlsBook.Sheets("150612Pos")
    var="20:20"
    xlsSheetPos.Range(var).Insert()
    xlsSheetPos.Range("7:7").Delete()
    #??xlsSheetPos.Range("A:A").Insert()
    xlsBook.Save() #SaveAs(Filename='C:\\temp\\mysheet0627.xls') 
    ttt=xlsSheetPos.Range("1:3").Copy()
    xlsSheetPos.Range("10:10").Insert()
    #??ttt1=xlsSheetPos.Range("A:A").Copy()
    #??xlsSheetPos.Range("C:C").Insert()
    xlsBook.SaveAs(Filename='C:\\temp\\mysheet0627.xls') 
    xlsBook.Close(SaveChanges=0)
    
    r=xlsSheetPos.Rows(1)
    sel=r.Select().insert(Shift='xlDown')
    sel.insert()
    rv=r.Value
    xxx=xlsSheetPos.Rows(1).insert
    xlsBook.SaveAs(Filename='C:\\temp\\mysheet0627.xls') 
    xlsBook.Close(SaveChanges=0)
    rs=xlsSheetPos.UsedRange.Rows
    # don't use this bad idea: delimiterMark = 'ppp'
    titleKeys=('m_symbol', 'm_localSymbol', 'position', 'marketPrice', 'm_secType', 'm_currency', 'averageCost', 'marketValue', 'unrealizedPNL', 'realizedPNL')
    for rowN in range(1, 1+len(rs.rows)):
        for colN in range(1, 1+len(rs.columns)):
            val = xlsSheetPos.Cells(rowN, colN).Value 
            if val == None:
                continue
            elif val == 'm_symbol':
                tmp = xlsSheetPos.Range( xlsSheetPos.Cells(rowN, colN), xlsSheetPos.Cells(rowN, colN+9))
                tmp.InsertAfter()
                tmpVal = tmp.Value
                if  xlsSheetPos.Cells(rowN, colN+1).Value == 'm_localSymbol':  #tmp == titleKeys:
                    xlsSheetPos.Rows(rowN).insert
                    #xlsBook.Save()
                    xlsBook.SaveAs(Filename='C:\\temp\\mysheet.xls') 
                    xlsBook.Close(SaveChanges=0)
                    return
            else:
                break
    # xlsSheetAcct=xlsBook.Sheets("150612Acct") 


exportAcct2NewXls()

updateAcctXls()

def test_004(connection, options):
    connection.reqAllOpenOrders()
    connection.reqAutoOpenOrders(True)
    connection.reqOpenOrders()
    connection.reqExecutions(0, exec_filter(options.clientid))


'''''
################ output
Server Version: 59
TWS Time at connection:20131108 18:55:57 ICT
Server Reply: <updateAccountValue key=AccountCode, value=XXXX, currency=None, accountName=XXXX>
....
Server Reply: <updateAccountValue key=TradingType-S, value=STKNOPT, currency=None, accountName=XXXX>
Server Reply: <updateAccountValue key=UnrealizedPnL, value=-9765.22, currency=BASE, accountName=XXXX>
Server Reply: <updateAccountValue key=UnrealizedPnL, value=-9765.22, currency=USD, accountName=XXXX>
Server Reply: <updateAccountValue key=WarrantValue, value=0.00, currency=BASE, accountName=XXXX>
Server Reply: <updateAccountValue key=WarrantValue, value=0.00, currency=USD, accountName=XXXX>
Server Reply: <updateAccountValue key=WhatIfPMEnabled, value=true, currency=None, accountName=XXXX>
Position: HTS 50 17.3999996 USD STK
Position: MITT 70 16.1100006 USD STK
Position: MTGE 50 19.7800007 USD STK
Position: NYMT 100 6.6199999 USD STK
Position: REM 130 11.85999965 USD STK
Position: STWD 50 25.94000055 USD STK
Position: WMC 50 15.98999975 USD STK








######################## In the following Python example we will write a simple SELL order for 100 shares in GTAT @ 11
# LOAD the ib.ext and ib.opt Libraries
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message

# DEFINE a basic function to capture error messages
def error_handler(msg):
    print "IB: Server Error = ", msg

# DEFINE a basic function to capture all server replies
def all_replies_handler(msg):
    print "IB: Server Response = ", msg.typeName, msg

# Main code

# Create the connection to IBGW with client socket id=123
# using a different method than ibConnection
ibgw_conTradeChannel=Connection.create(port=4001,clientId=123)
ibgw_conTradeChannel.connect()

# Map server replies for "Error" messages to the "error_handler" function
ibgw_conTradeChannel.register(error_handler, 'Error')

# Map all server replies to "all_replies_handler"
# Use typeName to distinguish between the different message types
# This is easier than registering different actions for different messages
ibgw_conTradeChannel.registerAll(all_replies_handler)

# Create a global OrderID for simplicity
# It will be submitted to the IB Server for executing the trade
# To be incremented for the next trade with calls to the IB Server
newOrderID=1

# Create a contract object
# Update the parameters to be sent to the Market Order request
order_ticker = Contract()
order_ticker.m_symbol = 'GTAT'
order_ticker.m_secType = 'STK'
order_ticker.m_exchange = 'SMART'
order_ticker.m_primaryExch = 'SMART'
order_ticker.m_currency = 'USD'
order_ticker.m_localSymbol = 'GTAT'

# Create an order object
# Update the parameters to be sent to the Market Order request
order_desc = Order()
order_desc.m_minQty = 100
order_desc.m_lmtPrice = 11.00
order_desc.m_orderType = 'LMT'
order_desc.m_totalQuantity = 100
order_desc.m_action = 'SELL'

# Send the Market Order request
ibgw_conTradeChannel.placeOrder(newOrderID, order_ticker, order_desc)

print 'disconnected', ibgw_conTradeChannel.disconnect()



####################### The Output will be something like this:
Server Version: 59
TWS Time at connection:20131109 22:01:26 ICT
IB: OrderID = 
>>> 4
IB: Server Response = nextValidId <nextValidId orderId=4>
IB: Server Response = error <error id=5, errorCode=399, errorMsg=Order Message:
Warning: your order will not be placed at the exchange until 2013-11-11 09:30:00 US/Eastern>
IB: Server Response = openOrder <openOrder orderId=5, contract=<ib.ext.Contract.Contract object at 0x012C3C90>, order=<ib.ext.Order.Order object at 0x012C3BB0>, 
orderState=<ib.ext.OrderState.OrderState object at 0x012C3A50>>
IB: Server Response = orderStatus <orderStatus orderId=5, status=PreSubmitted, filled=0, remaining=100, 
avgFillPrice=0.0, permId=XXXXXX, parentId=0, lastFillPrice=0.0, clientId=123, whyHeld=None>





################ Here what I did to manage OrderID in IB:
from ib.opt import ibConnection, Connection, message

def handle_order_id(msg):
    global newOrderID
    newOrderID = msg.orderId

# Main code

# Create the connection to IBGW with client socket id=123
# ibConnection = Connection.create
# ibgw_conTradeChannel = ibConnection(port=4001,clientId=123)
ibgw_conTradeChannel = Connection.create(port=4001,clientId=123)
ibgw_conTradeChannel.connect()

# Handle Order ID sent by Server
ibgw_conTradeChannel.register(handle_order_id, 'NextValidId')

# Receive the new OrderID sequence from the IB Server
ibgw_conTradeChannel.reqIds(0)

# Print the new OrderID that was sent by IB
print "This is the new OrderID sent by IB Server:", newOrderID

print 'disconnected', ibgw_conTradeChannel.disconnect()



'''''