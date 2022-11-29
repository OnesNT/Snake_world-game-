import pygame
import game_variable


class Map:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.blocked_area = []
        self.dir_map1 = True
        self.remove_part1 = 100
        self.dir_map2 = True
        self.remove_part2 = 100
        self.which_map = 0

    def draw(self):
        for pos in self.blocked_area:
            pygame.draw.rect(self.parent_screen, game_variable.white, pygame.Rect(pos[0], pos[1], 10, 10))

    def map_1(self):
        for block in range(0, game_variable.frame_size_x, 10):
            self.blocked_area.insert(0, (block, 0))
            self.blocked_area.insert(0, (block, game_variable.frame_size_y - 10))

        for block in range(0, game_variable.frame_size_y, 10):
            self.blocked_area.insert(0, (0, block))
            self.blocked_area.insert(0, (game_variable.frame_size_x - 10, block))

    def map_2(self):
        for block in range(0, game_variable.frame_size_x, 10):
            self.blocked_area.insert(0, (block, 0))
            self.blocked_area.insert(0, (block, game_variable.frame_size_y - 10))

        for block in range(0, game_variable.frame_size_y, 10):
            self.blocked_area.insert(0, (0, block))
            self.blocked_area.insert(0, (game_variable.frame_size_x - 10, block))

        for block_x in range(0, game_variable.frame_size_x, 180):
            for block_y in range(0, game_variable.frame_size_y - 10, 10):
                if block_y < block_x / 180 * 30 or block_y > block_x / 180 * 90:
                    self.blocked_area.insert(0, (block_x, block_y))

    def map_3(self):
        for block in range(0, game_variable.frame_size_x, 10):
            self.blocked_area.insert(0, (block, 0))
            self.blocked_area.insert(0, (block, game_variable.frame_size_y - 10))

        for block in range(0, game_variable.frame_size_y, 10):
            self.blocked_area.insert(0, (0, block))
            self.blocked_area.insert(0, (game_variable.frame_size_x - 10, block))

        for block_x in range(0, game_variable.frame_size_x, 240):
            for block_y in range(10, game_variable.frame_size_y - 10, 10):
                self.blocked_area.insert(0, (block_x, block_y))

