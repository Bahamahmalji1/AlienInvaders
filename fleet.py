import pygame as pg
from vector import Vector
from pygame.sprite import Sprite
from alien import Alien
from alienlaser import AlienLaser
from explosion import Explosion
import random

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.fleet_lasers = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)
        self.spacing = 1.4
        self.num_rows = 4
        self.max_aliens_per_row = 10
        self.create_fleet()
        self.explosions = []

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        self.max_aliens_per_row = 10 + self.stats.level
        alien = Alien(ai_game=self.ai_game, v=self.v, alien_type=0)
        alien_height = alien.rect.height
        current_y = alien_height + 50

        for row in range(self.num_rows):
            alien_type = 2 if row >= self.num_rows - 2 else row % 2
            self.create_row(current_y, alien_type)
            current_y += self.spacing * alien_height

    def create_row(self, y, alien_type):
        alien = Alien(ai_game=self.ai_game, v=self.v, alien_type=alien_type)
        alien_width = alien.rect.width
        current_x = alien_width 

        for _ in range(self.max_aliens_per_row):  
            new_alien = Alien(self.ai_game, v=self.v, alien_type=alien_type)
            new_alien.rect.y = y
            new_alien.y = y
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += self.spacing * alien_width
            
            if current_x >= self.settings.scr_width - alien_width:  
                break

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False
    
    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False

    def update(self):
        if self.aliens:
            alien_to_shoot = random.choice(self.aliens.sprites())
            if random.random() < alien_to_shoot.shooting_probability:
                laser = AlienLaser(ai_game=self.ai_game, x=alien_to_shoot.rect.centerx, y=alien_to_shoot.rect.bottom)
                self.ai_game.alien_lasers.add(laser)
                self.ai_game.sound.play_alien_laser()

        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.ai_game.sound.play_alien_hit()
                
                for alien in aliens:
                    explosion = Explosion(alien.rect.center)
                    self.explosions.append(explosion)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.ship.lasers.empty()
            self.create_fleet()
            self.stats.level += 1
            self.sb.prep_level()
            return

        if pg.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!")
            self.ship.ship_hit()
            return
        
        if self.check_bottom():
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed
            
        for alien in self.aliens:
            alien.update()

        dt = self.ai_game.clock.get_time()
        for explosion in self.explosions[:]:
            explosion.update(dt)
            explosion.draw(self.screen)
            if not explosion.active:
                self.explosions.remove(explosion)

    def draw(self): 
        for alien in self.aliens:
            alien.draw()

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
