import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.button_color = (255, 255, 255)
        self.text_color = (50, 50, 50)
        self.font = pygame.font.SysFont(None, 48)

        self._prep_msg(msg)

    def reset_message(self, msg="Play"):
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()

        padding_x, padding_y = 20, 10
        self.width = self.msg_image_rect.width + 2 * padding_x
        self.height = self.msg_image_rect.height + 2 * padding_y

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
