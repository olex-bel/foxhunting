import pygame
import utils
from pygame.sprite import Sprite
from pygame.locals import Rect


class Text(Sprite):

    def __init__(self, topleft):
        Sprite.__init__(self)
        self.image = None
        self.topleft = topleft
        self.font = utils.load_font('GenghisKhan.otf', 22)

    def _get_text(self):
        return ''

    def _get_font(self):
        return self.font

    def _update_image_text(self):
        self.image = self._render_text()
        image_rect = self.image.get_rect()
        self.rect = Rect(self.topleft, (image_rect.width, image_rect.height))

    def _render_text(self):
        return self._get_font().render(self._get_text(), False, (0, 0, 0))


class ClicksCounterText(Text):

    def __init__(self, topleft):
        Text.__init__(self, topleft)
        self.clicks = 0
        self._update_image_text()

    def increase_counter(self):
        self.clicks += 1
        self._update_image_text()

    def _get_text(self):
        return 'Shots: {0}'.format(self.clicks)


class HitsCounterText(Text):

    def __init__(self, topleft):
        Text.__init__(self, topleft)
        self.hits = 0
        self._update_image_text()

    def increase_counter(self):
        self.hits += 1
        self._update_image_text()

    def _get_text(self):
        return 'Hits: {0}'.format(self.hits)


class Button(Sprite):

    padding = 4
    background_color = (84, 87, 92)

    def __init__(self, topleft, caption):
        Sprite.__init__(self)
        self.caption = caption
        self.font = utils.load_font('GenghisKhan.otf', 20)
        self.image = self._render_text()
        image_rect = self.image.get_rect()
        self.rect = Rect(topleft, (image_rect.width, image_rect.height))

    def _render_text(self):
        text_image = self.font.render(self.caption, False, (0, 0, 0))
        text_image_rect = text_image.get_rect()
        (width, height) = text_image.get_size()
        image = pygame.Surface(
            (width + 2 * Button.padding, height + 2 * Button.padding)).convert()
        image.fill(Button.background_color)
        text_image_rect.center = image.get_rect().center
        image.blit(text_image, text_image_rect.topleft)

        return image


class EndGameMessage(Sprite):

    text_color = (0, 0, 0)
    background_color = (84, 87, 92)
    line_height = 8

    def __init__(self, topleft):
        Sprite.__init__(self)
        self.font = utils.load_font('GenghisKhan.otf', 26)
        self.text_line_1 = 'You found all foxes. Congratulations!'
        self.text_line_2 = 'Play again?'
        self.image = self._render_text()
        image_rect = self.image.get_rect()
        self.rect = Rect(topleft, (image_rect.width, image_rect.height))

    def _render_text(self):
        text_image_line_1 = self.font.render(
            self.text_line_1, False, EndGameMessage.text_color)
        text_image_line_2 = self.font.render(
            self.text_line_2, False, EndGameMessage.text_color)
        width = max(text_image_line_1.get_width(),
                    text_image_line_2.get_width())
        height = text_image_line_1.get_height() + text_image_line_2.get_height() + \
            EndGameMessage.line_height
        image = pygame.Surface((width, height))
        image.fill(EndGameMessage.background_color)

        image.blit(text_image_line_1,
                   ((width - text_image_line_1.get_width()) // 2, 0))
        image.blit(text_image_line_2,
                   ((width - text_image_line_2.get_width()) // 2, text_image_line_1.get_height() + EndGameMessage.line_height))

        return image
