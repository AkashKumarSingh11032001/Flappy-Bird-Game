import random  # random generator
import sys  # for exit using sys.exit
import pygame
from pygame.locals import *  # Basic pygame imports

# setting Basic Size

FPS = 32
ScreanWidth = 289
ScreanHeight = 511
Screan = pygame.display.set_mode((ScreanWidth, ScreanHeight))
Ground_Y = ScreanHeight * 0.8

# Gloabal Variable

Game_Sprites = {}
Game_Sound = {}

# setting material component

Player = 'gallery/sprites/bird.png'
Background = 'gallery/sprites/background.png'
Pipe = 'gallery/sprites/pipe.png'



if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()  # starting count
    pygame.display.set_caption('Flappy Bird by Simran & Akash')  # setting windows title
    Game_Sprites['numbers'] = (  # setting counts img
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    # setting Message img
    Game_Sprites['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    # setting base img
    Game_Sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    # setting pipe in two ways i.e upward face pipe and downward face pipe
    Game_Sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(), 180),  # for roataing Pipe about 180-deg
        pygame.image.load(Pipe).convert_alpha()
    )

    # # setting Game Sounds
    Game_Sound['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    Game_Sound['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    Game_Sound['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    Game_Sound['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    Game_Sound['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    Game_Sprites['background'] = pygame.image.load(Background).convert()  # setting game background img
    Game_Sprites['player'] = pygame.image.load(Player).convert_alpha()  # setting player img

    while True:
        welcomeScreen()  # show welcome screan to user until it press a button
        mainGame()  # main game screan
