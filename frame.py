# coding=utf-8
#-*- coding utf8 -*-
import time
import datetime
import win32com.client
import os
from sgmllib import SGMLParser
import urllib
#import win32gui, win32ui, win32con, win32api 

class WebTool( object ):
    def soap():
        pass
    def googleSearch( self ):
        pass

    @classmethod
    def checkServer( cls, siteAddr ):
        # ping siteAddr
        return

class NetTool( object ):
    @classmethod
    def ping ( cls, ip ):
        try:
            cmd = 'ping %s -n 3 -w 2000' % ( ip )
            ret = os.system( cmd )
            if ret == 0:
                print '%s is alive' % ( ip )
                return True
            else:
                print '%s is not alive' % ( ip )
                return False
            return True
        except:
            return False

    @classmethod
    def ping1 ( i, q ):
        while True:
            ip = q.get()
            cmd = 'ping %s -c 1' % ( ip )
            # print 'thread %s ping %s'%(i,ip)
            ret = subprocess.call( cmd, shell = True, stdout = open( '/dev/null', 'w' ) )
            if ret == 0:
                print '%s is alive' % ( ip )
            else:
                print '%s is not alive' % ( ip )
            q.task_done()

###########################################################################
#collect data periodically
###########################################################################

def window_capture():
    hwnd = 0
    hwndDC = win32gui.GetWindowDC( hwnd )
    mfcDC = win32ui.CreateDCFromHandle( hwndDC )
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
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

# # copy windows area of each product displayed on window one by one

# # use pytesser to change image to text

# # analyse text and construct record data of trade info

# # veriy data

# # save trade info to db


#拷贝指定窗口区域屏幕


# GUI常用操作模拟
#切换到指定程序窗口
def SetTopAppW( appName ):
    pass

#最大化
def MaximizeAppW():
    pass

#鼠标左键点击指定位置

#鼠标左键双击指定位置

#鼠标右键点击指定位置

#鼠标左键从指定位置按下拖动到指定位置后释放


###########################################################################
# automatically calc indexes and judge trend and chance every half second
###########################################################################

# trigger autotrade while some condition occured



###########################################################################
# autotrade
###########################################################################

# # trade channel test
# # network test
# # server test
# # realtime data test
# # time check


###########################################################################
#indexes calc colletion
###########################################################################
#BOLL

#MA

###########################################################################
#autotrade strategy
###########################################################################


###########################################################################
#system safety, insteady
###########################################################################
#system check
#strategy test




###########################################################################
# collect data automatically from internet
###########################################################################
def waitWin( WinName, seconds ):
    try:
        wsh = win32com.client.Dispatch( "Wscript.Shell" )
        i = 0
        while False == wsh.AppActivate( '%s' % WinName ):
            time.sleep( 1 )
            i = i + 1
            if i > seconds:
                print( 'overtime:%d' % seconds )
                return False
        return True
    except:
        print( 'exception in waitWin' )
        return False

def copy4Paste( fn ):
    try:
        wsh = win32com.client.Dispatch( "Wscript.Shell" )
        wsh.run( r'notepad%s' % fn )
        tmp = fn.split( '\\' )
        if not waitWin( tmp[-1], 30 ):
            print( '%s wind not found' % tmp[-1] )
            return False
        wsh.SendKeys( "^a" )
        wsh.SendKeys( "^c" )
        wsh.SendKeys( "%{F4}" )
        return True
    except:
        print( 'exception in copy4Paste' )
        return False

def SavePaste( fn ):
    try:
        wsh = win32com.client.Dispatch( "Wscript.Shell" )
        wsh.run( r'notepad%s' % fn )
        tmp = fn.split( '\\' )
        if not waitWin( tmp[-1], 30 ):
            print( '%s wind not found' % tmp[-1] )
            return False
        wsh.SendKeys( "^v" )
        wsh.SendKeys( "^s" )
        wsh.SendKeys( '{ENTER}' )
        wsh.SendKeys( "%{F4}" )
        time.sleep( 2 )
        return True
    except:
        print( 'exception in SavePaste' )
        return False

