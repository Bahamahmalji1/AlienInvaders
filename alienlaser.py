import pygame as pg
from pygame.sprite import Sprite

class AlienLaser(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pg.Surface((self.settings.alien_laser_width, self.settings.alien_laser_height))  
        self.image.fill(self.settings.alien_laser_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.alien_laser_speed
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

def main():
    print("\nYou have to run from alien_invasion.py\n")

if __name__ == "__main__":
    main()
