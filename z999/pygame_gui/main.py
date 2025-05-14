import pygame
from pygame.locals import *
import sys
import random

BLACK = (100, 100, 100)
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FRAMES_PER_SEC = 30
BALL_WIDTH_HEIGHT = 123
MAX_WIDTH = WINDOW_WIDTH - BALL_WIDTH_HEIGHT
MAX_HEIGHT = WINDOW_HEIGHT - BALL_WIDTH_HEIGHT
TARGET_X = 400
TARGET_Y = 320
TARGET_WIDTH_HEIGHT = 120
N_PIXELS_TO_MOVE = 3


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
ballImage = pygame.image.load('images/ithome_logo_0.png')

ballX = random.randrange(MAX_WIDTH)
ballY = random.randrange(MAX_HEIGHT)
ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONUP:
            if ballRect.collidepoint(e.pos):
                ballX = random.randrange(MAX_WIDTH)
                ballY = random.randrange(MAX_HEIGHT)
                ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)

    window.fill(BLACK)
    window.blit(ballImage, (ballX, ballY))
    pygame.display.update()
    clock.tick(FRAMES_PER_SEC)