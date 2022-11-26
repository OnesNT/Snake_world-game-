from Game import Game

if __name__ == '__main__':
    game = Game()
    game.enter_name_layout()
    game.select_color_snake()
    game.choose_level_layout()
    game.choose_map_layout()
    game.run_game()