def CheckAndTrim( fn ):
    '''
    TAG_DATASTART0 = '权证交易公开信息 '
    TAG_NODATA = '没有发现符合条件的文本 '
    TAG_DATASTART1 = '深圳证券市场权证交易公开信息'
    TAG_DATASTART2 = '(%s年%02d月%02d日)'%( .year, .month, .day )
    TAG_DATASTART3 = '--------------------------------------------------------------------------------'
    '''
    try:
        date = [fn[-9:-5], fn[-5:-3], fn[-3:-1]]
        TAGS = ['权证交易公开信息',
                      '没有发现符合条件的文本', '深圳证券市场权证交易公开信息',
                      '(%s年%s月%s日)' % ( date[0], date[1], date[2] ),
                      '--------------------------------------------------------------------------------']
        f1 = open( fn )
        f2 = open( '%sOK' % fn, 'w' )
        idx_tag = 0
        for ln in f1:
            #print(ln)
            if idx_tag < 5:
                if ln.strip().find( TAGS[idx_tag] ) > -1:
                    idx_tag += 1
                    if idx_tag == 2:
                        print( 'no data %s' % fn )
                        f1.close()
                        f2.close()
                        return 0
                elif idx_tag == 1:
                    if ln.strip().find( TAGS[idx_tag + 1] ) > -1:
                        idx_tag += 2
            else:
                if ln.strip() != '':
                    f2.write( ln )
        if idx_tag < 5:
            print( 'invalid format: %s' % fn )
            f1.close()
            f2.close()
            return - 1
        f1.close()
        f2.close()
        return 1
    except:
        f1.close()
        f2.close()
        print( 'exception in CheckAndTrim' )
        return - 1


# # http://www.szse.cn/main/disclosure/news/qzjygkxx/
# # http://www.niugoo.com/detail-flash.htm?stock=600795
def getSzQzInfo( date ):
    try:
        print( 'get %s' % date )
        if not copy4Paste( r'.\data\1.txt' ):  #wsh.SendKeys("查询日期")
            print( 'copy4Paste fail: %s' % r'.\data\1.txt' )
            return False
        wsh = win32com.client.Dispatch( "Wscript.Shell" )
        wsh.run( r"C:\Progra~1\Intern~1\iexplore.exe" )
        if not waitWin( 'Microsoft Internet Explorer', 30 ):
            print( 'waitWin Fail: %s' % 'Microsoft Internet Explorer' )
            return False
        wsh.SendKeys( "%D" )
        wsh.SendKeys( r"http://www.szse.cn/main/disclosure/news/qzjygkxx/" )
        wsh.SendKeys( "{ENTER}" )
        time.sleep( 8 )
        time.sleep( 1 )
        wsh.SendKeys( "^{END}" )
        time.sleep( 1 )
        wsh.SendKeys( "^{HOME}" )
        time.sleep( 1 )
        wsh.SendKeys( "^f" )
        time.sleep( 1 )
        wsh.SendKeys( "^v" )
        wsh.SendKeys( "{ENTER}" )
        time.sleep( 1 )
        wsh.SendKeys( "{ESC}" )
        wsh.SendKeys( "{TAB}" )
        wsh.SendKeys( "%s" % date )
        wsh.SendKeys( "{ENTER}" )
        time.sleep( 5 )
        wsh.SendKeys( "{TAB}" )
        wsh.SendKeys( "^a" )
        wsh.SendKeys( "^c" )
        wsh.SendKeys( "%{F4}" )
        tmp = date.split( '-' )
        fn = r'.\data\szqz\%s%s%s_' % ( tmp[0], tmp[1], tmp[2] )
        f = open( fn, 'w' )
        f.close()
        if not SavePaste( fn ):
            print( 'SavePaste fail: %d' % fn )
            return False
        # check data
        if - 1 == CheckAndTrim( fn ):
            print( 'CheckAndTrim fail: %s' % fn )
            return False
        return True
    except:
        print( 'exception in getSzQzInfo' )
        return False


def AnalyseAndImport( fn ):
    TAGS = ['代码:',
                 '成交数量:',
                 '成交金额:',
                 '买入金额最大的前5名',
                 '卖出金额最大的前5名',
                 '营业部或交易单元名称',
                 '买入金额(元)',
                 '卖出金额(元)',
                 '--------------------------------------------------------------------------------'
                ]
    try:
        f = open( fn )
        idx_tag = 0
        for ln in f:
            ele = ln.split()
            if x:
                pass
        f.close()
        return True
    except:
        print( 'except in AnalyseAndImport' )
        return False


