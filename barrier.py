import pygame as pg
from pygame.sprite import Sprite, Group

BARRIER_ARCH_HEIGHT = 4
BARRIER_ARCH_WIDTH_2 = 4

class BarrierPiece(Sprite):
    health_colors = {
        6: pg.Color(0, 255, 0),
        5: pg.Color(0, 128, 255),
        4: pg.Color(0, 0, 255),
        3: pg.Color(255, 255, 0),
        2: pg.Color(255, 128, 0),
        1: pg.Color(255, 0, 0),
        0: pg.Color(0, 0, 0)
    }

    def __init__(self, ai_game, rect):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.rect = rect
        self.health = len(BarrierPiece.health_colors) - 1

    def hit(self):
        print('BarrierPiece hit!')
        if self.health > 0: 
            self.health -= 1
        if self.health == 0: 
            self.kill()

    def draw(self):
        pg.draw.rect(self.screen, BarrierPiece.health_colors[self.health], self.rect)


class Barrier(Sprite):
    
    def __init__(self, ai_game, width, height, deltax, deltay, x, y):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.deltax, self.deltay = deltax, deltay
        self.barrier_pieces = Group()
        self.create_barrier_pieces()

    def create_barrier_pieces(self):
        num_rows = self.height // self.deltay
        num_cols = self.width // self.deltax

        for row in range(num_rows):
            for col in range(num_cols):
                rect = pg.Rect(self.x + col * self.deltax, self.y + row * self.deltay, 
                               self.deltax, self.deltay)

                if num_rows - row < BARRIER_ARCH_HEIGHT and abs(col - num_cols / 2) < BARRIER_ARCH_WIDTH_2:
                    continue

                self.barrier_pieces.add(BarrierPiece(ai_game=self.ai_game, rect=rect))

    def reset(self):
        self.barrier_pieces.empty()
        self.create_barrier_pieces()

    def update(self): 
        collisions = pg.sprite.groupcollide(self.barrier_pieces, self.ai_game.ship.lasers, False, True)
        for piece in collisions:
            piece.hit()


        collisions_with_alien_lasers = pg.sprite.groupcollide(self.barrier_pieces, self.ai_game.alien_lasers, False, True)
        for piece in collisions_with_alien_lasers:
            piece.hit()

        self.draw()

    def draw(self):
        """Draw all barrier pieces on the screen."""
        for piece in self.barrier_pieces:
            piece.draw()


BARRIER_WIDTH = 150
BARRIER_HEIGHT = 80

class Barriers:
    
    positions = [(BARRIER_WIDTH * x + BARRIER_WIDTH / 2.0, 600) for x in range(0, 7, 2)]

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):     
        barriers = [
            Barrier(ai_game=self.ai_game, 
                    width=BARRIER_WIDTH, height=BARRIER_HEIGHT, 
                    deltax=9, deltay=9,
                    x=x, y=y) for x, y in Barriers.positions]
        for barrier in barriers:
            self.barriers.add(barrier)

    def reset(self):
        for barrier in self.barriers:
            barrier.reset()

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()
