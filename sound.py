import pygame as pg 
import time

class Sound:
    def __init__(self): 
        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        pg.mixer.music.load('sounds/interstellar.mp3')
        pg.mixer.music.set_volume(0.2)

        self.alien_laser = pg.mixer.Sound('sounds/alien_laser.wav')
        
        self.alien_hit = pg.mixer.Sound('sounds/alien_hit.mp3')
        
        self.ship_hit = pg.mixer.Sound('sounds/ship_hit.wav')

    def play_background(self): 
        pg.mixer.music.play(-1, 0.0)
        self.music_playing = True
        
    def play_pickup(self): 
        if self.music_playing: 
            self.pickup.play()
            
    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(3.0) 
        
    def play_alien_laser(self):
        if self.music_playing: 
            self.alien_laser.play()

    def play_alien_hit(self):
        if self.music_playing: 
            self.alien_hit.play()

    def play_ship_hit(self):
        if self.music_playing: 
            self.ship_hit.play()

    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False 