def DigSzQzHisData():
    try:
        # loop workday since 2005-01-01
        startD = datetime.date( 2005, 1, 1 )
        d1 = datetime.date( 2005, 1, 2 ) - datetime.date( 2005, 1, 1 )
        startD = startD - d1
        td = datetime.datetime.now()
        OneDay = datetime.date( td.year, td.month, td.day )
        OneDay = OneDay + d1
        while startD <= OneDay:
            OneDay = OneDay - d1
            if OneDay.weekday() > 4:
                continue
            if not getSzQzInfo( '%s-%02d-%02d' % ( OneDay.year, OneDay.month, OneDay.day ) ):
                return  False
    except:
        print( 'exception in DigSzQzHisData' )
        return False


'''
os.system( r'notepad .\data\1.txt' )
wsh.SendKeys( "^a" )
wsh.SendKeys( "^c" )
wsh.SendKeys( "%{F4}" )

def GoToTag( fp ):
    pass

wsh.run( r"notepad" )
time.sleep( 1 )
wsh.SendKeys( "{TAB}" )
wsh.SendKeys( "TAB" )
wsh.SendKeys( "{ENTER}" )
wsh.SendKeys( "查询日期" )
wsh.SendKeys( "^f" )
'''

'''
class URLLister( SGMLParser ):
    def reset( self ):
        SGMLParser.reset( self )
        self.urls = []

    def start_a( self, attrs ):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend( href )
'''

def getURL( url ):
    try:
        usock = urllib.urlopen( url )
        content = usock.read()
        fp = open( r'.\data\webdata.txt', 'w' )
        fp.write( content )
        fp.close
    except:
        print 'get url excepton'
        return []

    parser = myparser()
    parser.feed( content )
    usock.close()
    parser.close()
    urls = parser.urls
    return urls


def getURLofFile( fn ):
    try:
        fp = open( fn )
        content = fp.read()
        fp.close
    except:
        print 'read file error'
        return []

    parser = myparser()
    parser.feed( content )
    parser.close()
    urls = parser.urls
    return urls

#spider(startURL,depth)递归调用getURL(url)，startURL为起始URL，depth为递归次数，及遍历的深度
def spider( startURL, depth ):
    i = 0
    global num      #num为全局变量，用来记录打印的url的数目
    if depth <= i:
       return 0
    else:
        urls = getURL( startURL )
        if len( urls ) > 0:
            for url in urls:
                print url, num
                num = num + 1
                spider( url, depth - 1 )
        else:
            return 0
    return 1

class myparser( SGMLParser ):
    is_td = 0
    is_prices = 0

    def reset( self ):
        SGMLParser.reset( self )
        self.urls = []

    def start_a( self, attrs ):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend( href )

    def __init__( self ):
        SGMLParser.__init__( self )
    #'''
    def start_div( self, attrs ):
        for id, value in attrs:
            if id == 'id' and value == 'prices' :
                self.is_prices = 1
        '''
        if attrs[0][1] == 'prices':
            self.is_prices = 1
        '''
    def end_div( self ):
        self.is_prices = 0
    def start_td( self, attrs ):
        self.is_td = 1
    def end_td( self ):
        self.is_td = 0
    def handle_data( self, text ):
        if self.is_prices == 1 and self.is_td == 1:
            print text.decode( 'cp936' )
    #'''



