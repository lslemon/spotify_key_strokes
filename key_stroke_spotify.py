# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:38:05 2019

@author: lukes
"""

#!/usr/bin/env python3
global combination
import subprocess
from pynput import keyboard
import Spotify_Music_Controls as sp

def on_press(key):
    global combination
    combination.append(key)
    if combination == combination_next:
        sp.next_song()
#        print("NEXT")
    if combination == combination_previous:
        sp.previous_song()
#        print("PREVIOUS")
    if combination == combination_resume:
        sp.resume_song()
#        print("RESUME")
    if combination == combination_pause:
        sp.pause_song()
#        print("PAUSE")
    if len(combination) > 3:
        combination.clear()
    
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    global combination
    combination.clear()
    

combination_next = [keyboard.Key.ctrl_l, keyboard.Key.right]
combination_previous = [keyboard.Key.ctrl_l, keyboard.Key.left]
combination_resume = [keyboard.Key.ctrl_l, keyboard.Key.up]
combination_pause = [keyboard.Key.ctrl_l, keyboard.Key.down]

combination = []
# ...or, in a non-blocking fashion:
#with  keyboard.Listener(
#    on_press=on_press,
#    on_release=on_release) as listener:
#    listener.join()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
#subprocess.Popen(listener.start())
listener.start()
