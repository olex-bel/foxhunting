import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from random import randint


class Cell(Sprite):

    width = 32
    height = 32
    image = None

    def __init__(self, topleft):
        Sprite.__init__(self)

        self.rect = Rect(topleft[0], topleft[1], Cell.width, Cell.height)
        self.isOpen = False
        self.hasFox = False
        self._set_current_image(Cell.image)

    def _set_current_image(self, image, background_color=None):
        self.image = pygame.Surface((Cell.width, Cell.height)).convert()

        if background_color is not None:
            self.image.fill(background_color)

        self.image.blit(image, (0, 0))
        pygame.draw.rect(self.image, (1, 1, 1), Rect(
            0, 0, Cell.width, Cell.height), 1)

    def _open_cell(self):
        pass

    def handle_click(self):
        if not self.isOpen:
            self.isOpen = True
            self._open_cell()

    def draw(self, surface):
        text_rect = self.image.get_rect()
        text_rect.center = self.rect.center
        surface.blit(self.image, text_rect.topleft)


class FoxCell(Cell):

    image = None
    open_cell_bg_color = (83, 221, 124)

    def __init__(self, topleft):
        Cell.__init__(self, topleft)
        self.hasFox = True

    def _open_cell(self):
        self._set_current_image(FoxCell.image, FoxCell.open_cell_bg_color)


class EmptyCell(Cell):

    open_cell_bg_color = (83, 221, 124)
    font = None

    def __init__(self, topleft, foxes_around):
        Cell.__init__(self, topleft)
        self.foxes_around = foxes_around

    def _open_cell(self):
        image = pygame.Surface((Cell.width, Cell.height))
        image.fill(EmptyCell.open_cell_bg_color)

        text_image = EmptyCell.font.render(
            str(self.foxes_around), False, (0, 0, 0))

        text_rect = text_image.get_rect()
        text_rect.center = image.get_rect().center
        image.blit(text_image, text_rect.topleft)
        self._set_current_image(image)


def generate_foxes_locations(grid_size, number_of_foxes):
    max_col = grid_size - 1
    max_row = grid_size - 1

    foxes_locations = {(randint(0, max_col), randint(0, max_row))}

    while len(foxes_locations) < number_of_foxes:
        point = (randint(0, max_col), randint(0, max_row))

        if point not in foxes_locations:
            foxes_locations.add(point)

    return foxes_locations


def create_cells_sprites(topleft, grid_size, number_of_foxes):
    foxes_locations = generate_foxes_locations(grid_size, number_of_foxes)
    cells_sprites = []
    cell_margin = 2
    x_cell_offset = Cell.width + cell_margin
    y_cell_offset = Cell.height + cell_margin

    for row in range(0, grid_size):
        for col in range(0, grid_size):
            x = topleft[0] + col * x_cell_offset + cell_margin
            y = topleft[1] + row * y_cell_offset + cell_margin

            if (col, row) in foxes_locations:
                cells_sprites.append(FoxCell((x, y)))
            else:
                foxes_on_vertical = [
                    location for location in foxes_locations if location[1] == row]
                foxes_on_horizontal = [
                    location for location in foxes_locations if location[0] == col]
                foxes_on_diagonals = [location for location in foxes_locations if abs(
                    col - location[0]) == abs(row - location[1])]
                number_foxes_around = len(
                    foxes_on_vertical) + len(foxes_on_horizontal) + len(foxes_on_diagonals)

                cells_sprites.append(EmptyCell((x, y), number_foxes_around))
    return cells_sprites