if __name__ == '__main__':
    # VosTool.ping( '122.9.61.34' )  #r'http://hq.forex.com.cn/' )  #'http://quote1.fx168.com/ajnew/WHs.aspx' )  #www.cnn.com' )

    '''
    num = 0
    spider( "http://www.xjtu.edu.cn/", 2 )
    '''

    #下面这段代码能轻易地抓取GOOGLE财经上上证指数的最新内容。要如何利用，随便你了。
    #   延时:   A stock/DJI/纳指/标普/ - realtime
    # 目前，谷歌提供的实时股票数据包括：道琼斯指数、纳斯达克指数、纳斯达克证券交易所、
    # 纽约证券交易所指数、标准普尔指数、深圳证券交易所和上海证券交易所，其他数据都会有15分钟
    # 至一个交易日不等的延时。之前，雅虎财经也将纳斯达克市场的指数升级为实时数据。

    urllink = urllib.urlopen( 'http://www.google.cn/finance/historical?q=SHA:000001' )
    data = urllink.read()
    urllink.close()
    fp = open( r'.\data\webdataGoogle.txt', 'w' )
    fp.write( data )
    fp.close
    my = myparser()
    my.feed( data )

    x = 1
    hyTitle = 'Hy Trade'
    #VosTool.waitWin( hyTitle, 10 )
    hyPath = r'C:\Program Files\HY Trader\terminal.exe' #"C:\Program Files\licai18\BootLoad.exe"
    VosTool.launch( hyPath, 30, hyTitle )

    ###########################################################################
    #auto launch data client
    wsh = win32com.client.Dispatch( "Wscript.Shell" )
    wsh.run( r'C:\new_gdzq_l2\TdxW.exe' )
    time.sleep( 3 )
    if False == wsh.AppActivate( '光大证券level2插件版' ):
        time.sleep( 1 )

    #auto imput user id info then login
    wsh.SendKeys( "{TAB}" )
    wsh.SendKeys( "40618106" )
    wsh.SendKeys( "{ENTER}" )
    wsh.SendKeys( "071210" )
    wsh.SendKeys( "{ENTER}" )
    # #随机验证码暂时无法自动识别输入

    #auto maximize the data client and switch to data collection model
    # #关闭自动弹出的风险提示窗口，自动弹出的窗口数量不定吗?
    # #切换到数据收集显示模式.006

    #verify his data, veryify model's validity and mechanism

    im = window_capture()
    import PIL
    box = ( int( left ), int( top ), int( right ), int( bottom ) )
    region = im.crop( box )
    region.save( 't.bmp', 'BMP' )

    import pytesser
    text1 = image_file_to_string( 't.bmp', graceful_errors = True )
    print( "\r\nmy char: " )
    print( text1 )
    from datetime import datetime
    s = datetime.now()
    s1 = '%02s%02s%02s' % ( s.hour, s.minute, s.second )
    rslt = open( "%s.txt" % s1, 'w' )
    rslt.write( text1 )


''' Yahoo! Finance
投资新手和嗜钱者的避风港，在这里，您可以找到一切与商业有关的内容，包括新闻、股评、图表乃至
出版发行。五月末，在主要的财经网站中，Yahoo! Finance率先恢复免费实时报价功能，从而取代了
标准的20分钟延时报价做法，如Google Finance和MSN Money就是采用这种报价方法（因与主要证券
交易所存在争议，该服务两年前曾中止过）。权力经纪人每个月为实时股票图表支付10.95美元。尽管
有舆论批评Yahoo!未有创新，但其金融网站则向人们展示了与其公司相称的最棒的内容。
'''

