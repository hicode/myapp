# coding=utf-8

#python win32 windows2008年09月28日 星期日 13:50
import win32gui, win32con
def wndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_CREATE: print 'message: WM_CREATE'
    if msg == win32con.WM_SIZE: print 'message: WM_SIZE'
    if msg == win32con.WM_PAINT: print 'message: WM_PAINT'
    if msg == win32con.WM_CLOSE: print 'message: WM_CLOSE'
    if msg == win32con.WM_DESTROY:
        print 'message: WM_DESTROY'
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)
       
wndClsStruct = win32gui.WNDCLASS()
wndClsStruct.hbrBackground = win32con.COLOR_BTNFACE + 1
wndClsStruct.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wndClsStruct.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
wndClsStruct.lpszClassName = "MySimpleWindow"
wndClsStruct.lpfnWndProc = wndProc

wndClassAtom = win32gui.RegisterClass(wndClsStruct)

hwnd = win32gui.CreateWindow(
            wndClassAtom, 'Spark Test', win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0,0, 0, None)

win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.UpdateWindow(hwnd)
win32gui.PumpMessages()
 


#python实现全屏截图(win32)2008年04月16日 下午 08:43#!/usr/bin/env python
# #coding:utf-8

#还有一种方法是利用发送按键，读取剪贴板，由于比较麻烦所以就不写了
#至于Linux下可以直接使用一些命令来达到目的。

import time 
import os, win32gui, win32ui, win32con, win32api 

def window_capture(): 
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd) 
    mfcDC=win32ui.CreateDCFromHandle(hwndDC) 
    saveDC=mfcDC.CreateCompatibleDC() 
    saveBitMap = win32ui.CreateBitmap() 
    MoniterDev=win32api.EnumDisplayMonitors(None,None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    print w,h
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h) 
    saveDC.SelectObject(saveBitMap) 
    saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY) 
    bmpname=win32api.GetTempFileName(".","")[0]+'.bmp'
    saveBitMap.SaveBitmapFile(saveDC, bmpname) 
    return bmpname
    
os.system(window_capture())




#python实现全屏截图(win32) 
#一段Python实现的全屏抓图代码:

# coding:gb2312
# python实现全屏截图(win32)

import time 
import os, win32gui, win32ui, win32con, win32api 

def window_capture(): 
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd) 
    mfcDC=win32ui.CreateDCFromHandle(hwndDC) 
    saveDC=mfcDC.CreateCompatibleDC() 
    saveBitMap = win32ui.CreateBitmap() 
    MoniterDev=win32api.EnumDisplayMonitors(None,None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    print w,h
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h) 
    saveDC.SelectObject(saveBitMap) 
    saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY) 
    bmpname=win32api.GetTempFileName(".","")[0]+'.bmp' 
    saveBitMap.SaveBitmapFile(saveDC, bmpname) 
    return bmpname
    
os.system(window_capture())



#Python获取屏幕分辨率大小 
#   获取屏幕大小有两种方法可以办到:
#  1.wxPython里的
#  2.win32api

# coding:gb2312
# wxApp.py 
# author: aoogur

import os
import wx
from win32api import GetSystemMetrics

class Frame(wx.Frame):
    def __init__ (self):
        wx.Frame.__init__(self,None,-1,title="wxApp.",size=(250,250),pos=(0,0))

        #一种方法(wxPython)
        mm=wx.DisplaySize()
        print "width=",mm[0]
        print 'height=',mm[1]
        #另一种方法
        print "width =", GetSystemMetrics (0)
        print "height =",GetSystemMetrics (1)
class App(wx.App):
    def OnInit(self):
        frame = Frame()
        frame.Show(True)
        return True
    
if __name__ == "__main__":
    app = App(False)
    app.MainLoop()

