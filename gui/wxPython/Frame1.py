#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1LISTBOX1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(5)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(734, 333), size=wx.Size(756, 544),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(748, 510))

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='button1',
              name='button1', parent=self, pos=wx.Point(112, 72),
              size=wx.Size(96, 24), style=wx.TE_RICH)
        self.button1.SetToolTipString('bt')
        self.button1.SetMaxSize(wx.Size(77, 77))
        self.button1.SetMinSize(wx.Size(33, 33))

        self.listBox1 = wx.ListBox(choices=[], id=wxID_FRAME1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(360, 48),
              size=wx.Size(132, 66), style=0)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='staticText1', name='staticText1', parent=self,
              pos=wx.Point(136, 256), size=wx.Size(62, 14), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(336, 232), size=wx.Size(100, 22),
              style=wx.TE_RICH | wx.TE_MULTILINE,
              value='textCtrl1AAAAAAAAAAAAAAAAAAAAA')

    def __init__(self, parent):
        self._init_ctrls(parent)
