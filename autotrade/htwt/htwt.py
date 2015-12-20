#-*- coding: utf-8 -*-  ##设置编码方式

import win32com.client
import win32api,win32gui,win32con
import time
from PIL import ImageGrab

def mouse_move(x,y):
    win32api.SetCursorPos( [x, y] )

def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move( x, y )
        time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def window_capture(hwnd):
    hwndDC = win32gui.GetWindowDC( hwnd )
    mfcDC = win32gui.CreateDCFromHandle( hwndDC )
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32gui.CreateBitmap()
    MoniterDev = win32api.EnumDisplayMonitors( None, None )
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    print( w, h )
    saveBitMap.CreateCompatibleBitmap( mfcDC, w, h )
    saveDC.SelectObject( saveBitMap )
    saveDC.BitBlt( ( 0, 0 ), ( w, h ) , mfcDC, ( 0, 0 ), win32con.SRCCOPY )
    bmpname = win32api.GetTempFileName( ".", "" )[0] + '.bmp'
    saveBitMap.SaveBitmapFile( saveDC, bmpname )
    return bmpname


im = window_capture()
import PIL
box = ( int( left ), int( top ), int( right ), int( bottom ) )
region = im.crop( box )
region.save( 't.bmp', 'BMP' )


import Image
import sys
from pyocr import pyocr
 
tools = pyocr.get_available_tools()[:]
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
print("Using '%s'" % (tools[0].get_name()))
tools[0].image_to_string(Image.open('test.png'), lang='fra', builder=TextBuilder())



import pytesser
text1 = image_file_to_string( 't.bmp', graceful_errors = True )
print( "\r\nmy char: " )
print( text1 )
from datetime import datetime
s = datetime.now()
s1 = '%02s%02s%02s' % ( s.hour, s.minute, s.second )
rslt = open( "%s.txt" % s1, 'w' )
rslt.write( text1 )


def ocrAcct():
    pass

def buy(code, p, v):
    pass

htwt = u'网上股票交易系统5.0' #此处假设主窗口名为tt
notepad = u'无标题 - 记事本'

appHWnd = win32gui.FindWindow(None, htwt)
wsh = win32com.client.Dispatch( "Wscript.Shell" )
if False == wsh.AppActivate( htwt ):
    pass
rect = win32gui.GetWindowRect(appHWnd)
print(rect)

mouse_click( (rect[0]+rect[2])/2, (rect[1]+rect[3])/2)
time.sleep( 0.1 )
wsh.SendKeys( "{F1}" )
time.sleep( 0.1 )
wsh.SendKeys( "%R" )
time.sleep( 0.1 )
wsh.SendKeys( "002081" )
time.sleep( 0.1 )
wsh.SendKeys( "{ENTER}"  )
time.sleep( 0.1 )
wsh.SendKeys( "%R" )
time.sleep( 0.1 )
wsh.SendKeys( "002375" )
time.sleep( 0.1 )
wsh.SendKeys( "{ENTER}"  )
time.sleep( 0.1 )
wsh.SendKeys( "12.34" )
time.sleep( 0.1 )
wsh.SendKeys( "{ENTER}"  )
time.sleep( 0.1 )
wsh.SendKeys( "100" )
time.sleep( 0.1 )
wsh.SendKeys( "{ENTER}"  )
time.sleep( 0.1 )
wsh.SendKeys( "%y"  )



win32gui.ShowWindow(appHWnd,win32con.SW_SHOWNORMAL)
win32gui.SetActiveWindow(appHWnd)
win32gui.SendMessage(appHWnd, win32con.WM_KEYDOWN, 49, 0)
win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_F3, 0)
time.sleep(0.03)

mouse_click( (rect[0]+rect[2])/2, (rect[1]+rect[3])/2)
time.sleep(0.03)
win32gui.SendMessage(appHWnd, win32con.WM_KEYDOWN, 49, 0)
#win32gui.SetForegroundWindow(appHWnd)

#win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_F1, 0)
time.sleep(0.03)
#win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
time.sleep(0.03)

win32gui.SendMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_F1, 0)
win32gui.SendMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)


for i in range(100000000):
    x=i

win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, ord('r'), 1<<29)
code = '002081'
for c in code:
    win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, ord(c), 0)
win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
p = '123.45'
for c in p:
    win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, ord(c), 0)
win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, 'r', 1<<29)

print appHWnd
print "---------------------------------"
time.sleep(1)

button = u'确定[&S]'
bbb = u'刷新 Firefox'
tree = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'AfxWnd42s'}, {'cptn':'HexinScrollWnd', 'cls':'Afx:400000:0'}, {'cptn':'HexinScrollWnd2', 'cls':'AfxWnd42s'}, {'cptn':None, 'cls':'SysTreeView32'} ]
cncl = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'#32770 (Dialog)'}, {'cptn':'全部选中', 'cls':'Button'} ]
cncl = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'#32770 (Dialog)'}, {'cptn':'撤单', 'cls':'Button'} ]
cncl = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'#32770 (Dialog)'}, {'cptn':'撤最后一笔(V)', 'cls':'Button'} ]
cnclList = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'#32770 (Dialog)'}, {'cptn':'HexinScrollWnd', 'cls':'Afx:400000:0'}, {'cptn':'HexinScrollWnd2', 'cls':'AfxWnd42s'}, {'cptn':'Custom1', 'cls':'CVirtualGridCtrl'} ]
