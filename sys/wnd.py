
#-*- coding: utf-8 -*-  ##设置编码方式

import win32com.client
import win32api,win32gui,win32con
import time

def mouse_move(x,y):
    win32api.SetCursorPos( [x, y] )

def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move( x, y )
        time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

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

pHwnd = appHWnd
for i in range(len(tree)):
    chldHWnd = win32gui.FindWindowEx(pHwnd,None,tree[i]['cls'],tree[i]['cptn'])
    print chldHWnd
    pHwnd = chldHWnd

ccc= win32gui.FindWindowEx(None,None,None,bbb)
print "-----------------------------"

time.sleep(1)
win32gui.SetForegroundWindow(hbtn)
time.sleep(1)

win32gui.PostMessage(hbtn, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
win32gui.PostMessage(hbtn, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

if appHWnd > 0:

    dlg = win32api.FindWindowEx(appHWnd, None, 'Edit', None)#获取appHWnd下第一个为edit控件的句柄

    buffer = '0' *50

    len = win32gui.SendMessage(dlg, win32con.WM_GETTEXTLENGTH)+1 #获取edit控件文本长度

    win32gui.SendMessage(dlg, win32con.WM_GETTEXT, len, buffer) #读取文本

    print buffer[:len-1]

    #虚拟鼠标点击按钮(或者回车)

    btnHWnd = win32api.FindWindowEx(appHWnd, None,'Button', None)

    # win32gui.PostMessage(btnHWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

    # win32gui.PostMessage(btnHWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    win32gui.PostMessage(btnHWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)

    win32gui.PostMessage(btnHWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

    #获取显示器屏幕大小

    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)

    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

"""
#点击窗口button
w=win32ui.FindWindow(clsname,windowtitle)
#b=w.GetDlgItem(窗口id)
b.postMessage(win32con.BM_CLICK)


#关闭窗体
import win32ui
import win32con
wnd=win32ui.FindWindow(classname,None)
wnd.SendMessage(win32con.WM_CLOSE)  #成功！

import win32ui
w=win32ui.FindWindow(classname,'网上股票交易系统5.0')
print w.GetDlgItemText(0xFFFF)  # 获得弹窗里的消息文字
"""

# 最小化窗体
w=win32gui.FindWindow()
win32gui.CloseWindow(w)
