import pygame
import sys
import time
import random

# Window size
frame_size_x = 720
frame_size_y = 480
difficulty = 0

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('SNAKE')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(255, 20, 147)
orange = pygame.Color(255, 140, 0)
purple = pygame.Color(148, 0, 211)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()
fps_controller.tick(60)

# Game variables

# blocked_area = []

# Snake variable
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
direction = 'RIGHT'
snake_col = white

# food variable
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True
score = 0
bonus_success = False
eat_bonus = False
move_food_delay = False


# player name
player_name = ''
f_write = open("highscore.txt", "a")
f_read = open("highscore.txt", "r")


def write_text_on_game(font, size, color_text, text, x, y):
    my_font = pygame.font.SysFont(font, size)
    surface = my_font.render(text, True, color_text)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    game_window.blit(surface, rect)


def upload_data():
    f_write.write(player_name)
    f_write.write(" ")
    f_write.write(str(score))
    f_write.write("\n")


name = ['Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown']
score_res = [0, 0, 0, 0, 0]


def load_data():
    for line in f_read:
        list_data = line.split()
        if list_data:
            name.append(list_data[0])
            score_res.append(int(list_data[-1]))
    name.append(player_name)
    score_res.append(score)
    for i in range(len(name) - 1):
        for j in range(i + 1, len(name)):
            if score_res[i] < score_res[j]:
                score_res[i], score_res[j] = score_res[j], score_res[i]
                name[i], name[j] = name[j], name[i]


def select_color_snake():
    global snake_col
    color_snake = [white, red, blue, orange, pink, purple]
    i = 0
    running = True
    while running:
        game_window.fill(black)
        write_text_on_game("times new roman", 30, white, "Please choose your snake color", frame_size_x / 2, 30)
        write_text_on_game("times new roman", 20, white, "Press OK when done", frame_size_x / 2, frame_size_y / 2 + 20)
        pygame.draw.rect(game_window, color_snake[i], (frame_size_x / 2 - 40, frame_size_y / 4, 80, 10))
        triagle_left = pygame.draw.polygon(game_window, white, points=[(340, 170), (340, 190), (330, 180)])
        triagle_right = pygame.draw.polygon(game_window, white, points=[(380, 170), (380, 190), (390, 180)])
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
                    snake_col = color_snake[i]


