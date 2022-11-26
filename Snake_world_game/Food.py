import random
import pygame
import game_variable


class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.food_pos = [random.randrange(1, (game_variable.frame_size_x // 10)) * 10,
                         random.randrange(1, (game_variable.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.bonus_success = False

    def bonus_food(self):
        direction_food = ["DOWN", "RIGHT"]
        ran = random.randrange(0, 2)
        if direction_food[ran] == "DOWN":
            self.food_pos[1] += 10
        if direction_food[ran] == "RIGHT":
            self.food_pos[0] += 10

        if self.food_pos[0] < 0 or self.food_pos[0] > game_variable.frame_size_x - 10 or self.food_pos[1] < 0 \
                or self.food_pos[1] > game_variable.frame_size_y - 10:
            self.food_spawn = False
            self.bonus_success = False

    def change_pos_food(self, x, y):
        self.food_pos = [x, y]

    def change_pos_bonus(self):
        self.food_pos = [random.randint(0, 100), random.randint(0, 100)]

    def draw(self):
        pygame.draw.rect(self.parent_screen, pygame.Color(0, 255, 0),
                         pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

