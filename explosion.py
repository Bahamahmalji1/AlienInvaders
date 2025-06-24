import pygame as pg

class Explosion:
    def __init__(self, position):
        self.image = pg.image.load('images/explosion.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.active = True
        self.timer = 0
        self.duration = 500

    def update(self, dt):
        self.timer += dt
        if self.timer > self.duration:
            self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