'''
    网页爬虫程序开发经验谈 作者：计世网商用软件频道 Jim http://www.ccw.com.cn 2008-08-15 09:02:01 我要评论(0)现在是网络的时代，所有数据都可以在互联网上得到，所以能够自动抓取Web数据的网页爬虫程序（又叫网络机器人，Web Robot）就逐渐流行了起来。 
    开发网页爬虫的过程，需要运用各种Heuristic（摸索体验）的作法：尝试你的想法，修正预期以外的错误（错误通常相当多），一再重复进行，直到网页爬虫可行为止。所以写网页爬虫程序时，是需要一点点耐心的。 
    一般的状况下，网页爬虫程序会先取一个网页，从此网页取出所有“后续的链接”，然后继续取这些链接的网页。网页的组织方式如果是线性的（例如：每个网页都有“前一笔资料”与“下一笔数据”的超级链接），那么超级链接就不会重复，所以就不需要判断这些链接有无重复。但组织方式只要不是线性的，都需要判断网页超级链接有无重复。 
    你以为HTTP状态码（status code）是代表正常的200，就表示能够顺利取网页吗？那可不一定，我发现有些服务器会限制同时上线的最大联机数目，超出限制，就会送出“服务器忙碌中”的HTML内容，但HTTP状态码（status code）居然还是使用代表正常的200。会不会遇到这种状况？何时会遇到？很难说得准。如果你想预防这种问题，可以从判断取内容的checksum有无重复来下手。 
    为了防堵网页爬虫，有些网站会限制来自同一个IP的请求频率。当频率超过限制，就会对此IP联机请求进行屏蔽，客户端最后会Timeout，联机失败。所以，当你遇到联机失败的状况，请先更换成新的IP，以确定服务器是否真的挂了，或者只是你的IP被封锁了。如果确定IP被封锁，你可以采用两种策略：（1）随时动态更换IP；或者（2）调节网页爬虫的请求频率。 
    如果你的计算机上同时有两三个IP，你当然可以在这些IP之间轮替更换，但这样其实帮助不大，因为IP被封锁通常会维持好一段时间，轮完第三个IP之后，恐怕第一个IP也还没被服务器从黑名单中去除。如果你要动态更换IP，最好改用ADSL拨号网络，因为ISP拥有大量的IP，会分配到和之前相同的IP机率很低。一旦你发现目前的IP被封锁，便可以立刻呼叫相关的API将网络断线并重新拨号，取得新的IP继续执行。 
    如果你不知道该如何呼叫拨号API，或者根本没有拨号网络，那么你只好降低网页爬虫发出请求的频率。频率太低，取得数据的速度太慢；频率太高，很快就会被服务器封锁。如何调整出一个理想值，通常需要测试好一阵子。 
    对网页资料的加工处理方式，通常是先将超级链接更新到本地文件，再提取重要数据保存到其他地方。更新超级链接其实满容易的，不容易出错，但“提取重要数据”就可能会遇到相当多问题，值得进一步探讨。 
    通过网页爬虫程序取的网页数据，通常需要经过加工处理。因此建议你不要一边取网页，一边加工处理，最好等网页全部取之后，再进行数据提取。为了避免URL名称不适合用来当成档名（例如Windows中不能用“con”当文件名），我习惯使用数字序号当文件名，然后再建立一个URL和数字序号的对照表（可以加上超级链接，以方便取用）。 
    在提取数据前，你需要先花一点时间研究出这些网页的HTML模板，接着你就可以取出特定tag的element，或者“以特定字符串为识别”的数据。我的经验是，光看几个HTML内容，仍不足以推测出完整的模板，有些状况可能是一百个或一千个网页才发生一次（更不用说还有一些是网站本身建构时的疏失）。因此，最好能先写一个程序扫描所有取的网页，证实你构想中的HTML模板是正确的，然后才开始进行数据提取。 
    在研究网页模板时，如果发现网页内出现JavaScript，你应该判断是否可以对它置之不理。因为许多网页的JavaScript程序代码是用来处理网页互动，和我们所关心的网页内容无关，可以不予理会。但如果遇到和数据相关的JavaScript程序代码（会产生HTTP请求），就必须特别注意。 
    你可以动用外部的JavaScript Engine（例如Rhino）来处理JavaScript程序代码，但是对网页爬虫程序来说，大多数的时候，其实没有必要这么做。你可以先阅读理解这些JavaScript程序代码，知道这段程序的目的是发出什么HTTP请求，就可以让网页爬虫自行模拟这样的HTTP请求。 
    当你的计算机跑着网页爬虫程序时，只要有预期以外的事情发生（例如格式不对、网站不通），就需要人的介入。尤其前几个小时是重要的观察期，这个时候最好乖乖地坐在计算机前，当出状况时，网页爬虫可以发出声音提醒我们进行处理。 
    我一直觉得，开发网页爬虫是相当实用、有趣、需要技巧的，且网页爬虫程序通常不大，所以很适合当作“下班后的自我挑战”，或是老师留给学生当作业。如果你没写过网页爬虫程序，我建议你马上试试看。
'''

'''
    Python常用模块
    图像获取：linux平台下使用sane模块，Windows平台下使用twain模块 
    图像处理PythonImageLibrary中文手册 
    使用_winreg模块操纵windows注册表 
    读取excel：用xlrd包。把excel转成csv，使用csv库操作。 
    将python程序打包成windows下可以执行的exe文件：使用py2exe模块 
    加密：Python Cryptography Toolkit http://www.amk.ca/python/code/crypto 
    在.net平台上使用python：IronPython 
    使用PyQt编写QT图形界面程序 http://www.riverbankcomputing.co.uk/pyqt/ 
    Python使用技巧 (2008-02-23 15:34:05由localhost编辑)
'''


