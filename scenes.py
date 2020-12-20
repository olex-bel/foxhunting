import pygame
import text
import board
import utils

GRID_SIZE = 10
NUMBER_OF_FOXES = 8
BACKGROUND_COLOR = (145, 145, 145)


class Scene:

    STATE_NEXT_SCENE = 1
    STATE_STOP_GAME_LOOP = 2

    def __init__(self, screen):
        self.screen = screen
        self.all = pygame.sprite.RenderUpdates()

    def init_scene(self):
        self.all.empty()

    def _draw(self):
        self.all.update()
        dirty = self.all.draw(self.screen)
        pygame.display.update(dirty)
        pygame.display.flip()

    def run_scene(self):
        return Scene.STATE_STOP_GAME_LOOP


class GameScene(Scene):

    background_color = (145, 145, 145)

    def __init__(self, screen):
        Scene.__init__(self, screen)
        board.Cell.image = utils.load_image('gross.png')
        board.FoxCell.image = utils.load_image('fox.png')
        board.FoxCell.image.set_colorkey((255, 255, 255))
        board.EmptyCell.font = pygame.font.Font(
            pygame.font.get_default_font(), 15)

        self.clicksCounter = None
        self.hitsCounter = None
        self.cells_sprites = None
        self.background = pygame.Surface(screen.get_size()).convert()
        self.background.fill(GameScene.background_color)
        self.clock = pygame.time.Clock()

    def init_scene(self):
        Scene.init_scene(self)
        self.clicksCounter = text.ClicksCounterText((350, 20))
        self.hitsCounter = text.HitsCounterText((350, 50))

        self.cells_sprites = board.create_cells_sprites(
            (5, 5), GRID_SIZE, NUMBER_OF_FOXES)
        self.all = pygame.sprite.RenderUpdates()

        self.all.add(*self.cells_sprites)
        self.all.add(self.clicksCounter, self.hitsCounter)
        self.screen.blit(self.background, (0, 0))

    def run_scene(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.STATE_STOP_GAME_LOOP

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    for sprite in self.cells_sprites:
                        if sprite.rect.collidepoint(pos) and not sprite.isOpen:
                            sprite.handle_click()
                            self.clicksCounter.increase_counter()

                            if sprite.hasFox:
                                self.hitsCounter.increase_counter()
                                break

            self._draw()

            if self.hitsCounter.hits == NUMBER_OF_FOXES:
                return Scene.STATE_NEXT_SCENE

            self.clock.tick(60)

    def _draw(self):
        self.all.clear(self.screen, self.background)
        Scene._draw(self)


class EndGameScene(Scene):

    def __init__(self, screen):
        Scene.__init__(self, screen)
        self.button_yes = None
        self.button_no = None
        self.message = None
        self.clock = pygame.time.Clock()

    def init_scene(self):
        Scene.init_scene(self)
        self.button_yes = text.Button((140, 220), 'Yes')
        self.button_no = text.Button((245, 220), 'No')
        self.message = text.EndGameMessage((50, 150))
        self.all.add(self.button_yes, self.button_no, self.message)

    def run_scene(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Scene.STATE_STOP_GAME_LOOP

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    if self.button_yes.rect.collidepoint(pos):
                        return Scene.STATE_NEXT_SCENE
                    elif self.button_no.rect.collidepoint(pos):
                        return Scene.STATE_STOP_GAME_LOOP

            self._draw()
            self.clock.tick(60)
