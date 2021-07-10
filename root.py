from pynput import keyboard
import pygame
from change import change

class Root:

    def __init__(self,volume):
        self.volume = volume
        self.flags = []
        self.run()

    def playSound(self, key):
        # for playing sound 
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("./sounds/{0}.wav".format(key))
            pygame.mixer.music.set_volume(float(int(self.volume.get())/100))
            pygame.mixer.music.play()       
        except:
            print("cannot find file"+key)
        
    def on_press(self, key):
        shouldPlay = True
        if hasattr(key, 'char'):
            if key.char == None:
                keyName = 'a'
            else:
                keyName = change(key.char.lower())
            if key.char in self.flags:
                shouldPlay = False
            else:
                self.flags.append(key.char)
        else:
            keyName = change(key.name.split('_')[0].lower())
            if key.name in self.flags:
                shouldPlay = False
            else:
                self.flags.append(key.name)
        if shouldPlay:
            self.playSound(keyName)

    def on_release(self, key):
        if hasattr(key, 'char'):
            if key.char in self.flags:
                self.flags.remove(key.char)
        else:
            if key.name in self.flags:
                self.flags.remove(key.name)

    def run(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()

        listener = keyboard.Listener(on_press=self.on_press,
                on_release=self.on_release)
        
        listener.start()