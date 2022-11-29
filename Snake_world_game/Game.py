from Snake import Snake
from Food import Food
from Map import Map
import pygame
import time
import sys
import math
import random
import game_variable


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake world")
        self.surface = pygame.display.set_mode((game_variable.frame_size_x, game_variable.frame_size_y))
        self.map = Map(self.surface)
        self.snake = Snake(self.surface)
        self.food = Food(self.surface)
        self.score = 0
        self.player_name = ''
        self.difficulty = 0

    def write_text_on_game(self, font, size, color_text, text, x, y):
        my_font = pygame.font.SysFont(font, size)
        surface_text = my_font.render(text, True, color_text)
        rect = surface_text.get_rect()
        rect.midtop = (x, y)
        self.surface.blit(surface_text, rect)

    def show_speed(self):
        self.write_text_on_game('times new roman', 20, game_variable.white, 'Speed: ' +
                                str(math.trunc(1 / self.difficulty)) + ' mm/s', game_variable.frame_size_x - 80, 15)

    def show_score(self, choice):
        x = 0
        y = 0
        if choice == 1:
            x = game_variable.frame_size_x / 10
            y = 15
        if choice == 0:
            x = game_variable.frame_size_x / 2
            y = game_variable.frame_size_y / 1.25

        Game.write_text_on_game(self, 'times new roman', 20, game_variable.white, 'Score: ' + str(self.score), x, y)

    def game_over(self):
        self.upload_data()
        self.load_data()

        while True:
            self.surface.fill(game_variable.black)
            self.write_text_on_game('times new roman', 90, game_variable.red, 'YOU DIED',
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 10 - 40)
            self.show_score(0)
            self.write_text_on_game('times new roman', 30, game_variable.white, "HIGHEST SCORE:",
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 - 20)

            self.write_text_on_game('times new roman', 20, game_variable.blue, "TOP 1: " + game_variable.name[0] +
                                    " got " + str(game_variable.score_res[0]) + "scores",
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 30)

            self.write_text_on_game('times new roman', 20, game_variable.blue,
                               "TOP 2: " + game_variable.name[1] + " got " + str(game_variable.score_res[1]) + " scores",
                               game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 70)

            self.write_text_on_game('times new roman', 20, game_variable.blue,
                               "TOP 3: " + game_variable.name[2] + " got " + str(game_variable.score_res[2]) + " scores",
                                game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 110)

            self.write_text_on_game('times new roman', 20, game_variable.blue,
                               "TOP 4: " + game_variable.name[3] + " got " + str(game_variable.score_res[3]) + " scores",
                               game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 150)

            self.write_text_on_game('times new roman', 20, game_variable.blue,
                               "TOP 5: " + game_variable.name[4] + " got " + str(game_variable.score_res[4]) + " scores",
                               game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 190)

            pygame.display.flip()
            time.sleep(5)
            game_variable.f_write.close()
            game_variable.f_read.close()
            pygame.quit()
            sys.exit()

    def game_over_condition(self):
        # Touching blocked area
        if (self.snake.snake_pos[0], self.snake.snake_pos[1]) in self.map.blocked_area:
            self.game_over()
        # Touching the snake body
        for block in self.snake.snake_body[1:]:
            if self.snake.snake_pos[0] == block[0] and self.snake.snake_pos[1] == block[1]:
                self.game_over()

    def eat_food(self):
        # bonus food
        eat_bonus = False
        if self.score % 5 == 1:
            self.food.bonus_success = True

        if self.score % 5 == 0 and self.score > 0 and self.food.bonus_success:
            self.food.bonus_food()
            if self.food.food_pos[0] == self.snake.snake_pos[0] and self.food.food_pos[1] == self.snake.snake_pos[1]:
                eat_bonus = True

        # Spawning food on the screen
        if not self.food.food_spawn:
            if self.score % 5 == 0 and self.score > 0 and self.food.bonus_success:
                self.food.change_pos_bonus()
            else:
                x = random.randrange(1, (game_variable.frame_size_x // 10)) * 10
                y = random.randrange(1, (game_variable.frame_size_y // 10)) * 10
                while (x, y) in self.map.blocked_area or x == 240 or x == 480:
                    x = random.randrange(1, (game_variable.frame_size_x // 10)) * 10
                    y = random.randrange(1, (game_variable.frame_size_y // 10)) * 10
                self.food.change_pos_food(x, y)
        self.food.food_spawn = True

        # snake grow up
        if eat_bonus:
            self.score += 30
            self.food.food_spawn = False
        if self.snake.snake_pos[0] == self.food.food_pos[0] and self.snake.snake_pos[1] == self.food.food_pos[1] \
                and not eat_bonus:
            self.score += 1
            self.food.food_spawn = False
        else:
            # if snake didn't eat food, we will pop tail out
            self.snake.snake_pop_out()

    def enter_name_layout(self):
        font = pygame.font.Font(None, 32)
        color = game_variable.white
        active = False
        input_box = pygame.Rect(game_variable.frame_size_x / 2.75, game_variable.frame_size_y / 4 + 50, 140, 32)
        color_inactive = game_variable.white
        color_active = pygame.Color(250, 250, 210)
        running_hello_layout = True

        while running_hello_layout:
            self.write_text_on_game("times new roman", 30, game_variable.white,
                                    "WELCOME TO SNAKE WORLD", game_variable.frame_size_x / 2, 30)
            self.write_text_on_game("times new roman", 20, game_variable.white,
                                    " Please enter your name: ", game_variable.frame_size_x / 2,
                                    game_variable.frame_size_y / 4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            running_hello_layout = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += event.unicode

            # Render the current text.
            txt_surface = font.render(self.player_name, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            # Blit the text.
            self.surface.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            # Blit the input_box rect.
            pygame.draw.rect(self.surface, color, input_box, 2)
            pygame.display.flip()

    def choose_level_text(self):
        self.surface.fill(game_variable.black)
        self.write_text_on_game('times new roman', 30, game_variable.white, 'Please choose level to play: ',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 10)

        self.write_text_on_game('times new roman', 20, game_variable.white, 'press 1: easy',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 30)

        self.write_text_on_game('times new roman', 20, game_variable.white, 'press 2: medium',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 60)

        self.write_text_on_game('times new roman', 20, game_variable.white, 'press 3: hard',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 90)

        self.write_text_on_game('times new roman', 20, game_variable.white, 'press 4: expert',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 120)

        self.write_text_on_game('times new roman', 20, game_variable.white, 'press 5: impossible',
                           game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 150)
        pygame.display.flip()

    #
    def choose_level_layout(self):
        choosing_level = True
        while choosing_level:

            self.choose_level_text()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.difficulty = 0.2
                        choosing_level = False
                    if event.key == pygame.K_2:
                        self.difficulty = 0.1
                        choosing_level = False
                    if event.key == pygame.K_3:
                        self.difficulty = 0.05
                        choosing_level = False
                    if event.key == pygame.K_4:
                        self.difficulty = 0.025
                        choosing_level = False
                    if event.key == pygame.K_5:
                        self.difficulty = 0.012
                        choosing_level = False

    def snake_speed_up(self):
        if self.score % 5 == 0 and self.score - game_variable.old_score != 0:
            game_variable.old_score = self.score
            self.difficulty /= 1.2

    def select_color_snake(self):
        color_snake = [game_variable.white, game_variable.red, game_variable.blue, game_variable.orange,
                       game_variable.pink, game_variable.purple]
        i = 0
        running = True
        while running:
            self.surface.fill(game_variable.black)
            self.write_text_on_game("times new roman", 30, game_variable.white, "Please choose your snake color",
                                    game_variable.frame_size_x / 2, 30)
            self.write_text_on_game("times new roman", 20, game_variable.white, "Press OK when done",
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 2 + 20)

            pygame.draw.rect(self.surface, color_snake[i],
                             (game_variable.frame_size_x / 2 - 40, game_variable.frame_size_y / 4, 80, 10))

            triagle_left = pygame.draw.polygon(self.surface, game_variable.white,
                                               points=[(340, 170), (340, 190), (330, 180)])
            triagle_right = pygame.draw.polygon(self.surface, game_variable.white,
                                                points=[(380, 170), (380, 190), (390, 180)])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if triagle_right.collidepoint(event.pos):
                        i = (i + 1) % len(color_snake)
                    if triagle_left.collidepoint(event.pos):
                        i = (i - 1) % len(color_snake)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        self.snake.snake_col = color_snake[i]

    def upload_data(self):
        if self.player_name != '' and not self.player_name.isspace():
            game_variable.f_write.write(self.player_name)
        else:
            game_variable.f_write.write("Unknown")

        game_variable.f_write.write(" ")
        game_variable.f_write.write(str(self.score))
        game_variable.f_write.write("\n")

    def load_data(self):
        for line in game_variable.f_read:
            list_data = line.split()
            if list_data:
                game_variable.name.append(list_data[0])
                game_variable.score_res.append(int(list_data[-1]))
        if self.player_name != '' and not self.player_name.isspace():
            game_variable.name.append(self.player_name)
        else:
            game_variable.name.append("Unknown")

        game_variable.score_res.append(self.score)
        for i in range(len(game_variable.name) - 1):
            for j in range(i + 1, len(game_variable.name)):
                if game_variable.score_res[i] < game_variable.score_res[j]:
                    game_variable.score_res[i], game_variable.score_res[j] = \
                        game_variable.score_res[j], game_variable.score_res[i]
                    game_variable.name[i], game_variable.name[j] = game_variable.name[j], game_variable.name[i]

    def move_map1(self, x):
        if self.map.dir_map1:
            self.map.remove_part1 += 1
        else:
            self.map.remove_part1 -= 1

        if self.map.remove_part1 == 100 or self.map.remove_part1 == game_variable.frame_size_y - 110:
            self.map.dir_map1 = not self.map.dir_map1
            print(self.map.dir_map1)
        if (x, self.map.remove_part1) in self.map.blocked_area:
            for i in range(10):
                if self.map.dir_map1:
                    if (x, self.map.remove_part1 + 10 * i) in self.map.blocked_area:
                        self.map.blocked_area.remove((x, self.map.remove_part1 + 10 * i))
                else:
                    if (x, self.map.remove_part1 - 10 * i) in self.map.blocked_area:
                        self.map.blocked_area.remove((x, self.map.remove_part1 - 10 * i))

        for i in range(10):
            if self.map.dir_map1:
                if not ((x, self.map.remove_part1 - 10 * i) in self.map.blocked_area):
                    self.map.blocked_area.append((x, self.map.remove_part1 - 10 * i))
            else:
                if not ((x, self.map.remove_part1 + 10 * i) in self.map.blocked_area):
                    self.map.blocked_area.append((x, self.map.remove_part1 + 10 * i))

    def move_map2(self, x):
        if self.map.dir_map2:
            self.map.remove_part2 += 2
        else:
            self.map.remove_part2 -= 2

        if self.map.remove_part2 == 100 or self.map.remove_part2 == game_variable.frame_size_y - 110:
            self.map.dir_map2 = not self.map.dir_map2
            print("hello")

        if (x, self.map.remove_part2) in self.map.blocked_area:
            for i in range(10):
                if self.map.dir_map2:
                    if (x, self.map.remove_part2 + 10 * i) in self.map.blocked_area:
                        self.map.blocked_area.remove((x, self.map.remove_part2 + 10 * i))
                        if not ((x, self.map.remove_part2 - 10 * i) in self.map.blocked_area):
                            self.map.blocked_area.append((x, self.map.remove_part2 - 10 * i))
                else:
                    if (x, self.map.remove_part2 - 10 * i) in self.map.blocked_area:
                        self.map.blocked_area.remove((x, self.map.remove_part2 - 10 * i))
                        if not ((x, self.map.remove_part2 + 10 * i) in self.map.blocked_area):
                            self.map.blocked_area.append((x, self.map.remove_part2 + 10 * i))

    def handle_map3(self):
        self.move_map1(240)
        self.move_map2(480)

    def choose_map_layout(self):
        choosing_map = True
        while choosing_map:
            self.surface.fill(game_variable.black)
            self.write_text_on_game('times new roman', 30, game_variable.white, 'Please choose level to play: ',
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 10)

            self.write_text_on_game('times new roman', 20, game_variable.white, 'press 1: Map 1',
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 30)

            self.write_text_on_game('times new roman', 20, game_variable.white, 'press 2: Map 2',
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 60)

            self.write_text_on_game('times new roman', 20, game_variable.white, 'press 3: Map 3',
                                    game_variable.frame_size_x / 2, game_variable.frame_size_y / 4 + 90)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.map.which_map = 1
                        choosing_map = False
                    if event.key == pygame.K_2:
                        self.map.which_map = 2
                        choosing_map = False
                    if event.key == pygame.K_3:
                        self.map.which_map = 3
                        choosing_map = False

    def map_chosen(self):
        if self.map.which_map == 1:
            self.map.map_1()
        if self.map.which_map == 2:
            self.map.map_2()
        if self.map.which_map == 3:
            self.map.map_3()

    def run_game(self):
        fps_controller = pygame.time.Clock()
        fps_controller.tick(60)
        self.map_chosen()
        while True:
            self.surface.fill(game_variable.black)
            self.snake.snake_move()
            self.snake_speed_up()
            self.eat_food()
            if self.map.which_map == 3:
                self.handle_map3()
            self.snake.draw()
            self.food.draw()
            self.map.draw()
            self.game_over_condition()
            self.show_speed()
            self.show_score(1)
            time.sleep(self.difficulty)
            # Refresh game screen
            pygame.display.update()
