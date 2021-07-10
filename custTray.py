import wx.adv
import wx

class CustomTaskBarIcon(wx.adv.TaskBarIcon ):
    
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        
        img = wx.Image("icon.png", wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(img)
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(bmp)
        
        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
 
    def OnTaskBarActivate(self, evt):
        pass
 
    def OnTaskBarClose(self, evt):
        self.frame.Close()
 
    def OnTaskBarLeftClick(self, evt):
        self.frame.Show()
        self.frame.Restore()