def create_input_box_game():
    global player_name
    font = pygame.font.Font(None, 32)
    color = white
    active = False
    input_box = pygame.Rect(frame_size_x / 2.75, frame_size_y / 4 + 50, 140, 32)
    color_inactive = white
    color_active = pygame.Color(250, 250, 210)
    running_hello_layout = True

    while running_hello_layout:
        write_text_on_game("times new roman", 30, white, "WELCOME TO SNAKE WORLD", frame_size_x / 2, 30)
        write_text_on_game("times new roman", 20, white, " Please enter your name: ", frame_size_x / 2,
                           frame_size_y / 4)
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
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        # Render the current text.
        txt_surface = font.render(player_name, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        game_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(game_window, color, input_box, 2)

        pygame.display.flip()


# Game Over
def game_over():
    upload_data()
    load_data()

    while True:
        game_window.fill(black)
        write_text_on_game('times new roman', 90, red, 'YOU DIED', frame_size_x / 2, frame_size_y / 10 - 40)
        show_score(0)
        write_text_on_game('times new roman', 30, white, "HIGHEST SCORE:", frame_size_x / 2, frame_size_y / 4 - 20)
        write_text_on_game('times new roman', 20, blue, "TOP 1: " + name[0] + " got " + str(score_res[0]) + " scores",
                           frame_size_x / 2, frame_size_y / 4 + 30)
        write_text_on_game('times new roman', 20, blue, "TOP 2: " + name[1] + " got " + str(score_res[1]) + " scores",
                           frame_size_x / 2, frame_size_y / 4 + 70)
        write_text_on_game('times new roman', 20, blue, "TOP 3: " + name[2] + " got " + str(score_res[2]) + " scores",
                           frame_size_x / 2, frame_size_y / 4 + 110)
        write_text_on_game('times new roman', 20, blue, "TOP 4: " + name[3] + " got " + str(score_res[3]) + " scores",
                           frame_size_x / 2, frame_size_y / 4 + 150)
        write_text_on_game('times new roman', 20, blue, "TOP 5: " + name[4] + " got " + str(score_res[4]) + " scores",
                           frame_size_x / 2, frame_size_y / 4 + 190)

        pygame.display.flip()
        time.sleep(5)
        f_write.close()
        f_read.close()
        pygame.quit()
        sys.exit()


def show_speed():
    write_text_on_game('consolas', 20, white, 'Speed: ' + str(difficulty) + ' m/s', frame_size_x - 80, 15)


# Score
def show_score(choice):
    if choice == 1:
        x = frame_size_x / 10
        y = 15
    else:
        x = frame_size_x / 2
        y = frame_size_y / 1.25

    write_text_on_game('consolas', 20, white, 'Score: ' + str(score), x, y)


# choose level for game
def choose_level_text():
    game_window.fill(black)
    write_text_on_game('times new roman', 30, white, 'please choose level to play: ', frame_size_x / 8,
                       frame_size_y / 10)
    write_text_on_game('times new roman', 20, white, 'press 1: easy', frame_size_x / 2, frame_size_y / 4 + 30)
    write_text_on_game('times new roman', 20, white, 'press 2: medium', frame_size_x / 2, frame_size_y / 4 + 60)
    write_text_on_game('times new roman', 20, white, 'press 3: hard', frame_size_x / 2, frame_size_y / 4 + 90)
    write_text_on_game('times new roman', 20, white, 'press 4: expert', frame_size_x / 2, frame_size_y / 4 + 120)
    write_text_on_game('times new roman', 20, white, 'press 5: impossible', frame_size_x / 2, frame_size_y / 4 + 150)
    pygame.display.flip()


def choose_level_layout():
    choosing_level = True
    global difficulty

    while choosing_level:
        choose_level_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 30
                    choosing_level = False
                if event.key == pygame.K_2:
                    difficulty = 60
                    choosing_level = False
                if event.key == pygame.K_3:
                    difficulty = 200
                    choosing_level = False
                if event.key == pygame.K_4:
                    difficulty = 300
                    choosing_level = False
                if event.key == pygame.K_5:
                    difficulty = 500
                    choosing_level = False


def game_delay(diff):
    if diff == 30:
        return 0.1
    if diff == 60:
        return 0.05
    if diff == 200:
        return 0.02
    if diff == 300:
        return 0.01
    if diff == 500:
        return 0

    return 0


def snake_move():
    global direction
    change_to = str()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # add position of snake's head to snake's body
    snake_body.insert(0, list(snake_pos))


def food_and_bonus():
    global food_pos
    global eat_bonus
    global bonus_success
    global food_spawn
    global score

    direction_food = ["UP", "DOWN", "RIGHT", "LEFT"]
    eat_bonus = False
    if score % 5 == 1:
        bonus_success = True

    if score % 5 == 0 and score >= 5 and bonus_success:
        ran = random.randrange(0, 4)
        if direction_food[ran] == "UP":
            food_pos[1] -= 10
        if direction_food[ran] == "DOWN":
            food_pos[1] += 10
        if direction_food[ran] == "RIGHT":
            food_pos[0] += 10
        if direction_food[ran] == "LEFT":
            food_pos[0] -= 10
        if food_pos[0] == snake_pos[0] and food_pos[1] == snake_pos[1]:
            eat_bonus = True
        if food_pos[0] < 0 or food_pos[0] > frame_size_x - 10 or food_pos[1] < 0 or food_pos[1] > frame_size_y - 10:
            food_spawn = False
            bonus_success = False

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    # snake grow up
    if eat_bonus:
        score += 5
        food_spawn = False
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1] and not eat_bonus:
        score += 1
        food_spawn = False
    else:
        # if snake didn't eat food, we will pop tail out
        snake_body.pop()


def draw():
    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, snake_col, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    # game_window.blit(apple, (food_pos[0], food_pos[1]))
    pygame.draw.rect(game_window, green, pygame.Rect(food_pos[0], food_pos[1], 10, 10))


def game_over_condition():
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()


# Main logic
if __name__ == '__main__':

    create_input_box_game()
    select_color_snake()
    choose_level_layout()

    while True:
        # handle snake
        snake_move()

        # handle food and score of game
        food_and_bonus()

        # modify game difficulty
        time.sleep(game_delay(difficulty))

        # draw snake and food
        draw()

        # game over
        game_over_condition()

        # showing speed on screen while playing
        show_speed()

        # showing score on screen while playing
        show_score(1)
        pygame.display.flip()

        # Refresh game screen
        pygame.display.update()
