# Game where a spaceship tries to stay alive and destroy as many Aliens as possible
__author__ = "Alex Shaikh"
__version__ = "2.9.2026"

player = "Alex" # this changes the name that will appear when you submit your scores

import pygame
from pygame.constants import *
import random

# for my extra on this game I included the ability to fire a huge laser once every 18s by pressing x
# this laser does not despawn on contacting aliens and has indicator in the bottom when you can fire it

# this will add aliens until it reaches the count
# stores them along with the velocity in the list aliens
# I decided to have the aliens spawn a random position off the top of screen
# I did this so it adds an element of randomness so they don't all drop at once
def addAliens(aliens,window, count,cochran):
    while len(aliens) < count:
        temp = cochran.get_rect()
        temp.x = random.randint(0, window.get_width()-50)
        temp.y = -random.randint(0,400)
        velocity = random.randint(1,4)
        aliens.append([temp,velocity])

# will draw the hearts to the screen
# will use the amount described in hearts
# applies an offset of 30 pixels
def drawHearts(hearts,window):
    positionX = 30
    for heart in range(hearts):
        pygame.draw.rect(window, (0, 255, 0), (positionX, 770, 20, 20))
        positionX += 30

# This will draw the score to the bottom right of the screen
def drawScore(score,window):
    font = pygame.font.Font(None, 22)
    text_surface = font.render("Score: %d"%score, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(700, 770))
    window.blit(text_surface, text_rect)

