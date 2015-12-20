# coding=utf-8

###########################################################################################################################################
from pywinauto import application
import time
import win32api,win32gui,win32con

cptn = u'同花顺(v8.50.90)'
appHWnd = win32gui.FindWindow(None, cptn)
print appHWnd
appHWnd = 0x001B11AC
win32gui.ShowWindow(appHWnd,win32con.SW_SHOWMAXIMIZED)
win32gui.SetActiveWindow(appHWnd)
win32gui.SendMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
#win32gui.PostMessage(appHWnd, win32con.WM_KEYDOWN, win32con.VK_F3, 0)
time.sleep(0.03)

#app = application.Application().connect_(title_re = cptn)

'''
appName = "notepad.exe"
appName = u'D:\同花顺软件\同花顺\hexin.exe'
app = application.Application.start( appName )
'''

time.sleep( 1 )
mainDlg = app.top_window_()
time.sleep( 3 )

mainDlg.TypeKeys("00001{ENTER}")
time.sleep( 1 )
mainDlg.TypeKeys("{F5}")
#mainDlg.TypeKeys("{PGDN}")
#win32gui.SendMessage(mainDlg, win32con.WM_KEYDOWN, win32con.SB_PAGEDOWN, 0)
for i in range(3000):
    '''
    time.sleep( 0.2 )
    mainDlg.TypeKeys("%{DOWN}")
    time.sleep( 0.2 )
    mainDlg.TypeKeys("%{DOWN}")
    time.sleep( 0.2 )
    mainDlg.TypeKeys("%{DOWN}")
    time.sleep( 0.2 )
    mainDlg.TypeKeys("%{DOWN}")
    time.sleep( 0.2 )
    mainDlg.TypeKeys("%{DOWN}")
    '''
    time.sleep( 1 )
    mainDlg.TypeKeys("{PGDN}")
    time.sleep( 1 )
    mainDlg.TypeKeys("^{PGDN}")
    time.sleep( 1 )
    mainDlg.TypeKeys("%{PGDN}")
    time.sleep( 1 )
    mainDlg.TypeKeys("+{PGDN}")

#app.notepad.TypeKeys("%FX")
#app.Notepad.MenuSelect(u'帮助->关于记事本'.decode('gb2312'))

top_dlg = app.top_window_()
print top_dlg
about_dlg = app.window_(title_re = u"关于", class_name = "#32770")
print about_dlg
about_dlg.print_control_identifiers()


app.window_(title_re = u'关于“记事本”').window_(title_re = u'确定')

OK = u'确定'
about_dlg[OK].Click()
app[u'关于“记事本”'][u'确定'].Click()



htwt = u'网上股票交易系统5.0' #此处假设主窗口名为tt
notepad = u'无标题 - 记事本'

app = application.Application().connect_(title_re = htwt)
MainDlg=app.top_window_()
tree = [{'cptn':None, 'cls':'AfxMDIFrame42s'}, {'cptn':None, 'cls':'AfxWnd42s'}, {'cptn':'HexinScrollWnd', 'cls':'Afx:400000:0'}, {'cptn':'HexinScrollWnd2', 'cls':'AfxWnd42s'}, {'cptn':None, 'cls':'SysTreeView32'} ]

{'cptn':None, 'cls':None}
{'cptn':None, 'cls':'AfxMDIFrame42s'}
{'cptn':None, 'cls':'#32770 (Dialog)'}
{'cptn':'HexinScrollWnd', 'cls':'Afx:400000:0'}
{'cptn':'HexinScrollWnd2', 'cls':'AfxWnd42s'}
{'cptn':'Custom2', 'cls':'CVirtualGridCtrl'}




















###########################################################################################################################################
#import Image  
from PIL import Image # use pillow instead of PIL

import sys
import pyocr

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'tesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'

imgF = 'c:\\testocrpng.jpg'

txt = tool.image_to_string(
    Image.open( imgF ),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
word_boxes = tool.image_to_string(
    Image.open( imgF ),
    lang=lang,
    builder=pyocr.builders.WordBoxBuilder()
)
line_and_word_boxes = tool.image_to_string(
    Image.open( imgF ), lang=lang,
    builder=pyocr.builders.LineBoxBuilder()
)

# Digits - Only Tesseract
digits = tool.image_to_string(
    Image.open( imgF ),
    lang=lang,
    builder=pyocr.tesseract.DigitBuilder()
)

str = tools[0].image_to_string(Image.open( imgF ), lang='eng', builder=pyocr.builders.TextBuilder())


###########################################################################################################################################

juheKey = 'b78b1b7eb447cd08d581d544d85041ba'
'http://web.juhe.cn:8080/finance/stock/hs?gid=sh601009&key=%s' % juheKey

'''
http://web.juhe.cn:8080/finance/stock/hs?gid=sh601009&key=b78b1b7eb447cd08d581d544d85041ba
http://web.juhe.cn:8080/finance/stock/hs?gid=sz002375&key=b78b1b7eb447cd08d581d544d85041ba

http://web.juhe.cn:8080/finance/stock/hk?gid=hk1211&key=b78b1b7eb447cd08d581d544d85041ba
'''
