from root import Root
import threading
from resource_path import resource_path 
from gui import GUI

class MechVibes:

    class Volume:
        def __init__(self,volume):
            self.volume = volume
        
        def get(self):
            return self.volume

        def changeVolume(self, volume):
            self.volume = volume

    def launchgui(self, volume):
        GUI(volume)
        
    def launchroot(self, volume):
        Root(volume)


if __name__ == '__main__':
    try:
        fo = open(resource_path("initial_data.txt"), "r")
        initail_volume = int(fo.read())
        fo.close()
    except:
        initail_volume = 100
    mechVibes = MechVibes()
    volume = mechVibes.Volume(initail_volume)

    p2 = threading.Thread(target=mechVibes.launchroot, args=(volume, ), daemon=True)
    p1 = threading.Thread(target=mechVibes.launchgui, args=(volume, ), daemon=True)
    
    p1.start()
    p2.start()
  
    p1.join()
    p2.join()

    
