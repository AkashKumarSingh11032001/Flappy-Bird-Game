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


# this function help to show welcome screan !!!

def welcomeScreen():


    playerx = int(ScreanWidth / 5)
    playery = int((ScreanHeight - Game_Sprites['player'].get_height()) / 2)
    messagex = int((ScreanWidth - Game_Sprites['message'].get_width()) / 2)
    messagey = int(ScreanHeight * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                Screan.blit(Game_Sprites['background'], (0, 0))
                Screan.blit(Game_Sprites['player'], (playerx, playery))
                Screan.blit(Game_Sprites['message'], (messagex, messagey))
                Screan.blit(Game_Sprites['base'], (basex, Ground_Y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# main function (major part of game ~ analytical calculation)

def mainGame():
    score = 0 # score to 0
    playerx = int(ScreanWidth / 5) # setting player(bird) at center
    playery = int(ScreanWidth / 2) # setting player(bird) at center
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': ScreanWidth + 200, 'y': newPipe1[0]['y']},
        {'x': ScreanWidth + 200 + (ScreanWidth / 2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': ScreanWidth + 200, 'y': newPipe1[1]['y']},
        {'x': ScreanWidth + 200 + (ScreanWidth / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping
    # internship2020 #lpu
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    Game_Sound['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + Game_Sprites['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + Game_Sprites['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                Game_Sound['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = Game_Sprites['player'].get_height()
        playery = playery + min(playerVelY, Ground_Y - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -Game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        Screan.blit(Game_Sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screan.blit(Game_Sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            Screan.blit(Game_Sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        Screan.blit(Game_Sprites['base'], (basex, Ground_Y))
        Screan.blit(Game_Sprites['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Game_Sprites['numbers'][digit].get_width()
        Xoffset = (ScreanWidth - width) / 2

        for digit in myDigits:
            Screan.blit(Game_Sprites['numbers'][digit], (Xoffset, ScreanHeight * 0.12))
            Xoffset += Game_Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# setting Collider, that means that we basically setting the limit that how bird will die after touching pipe

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > Ground_Y - 25 or playery < 0:
        Game_Sound['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = Game_Sprites['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < Game_Sprites['pipe'][0].get_width()):
            Game_Sound['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + Game_Sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                Game_Sprites['pipe'][0].get_width():
            Game_Sound['hit'].play()
            return True

    return False




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
