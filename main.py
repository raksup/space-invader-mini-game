import pygame
import random
import math

from pygame import mixer


#Initialization of pygame
pygame.init()
#Create the Screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('background.jpg')

#Music and Audio Effects
bullet_Sound = mixer.Sound('laser.wav')
bullet_Sound.set_volume(0.1)
collision_Sound = mixer.Sound('explosion.wav')
collision_Sound.set_volume(0.1)

#Title and Icon
pygame.display.set_caption("Space Saver")
icon = pygame.image.load('sicon.png')
pygame.display.set_icon(icon)

#Player Image
playerImg = pygame.image.load('player_icon.png')
playerX = 365
playerY = 500
playerX_change = 0

# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy_icon.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(30)

#Bullet   state(ready)- not visible      state(fire)- moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 7
bullet_state = "ready"

#Game Score Counter
score_val = 0
font = pygame.font.SysFont("comicsansms", 32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_val), True, (0,255,0))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((bulletY - enemyY), 2) + math.pow((bulletX - enemyX), 2))
    if distance <= 27:
        return True
    else:
        return False

#game over function
over_font = pygame.font.SysFont("comicsansms", 64)
def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300,250))


#Game Loop
running = True
while running:
    #RGB Values
    screen.fill((1,1,1))
    #Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If keystroke is pressed, check whether left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    #Checking and restricting boundary for player and enemy
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_enemies):

        # Game Over
        if enemyY[i] > 480:
            for j in range(num_enemies):
                enemyY[j] = 900
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collission = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collission:
            collision_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_val += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 10:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()