import pygame
import scenes


def main():
    # Initialise screen
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((445, 353))
    pygame.display.set_caption('Fox Hunting')

    main_scene = scenes.GameScene(screen)
    end_game_scene = scenes.EndGameScene(screen)

    while True:
        main_scene.init_scene()

        if main_scene.run_scene() == scenes.Scene.STATE_NEXT_SCENE:
            end_game_scene.init_scene()

            if end_game_scene.run_scene() == scenes.Scene.STATE_STOP_GAME_LOOP:
                return
        else:
            return


if __name__ == '__main__':
    main()
