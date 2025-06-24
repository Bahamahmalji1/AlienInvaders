import sys
import pygame as pg
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from event import Event
from barrier import Barriers
from sound import Sound
from alienlaser import AlienLaser
from explosion import Explosion

class SpaceInvaders:
    def __init__(self):
        pg.init()   
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()

        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(ai_game=self)

        self.alien_lasers = pg.sprite.Group()

        pg.display.set_caption("Alien Invasion")

        self.background = pg.image.load('images/background.jpeg').convert()
        self.background = pg.transform.scale(self.background, self.settings.w_h)

        self.game_active = False
        self.first = True

        self.play_button = Button(self, "Play")
        self.event = Event(self)

    def game_over(self):
        print("Game over!") 
        self.sound.play_gameover()
        self.game_active = False
        self.play_button.reset_message("Play again? (Press P to play, Q to quit)")
        pg.mouse.set_visible(True)

    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.sound.play_background()

        self.ship.reset_ship()
        self.fleet.reset_fleet()
        pg.mouse.set_visible(False)

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.play_button.reset_message("Play again? (q for quit)")
        self.reset_game()

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        while not self.finished:
            self.finished = self.event.check_events()
            if self.first or self.game_active:
                self.first = False

                self.screen.blit(self.background, (0, 0))

                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()
                self.alien_lasers.update()

                self.alien_lasers.draw(self.screen)

                if pg.sprite.spritecollideany(self.ship, self.alien_lasers):
                    self._ship_hit()

            if not self.game_active:
                self.play_button.draw_button()
                keys = pg.key.get_pressed()
                if keys[pg.K_p]:
                    self.reset_game()
                if keys[pg.K_q]:
                    self.finished = True

            pg.display.flip()
            self.clock.tick(60)
        pg.quit()
        sys.exit()

    def _ship_hit(self):
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        self.sb.prep_score_level_ships()

        self.sound.play_ship_hit()

        explosion = Explosion(self.ship.rect.center)
        self.fleet.explosions.append(explosion)

        if self.stats.ships_left > 0:
            self.ship.reset_ship()
        else:
            self.game_over()

if __name__ == '__main__':
    ai = SpaceInvaders()
    ai.run_game()
