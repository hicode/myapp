import sqlite3 as db

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

