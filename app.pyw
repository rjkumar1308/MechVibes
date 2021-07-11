import wx
from root import Root
import threading
import custTray
import sys
from resource_path import resource_path 

class MechVibes:

    class MyFrame(wx.Frame):

        def __init__(self, volume):
            super().__init__(parent=None, title='MechVibes', size=(400,300), style=wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
            panel = wx.Panel(self)  
            panel.SetBackgroundColour((255,255,255))
            self.SetIcon(wx.Icon(resource_path("icon.png")))      
            my_sizer = wx.BoxSizer(wx.VERTICAL)    

            border = wx.StaticBox(panel, -1, '') 
            borderSizer = wx.StaticBoxSizer(border, wx.VERTICAL) 
            borderbox = wx.BoxSizer(wx.HORIZONTAL) 
            borderbox2 = wx.BoxSizer(wx.HORIZONTAL) 
            topSizer = wx.BoxSizer(wx.HORIZONTAL) 
            volumeSizer = wx.BoxSizer(wx.HORIZONTAL) 
            volumeSizerTop = wx.BoxSizer(wx.HORIZONTAL) 

            heading = wx.StaticText(panel ,style = wx.ALIGN_CENTER)
            font = wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) 
            heading.SetFont(font) 
            heading.SetLabel("MechVibes")

            borderbox.Add(heading, 0, wx.BOTTOM|wx.TOP, 20) 
            borderbox2.Add(borderbox, 0, wx.LEFT|wx.RIGHT, 5) 
            borderSizer.Add(borderbox2, 0, wx.ALL|wx.CENTER, 10)  
            topSizer.Add(borderSizer, 0, wx.BOTTOM|wx.TOP, 20)  

            self.lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
            self.lbl.SetSize(15, 173, 250, -1)
            font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT) 
            self.lbl.SetFont(font) 
            self.lbl.SetLabel("Volume "+str(volume.get()))
            self.lbl.SetForegroundColour("#808080")

            self.hslider2 = wx.Slider(panel, -1, volume.get(), 0, 100,
                size=(250, -1),
                style=wx.SL_HORIZONTAL)       
            self.hslider2.SetSize(150, 175, 200, -1)
            self.hslider2.Bind(wx.EVT_COMMAND_SCROLL, self.on_press(volume))

            volumeSizer.Add(self.lbl, 0, wx.RIGHT|wx.LEFT|wx.BOTTOM, 20) 
            volumeSizer.Add(self.hslider2, 0, wx.RIGHT|wx.LEFT|wx.BOTTOM, 20) 
            volumeSizerTop.Add(volumeSizer, 0, wx.TOP, 20) 

            my_sizer.Add(topSizer,0, wx.ALL|wx.CENTER, 5) 
            my_sizer.Add(volumeSizerTop, 0, wx.LEFT|wx.RIGHT, 25)  
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
                fo = open(resource_path("initial_data.txt"), "w")
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
    fo = open(resource_path("initial_data.txt"), "r")
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

    
