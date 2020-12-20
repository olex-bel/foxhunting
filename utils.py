import os.path
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(filename):
    filepath = os.path.join(main_dir, "assets", filename)
    try:
        surface = pygame.image.load(filepath)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert()


def load_font(filename, size):
    filepath = os.path.join(main_dir, "fonts", filename)

    return pygame.font.Font(filepath, size)
