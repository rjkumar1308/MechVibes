import wx.adv
import wx
from resource_path import resource_path 

class CustomTaskBarIcon(wx.adv.TaskBarIcon ):
    
    TBMENU_RESTORE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        
        img = wx.Image(resource_path("icon.png"), wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(img)
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(bmp)
        
        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarRightClick)
        self.Bind(wx.EVT_MENU, self.OnTaskBarLeftClick, id=self.TBMENU_RESTORE)   
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE) 
 
    def OnTaskBarActivate(self, evt):
        pass
 
    def OnTaskBarClose(self, evt):
        self.frame.Close()
 
    def OnTaskBarLeftClick(self, evt):
        self.frame.Show()
        self.frame.Restore()

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        self.menu.Append(self.TBMENU_RESTORE, "Restore")
        self.menu.Append(self.TBMENU_CLOSE, "Close")
        return self.menu

    def OnTaskBarRightClick(self, evt):
        self.CreatePopupMenu()