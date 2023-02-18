import random
import math
import pygame
from pygame import mixer

# initializing the pygame
pygame.init()

#create screen with size 800x600
screen = pygame.display.set_mode((800, 600))

#variable for the state of the program
running = True

#background image (stars)
background = pygame.image.load('background-stars.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#change title and corner icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("project.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("space-invaders2.png")
playerX = 370
playerY = 480
# how quickly you want the spaceship to move:
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("carrot-boy.png"))
    enemyX.append(random.randint(64, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("laser-green.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# ready - you can't see the bullet on the screen
# fire - it's moving
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('Sunny Spells.ttf', 86)

#first have to render, then blit it on the screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("YOU'RE A BUTT!", True, (255, 244, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# make bullet_state global so it can be accessed inside function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# calculating distance btw bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 42:
        return True
    else:
        return False

# game loop
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 32))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # boundaries for the player movement
    if playerX <= 0:
        playerX = 0
    # 736 bc image size is 64x64 pixels, and 736 = 800 - 64
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change

    #enemy movement: if hits boundary, changes direction
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(64, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    # instatiating the player and enemy
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
