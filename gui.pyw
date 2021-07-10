import wx
from root import Root
import threading
import custTray
import sys

class MechVibes:

    class MyFrame(wx.Frame):

        def __init__(self, volume):
            super().__init__(parent=None, title='MechVibes', size=(400,200))
            panel = wx.Panel(self)        
            my_sizer = wx.BoxSizer(wx.VERTICAL)    
            heading = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
            heading.SetSize(120, 23, 250, -1)
            font = wx.Font(25, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
            heading.SetFont(font) 
            heading.SetLabel("MechVibes")

            self.lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
            self.lbl.SetSize(15, 83, 250, -1)
            font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
            self.lbl.SetFont(font) 
            self.lbl.SetLabel("Volume "+str(volume.get()))


            self.hslider2 = wx.Slider(panel, -1, volume.get(), 0, 100,
                size=(250, -1),
                style=wx.SL_HORIZONTAL)       
            self.hslider2.SetSize(150, 85, 200, -1)
            self.hslider2.Bind(wx.EVT_COMMAND_SCROLL, self.on_press(volume))      
            panel.SetSizer(my_sizer)        
            
            self.tbIcon = custTray.CustomTaskBarIcon(self)
            
            self.Bind(wx.EVT_ICONIZE, self.onMinimize)
            self.Bind(wx.EVT_CLOSE, self.onClose)
            
            self.Hide()

        def on_press(self, volume):
            def OnClick(event):
                vol = self.hslider2.GetValue()
                self.lbl.SetLabel("Volume "+str(volume.get()))
                volume.changeVolume(int(vol))
                fo = open("initial_data.txt", "w")
                fo.write(str(vol))
                fo.close()
            return OnClick
        
        def onClose(self, evt):
            self.tbIcon.RemoveIcon()
            self.tbIcon.Destroy()
            self.Destroy()
            sys.exit()
            
        def onMinimize(self, event):
            if self.IsIconized():
                self.Hide()

    class Volume:
        def __init__(self,volume):
            self.volume = volume
        
        def get(self):
            return self.volume

        def changeVolume(self, volume):
            self.volume = volume

    def launchgui(self, volume):
        app = wx.App()
        self.MyFrame(volume)
        app.MainLoop()
        
    def launchroot(self, volume):
        Root(volume)

if __name__ == '__main__':
    fo = open("initial_data.txt", "r")
    initail_volume = int(fo.read())
    fo.close()
    mechVibes = MechVibes()
    volume = mechVibes.Volume(initail_volume)

    p2 = threading.Thread(target=mechVibes.launchroot, args=(volume, ), daemon=True)
    p1 = threading.Thread(target=mechVibes.launchgui, args=(volume, ), daemon=True)
    
    p1.start()
    p2.start()
  
    p1.join()
    p2.join()

    
