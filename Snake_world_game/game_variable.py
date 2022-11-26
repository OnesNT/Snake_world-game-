import pygame

# Window size
frame_size_x = 720
frame_size_y = 480

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(255, 20, 147)
orange = pygame.Color(255, 140, 0)
purple = pygame.Color(148, 0, 211)

# Player variable
f_write = open("highscore.txt", "a")
f_read = open("highscore.txt", "r")
name = ['Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown']
score_res = [0, 0, 0, 0, 0]
old_score = 0
