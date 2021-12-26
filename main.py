import pygame
from pygame import mixer
import random
import math


# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")        # game caption
icon = pygame.image.load('ufo.png')     # puts picture in icon variable
pygame.display.set_icon(icon)       # chooses game icon

# background
background = pygame.image.load('background.png')     # puts picture in background variable

# background sound
mixer.music.load('background.wav')      # loads in long sound file
mixer.music.play(-1)        # makes sound play in loop

# player
playerImg = pygame.image.load('spaceship.png')      # puts picture in variable
playerX = 370       # sets start X coordinates
playerY = 480       # sets start Y coordinates
playerX_change = 0      # creates a change variable for movement

# enemy
enemyImg = []       # empty list for enemy figure
enemyX = []     # empty list for enemy X coordinates
enemyY = []     # empty list for enemy Y coordinates
enemyX_change = []      # empty list for enemy movement along the X axis
enemyY_change = []      # empty list for enemy movement along the Y axis
num_of_enemies = 6      # declaring number of enemies in this variable


for i in range(num_of_enemies):     # loop that goes once for each enemy
    enemyImg.append(pygame.image.load('enemy.png'))     # appends image to list
    enemyX.append(random.randint(0, 735))       # appends random X coordinates for enemy to list
    enemyY.append(random.randint(50, 150))      # appends random Y coordinates for enemy to list
    enemyX_change.append(4)     # sets and appends movement speed for enemy to list
    enemyY_change.append(40)        # appends change in position when enemy hits border


# bullet
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')     # puts bullet image in variable
bulletX = 0     # creates X coordinate variable for bullet
bulletY = 480       # creates Y coordinate variable for bullet
bulletX_change = 2
bulletY_change = 15     # bullet velocity along Y axis when fired. Number of pixels moved each loop iteration
bullet_state = "ready"      # ready - you can't see the bullet on the screen

# score
score_value = 0     # variable to hold the score
font = pygame.font.Font('freesansbold.ttf', 32)     # variable to hold font information

# text position
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)     # variable to hold font information

# show score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))     #rendering the font variable and adding score_value
    screen.blit(score, (x, y))      # blit the score variable

# show game over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# player creation
def Player(x, y):
    screen.blit(playerImg, (x, y))      # blit player character

# enemy creation
def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))        # blit enemies from enemyImg list

# bullet fire function
def fire_bullet(x, y):
    global bullet_state     # make the variable global and accessible inside function
    bullet_state = "fire"       # fire - bullet is fired from spaceship
    screen.blit(bulletImg, (x + 16, y + 10))        # blit bullet on screen

# collision detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))     # calculating distance between objects
    if distance < 27:       # if distance is less than
        return True
    else:       # if distance is more
        return False


# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    # pygame events in this loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')     # add sound to variable
                    bullet_sound.play()     # play sound if space if bullet is fired
                    bulletX = playerX       # get the current coordinate of the spaceship
                    fire_bullet(bulletX, bulletY)

        # checking if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # add value from keystroke to position
    playerX += playerX_change

    # checking for boundaries for spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:     # if an enemy is too close to spaceship
            for j in range(num_of_enemies):     # go through all enemies
                enemyY[j] = 2000        # move each enemy out of picture
            game_over_text()        # when all enemies are gone, show text
            break       # break out of loop

        # move enemy along X axis by the amount in variable
        enemyX[i] += enemyX_change[i]

        # checking for boundaries for alien
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        Enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    Player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
