from pynput import keyboard
import pygame

def main(volume):
    flags = []

    def playSound(key):
        # for playing sound 
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("./sounds/{0}.wav".format(key))
            pygame.mixer.music.set_volume(float(int(volume.get())/100))
            pygame.mixer.music.play()       
        except:
            print("cannot find file"+key)

    def change(key):
        return {
            'ctrl':'c',
            'alt':'v',
            'cmd':'shift',
            '`':'n',
            '1':'m',
            '2':'n',
            '3':'b',
            '4':'v',
            '5':'g',
            '6':'h',
            '7':'j',
            '8':'k',
            '9':'l',
            '0':'c',
            '!':'m',
            '@':'n',
            '#':'b',
            '$':'v',
            '%':'g',
            '^':'h',
            '&':'j',
            '*':'k',
            '(':'l',
            ')':'c',
            ';':'q',
            '\'':'e',
            '\\':'s',
            '|':'s',
            '/':'z',
            '?':'z',
            '.':'t',
            ',':'u',
            '>':'t',
            '<':'u',
            '{':'[',
            '}':']',
            '-':'u',
            '_':'u',
            '+':'t',
            '=':'t',
            '\x00':'@',
            '\x01':'a',
            '\x02':'b',
            '\x03':'c',
            '\x04':'d',
            '\x05':'e',
            '\x06':'f',
            '\x07':'g',
            '\x08':'h',
            '\x09':'i',
            '\x0a':'j',
            '\x0b':'k',
            '\x0c':'l',
            '\x0d':'m',
            '\x0e':'n',
            '\x0f':'o',
            '\x10':'p',
            '\x11':'q',
            '\x12':'r',
            '\x13':'s',
            '\x14':'t',
            '\x15':'u',
            '\x16':'v',
            '\x17':'w',
            '\x18':'x',
            '\x19':'y',
            '\x1a':'z',
            '\x1b':'[',
            '\x1c':']',
            '\x1d':']',
            '\x1e':'^',
            '\x1f':'_',
            '\x20':' ',
            '\x7f':'?',
            'esc':'s',
            'f1':'r',
            'media':'g',
            'print':'b',
            'delete':'m',
            'up':'i',
            'down':'j',
            'left':'k',
            'right':'l',
            'num':'g',
            'insert':'c',
            'end':'m',
            'page':'b',
            'home':'j',
        }.get(key, key)
        
    def on_press(key):
        shouldPlay = True
        if hasattr(key, 'char'):
            if key.char == None:
                keyName = 'a'
            else:
                keyName = change(key.char.lower())
            if key.char in flags:
                shouldPlay = False
            else:
                flags.append(key.char)
        else:
            keyName = change(key.name.split('_')[0].lower())
            if key.name in flags:
                shouldPlay = False
            else:
                flags.append(key.name)
        if shouldPlay:
            playSound(keyName)

    def on_release(key):
        if hasattr(key, 'char'):
            if key.char in flags:
                flags.remove(key.char)
        else:
            if key.name in flags:
                flags.remove(key.name)

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press,
            on_release=on_release)
    
    listener.start()