''' server of hy trader
     Proto  Local Address          Foreign Address        State
     TCP    soho-tiger:3507        122.9.61.34:https      ESTABLISHED    eastaia02
     TCP    soho-tiger:4134        210.51.60.178:https    ESTABLISHED    eastaia01
'''

'''
    用python 连接google的简单例子
    作者：george chang      来源：cublog.cn     发表时间：2006-04-19     浏览次数： 5524      字号：大  中  小
    中国源码网内相关主题链接
    
    Python CGI实现用户会话 
    python中的类型判定 
    python元类的一些新认识 
    XML-RPC in Python简介 
    python的memcache和json模块 
    用Psyco让Python运行得像C一样快 
    python非贪婪,多行匹配正则表... 
    Python程序员常用的IDE和其它... 
    
    昨天突然想到用google查询点东西，后来想起了O'Reilly 的google hacks这本书，
    翻了一下，看到可以用python实现，就试了一试.注意要想通过python使用google api,那么需要SOAPPY,还有ZSI,pygoogle等模块.另外,要安装python的模块，还需要用到python-setuptools.
    
    源代码如下:
    #!/usr/bin/python
    import sys,string,codecs
    #google search api
    import google
    #handling command line arguments
    import getopt
    if sys.argv[1:]:
        #如果不进行unicode转换,好像查中文时会出错
        query=unicode(sys.argv[1],'utf-8') 
    else:
        sys.exit('Usage: python gsearch.py <query>')
    #my google license key
    google.LICENSE_KEY='输入你的google license key'
    #query google
    data=google.doGoogleSearch(query)
    sys.stdout=codecs.lookup('utf-8')[-1](sys.stdout)
    for result in data.results:
        print string.join((result.title,result.URL,result.snippet),"n"),"n"
'''

'''
   美元指数(USDX)的构成,各个货币兑所占权重。
   默认分类   2009-11-20 15:03   阅读36   评论0   字号： 大大  中中  小小  美元指数于CRB指数、道琼斯指数，被合称为反应美国经济风向标的三大指数。其中，美元指数是反应美元在外汇市场上整体强弱的指标。在国际市场中，几乎所有大宗商品都是以美元计价，所以美元的强弱会影响国际商品价格。 
   美元指数US Dollar Index(USDX)最初推出时，是由10个外汇品种构成，分别是德国马克、法国法郎、荷兰盾、意大利里拉、比利时法郎、日元、英镑、加拿大元、瑞典克朗和瑞士法郎。1999年欧元推出后，前五者均为欧元区货币，因此，美元指数在2000年也作了相应调整，以欧元代替这五种货币。所以，现在的美元指数是由6种货币构成。
                                                                             货币                        权重 
                                                                          欧元EUR                 0.576 
                                                                          日元JPY                  0.136 
                                                                          英镑GBP                 0.119 
                                                                          加拿大元CAD         0.091 
                                                                          瑞典克朗SEK         0.042 
                                                                          瑞士法郎CHF         0.036 
   这样的权重分配与最初美联储交易权重指数中使用的权重是一样的。
   美元指数的基期是1973年3月，从那是起主要贸易国都允许本国货币自由地于另一国货币进行浮动报价。 
   美元指数以几何加权平均方式计算，计算公式为： 
 USDX = 50.14348112 × EUR^-0.576 × JPY^0.136 × GBP/USD^-0.119 × USD/CAD^0.091 × SEK^0.042 × CHF^0.036 。其中，50.14348112是一个常数。这是为使基期指数为100而引入的。 
   美元指数中，各个币种的及时汇率数据是最基础的数据。全球外汇市场上的汇率在同一时间内可能有差异。现实中，NYBOT的美元指数采用数据来自世界范围内的500家左右的银行，由Reuters负责收集数据并计算。Reuters对来自世界各地银行的外汇报价进行每周七天、每天24小时的连续计算。计算结果由NYBOT的FINEX发布。 

'''
# 测试
