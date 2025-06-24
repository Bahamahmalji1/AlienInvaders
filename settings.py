from colors import DARK_GREY, RED, BLACK, ORANGE, PURPLE

class Settings:
    def __init__(self):
        self.scr_width = 1200
        self.scr_height = 800
        self.bg_color = BLACK
        self.w_h = (self.scr_width, self.scr_height)

        self.laser_speed = 3.0
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = RED

        self.alien_laser_speed = 2.5
        self.alien_laser_width = self.laser_width
        self.alien_laser_height = self.laser_height
        self.alien_laser_color = ORANGE

        self.ship_limit = 3
        self.ship_fire_every = 10
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 10.0
        self.laser_speed = 2.5
        self.alien_speed = 1.0

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


def main():
    print('\n*** message from settings.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()
