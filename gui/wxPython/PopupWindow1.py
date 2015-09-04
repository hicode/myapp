#Boa:PopupWindow:PopupWindow1

import wx
import wx.lib.buttons

def create(parent):
    return PopupWindow1(parent)

[wxID_POPUPWINDOW1, wxID_POPUPWINDOW1GENBUTTON1, wxID_POPUPWINDOW1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(3)]

class PopupWindow1(wx.PopupWindow):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.PopupWindow.__init__(self, flags=wx.SIMPLE_BORDER, parent=prnt)
        self.SetSize(wx.Size(664, 571))
        self.Move(wx.Point(235, 304))

        self.staticText1 = wx.StaticText(id=wxID_POPUPWINDOW1STATICTEXT1,
              label='staticText1', name='staticText1', parent=self,
              pos=wx.Point(64, 24), size=wx.Size(62, 14), style=0)

        self.genButton1 = wx.lib.buttons.GenButton(id=wxID_POPUPWINDOW1GENBUTTON1,
              label='genButton1', name='genButton1', parent=self,
              pos=wx.Point(184, 16), size=wx.Size(79, 26), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