# This occurs when the player loses
# This draws the player's score to the screen
def gameOver(window, size, score):
    font = pygame.font.Font(None, 22)
    text_surface = font.render("Game Over Your Score Was: %d" % score, True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(size[0]//2, size[1]//2))
    window.blit(text_surface, text_rect)


# this reads the score.txt document and stores the score and the player name in scores.
# this returns the list of scores
def readScrores():
    handle = open('score.txt', 'r')
    scores = []
    for line in handle:
        line = line.strip()
        scores.append([int(line[line.find("%")+1:]), line[:line.find("%")-1]])
    handle.close()
    return scores

# This will write the previous score to the score.txt document
# first it adds the score to the list then sorts it by the highest scores
# It then writes every score in the list separated by %
def writeScore(score,scores):

    scores.append([score, player])
    scores.sort()
    scores.reverse()
    handle = open('score.txt', 'w')
    for score in scores:
        handle.write(score[1] + " %"+ str(score[0]) + "\n")
    handle.close()

def main():
    # Initialize pygame engine
    pygame.init()
    # set up the window size
    size = (800, 800)

    # initialize the display
    window = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)
    pygame.display.set_caption("Tower Defense")

    #fps
    clock = pygame.time.Clock()
    # keep the animation going
    running = True
    # controls how fast you are able to fire your laser
    smallLaserTime = 0
    #Controls how fast you are able to fire your big laser
    bigLaserTime = 0
    # This controls how long to wait before spawning another alien
    stopwatch = 0
    # how many aliens to spawn. starts at 2 at a time.
    alienCount = 2
    # how long to wait before spawning another alien.
    difficultyUp = 1200
    # start the mixer and get the sound
    pygame.mixer.init()
    # get all the sounds
    laserSound = pygame.mixer.Sound('sound/laser.wav')
    laserSound.set_volume(0.3) # the regular laser was very loud and made my ears hurt so I turned it down
    boomSound = pygame.mixer.Sound('sound/boom1.wav')
    bigLaserSound = pygame.mixer.Sound('sound/bigLaser.wav')

    # get all the images
    shipImage = pygame.image.load('img/spaceship.png')
    alienImg = pygame.image.load('img/alien1.png')
    alienImgResized =  pygame.transform.scale(alienImg, (50, 50)) # set the right size for the alien
    ship = shipImage.get_rect()
    # The amount of hearts the player has
    hearts = 3
    # the players score
    score = 0
    #stores the alien rects and velocity
    aliens = []
    # stores the laser rects, laser type , and laser fire time till deletion
    lasers = []
    # initialize the scores
    scores = readScrores()
    # add the initial aliens
    addAliens(aliens,window,alienCount,alienImgResized)

    # centered in window
    ship.x = window.get_width()//2- shipImage.get_width()//2
    ship.y = window.get_height()-120

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # collects inputs
        key = pygame.key.get_pressed()
        # check for inputs and move the player square
        smallLaserTime-=1
        bigLaserTime-=1
        # if you press the spacebar and the cooldown is passed
        if key[K_SPACE] and smallLaserTime <= 0:
            smallLaserTime = 20
            laserSound.play()
            lasers.append([pygame.Rect(ship.x+20, ship.y, 10, 10),60,1])
            # index number 1 ( the number 60 in this case) represents how long until the laser is removed
            # Index number 2(the number 1 in this case) represents the laser type (1 = small, 2 = big)
        # press the x button
        if key[K_x] and bigLaserTime <= 0:
            bigLaserTime = 1080 # can fire every 18s
            bigLaserSound.play()
            lasers.append([pygame.Rect(ship.x+20, ship.y-675, 13, 675),120,2])
            # index number 1 ( the number 120 in this case) represents how long until the laser is removed
            # Index number 2(the number s in this case) represents the laser type (1 = small, 2 = big)

        # updates the ship position
        if key[K_LEFT]:
            ship.move_ip(-8, 0)
        if key[K_RIGHT]:
            ship.move_ip(8, 0)
        # clamp ship
        ship.clamp_ip(window.get_rect())
        window.fill((0, 0, 0))
        # display ship
        window.blit(shipImage, ship)

        for laser in lasers:
            laser[1] -=1 # reduces the timer of the laser
            if laser[2] == 1:
                laser[0].move_ip(0, -15) # if small laser move it up
            else:
                laser[0].x = ship.x+20 # if big update its position to the ships x position
            if laser[1] < 0:
                lasers.remove(laser) # if its timer runs out, delete it
            else:
                # draw the laser
                pygame.draw.rect(window, (255, 0, 0), laser[0])

        for alien in aliens:
            # move the alien down by its velocity
            alien[0].move_ip(0, alien[1])
            window.blit(alienImgResized,alien[0]) # draw the alien
            if alien[0].y > 800: # if it goes off-screen then delete it and lose a heart
                aliens.remove(alien)
                hearts -= 1
                break
            if alien[0].colliderect(ship): # if it collides with the ship remove the alien and lose a heart
                aliens.remove(alien)
                boomSound.play()# also play a sound
                hearts -= 1

            for laser in lasers: # checking for collision
                if alien[0].colliderect(laser[0]):
                    aliens.remove(alien) # remove the alien and increase the score
                    score += 1
                    if laser[2] == 1: # if it is a small laser remove the laser
                        lasers.remove(laser)
        stopwatch += 1
        if stopwatch >= difficultyUp: # upon the required time increase the number of aliens
            difficultyUp += 200 # increase the amount time to add another alien
            # I found it more fun to play when the time of the difficulty increases
            stopwatch = 0
            alienCount += 1
        if bigLaserTime <= 0: # draws a red box to indicate that the big laser can be used
            pygame.draw.rect(window, (255, 0, 0), (0,770,20,20))
        # draws the hearts and the score
        drawHearts(hearts,window)
        drawScore(score,window)
        if hearts == 0: # stop running if you run out of lives
            running = False
        addAliens(aliens,window,alienCount,alienImgResized)# add the aliens
        pygame.display.flip()# update the display
        clock.tick(60)# frames
    # after the death write the scores to the file
    writeScore(score,scores)
    if score == scores[0][0]: # determines if the previous score is the high score
         hasHighScore = True
    else:
        hasHighScore = False

    running2 = True
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN: # quits on mouse click
                running2 = False

        window.fill((0, 0, 0))
        if hasHighScore: # if you have the high score indicate so
            font = pygame.font.Font(None, 22)
            text_surface = font.render("You Got the HighScore of %d" % score, True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(size[0] // 2, (size[1] //2)-50))
            window.blit(text_surface, text_rect)
        else: # if you did not indicate the high score and who set it
            font = pygame.font.Font(None, 22)
            text_surface = font.render("The High Score Is %d set by %s" % (scores[0][0],scores[0][1]) , True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(size[0] // 2, (size[1] // 2) - 50))
            window.blit(text_surface, text_rect)

        gameOver(window,size,score)

        pygame.display.flip()
    pygame.quit()




if __name__ == '__main__': # main entry point
    main()
