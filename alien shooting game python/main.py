import pygame
import math
import random
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien Shooter")

font=pygame.font.Font("freesansbold.ttf",32)
score_val = 0

text_x=10
text_y=10

#Player
player_x = 380
player_y = 480
velocity = 0
player_image = pygame.image.load('spaceship.png')

#alien
num_of_aliens = 5
alien_img = pygame.image.load('alien.png')
aliens = []
velocity_aliens = []

for i in range(num_of_aliens):
    aliens.append([random.randint(0, width - 64), random.randint(30, 150)])
    velocity_aliens.append(0.2)


#bullet
bullet_image = pygame.image.load('bullet.png')
bullets = []
fire_delay = 200
bullet_timer = pygame.time.get_ticks()
bullet_velocity = -0.5


def player(x, y):
    screen.blit(player_image, (x, y))
def alien(x, y):
    screen.blit(alien_img, (x, y))
def fire_bullet(x, y):
    screen.blit(bullet_image, (x + 16, y + 10))
def isCollision(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by) < 27
def score(x,y):
    score=font.render("score = "+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))



# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                velocity = 0.3
            elif event.key == pygame.K_LEFT:
                velocity = -0.3
    if event.type == pygame.KEYUP:
        if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
            velocity = 0

    player_x += velocity
    if player_x < 0:
        player_x = 0
    elif player_x > width - 64:
        player_x = width - 64

    for i in range(num_of_aliens):
        aliens[i][0] += velocity_aliens[i]
        if aliens[i][0] <= 0:
            velocity_aliens[i] = 0.2
            aliens[i][1] += 30
        elif aliens[i][0] >= width - 64:
            velocity_aliens[i] = -0.2
            aliens[i][1] += 30
        alien(aliens[i][0], aliens[i][1])

    current_time = pygame.time.get_ticks()
    if current_time - bullet_timer > fire_delay:
        bullets.append([player_x + 16, player_y])
        bullet_timer = current_time

    for b in bullets[:]:
        b[1] += bullet_velocity
        fire_bullet(b[0], b[1])
        if b[1] < 0:
            bullets.remove(b)
        else:
            for i in range(num_of_aliens):
                if isCollision(aliens[i][0], aliens[i][1], b[0], b[1]):
                    try:
                        bullets.remove(b)
                    except ValueError:
                        pass
                    score_val += 1
                    
                    aliens[i] = [random.randint(0, width - 64), random.randint(30, 150)]

    player(player_x, player_y)
    score(text_x,text_y)
    pygame.display.update()

pygame.quit()

