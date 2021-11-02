# Simple pygame program
# Import and initialize the pygame library
import pygame
import random
import os
import sqlite3
from sqlite3 import Error

pygame.font.init()

directory_carpeta = os.path.dirname(__file__)
ruta_score = os.path.join(directory_carpeta,"resources/score.txt")
ruta_jet = os.path.join(directory_carpeta,"resources/jet.png")
ruta_missile = os.path.join(directory_carpeta,"resources/missile.png")
ruta_cloud = os.path.join(directory_carpeta,"resources/cloud.png")
ruta_laser = os.path.join(directory_carpeta,"resources/laser.png")
ruta_apoxode = os.path.join(directory_carpeta,"resources/Apoxode_-_Electric_1.ogg")
ruta_collision = os.path.join(directory_carpeta,"resources/Collision.ogg")
ruta_falling = os.path.join(directory_carpeta,"resources/Falling_putter.ogg")
ruta_rising = os.path.join(directory_carpeta,"resources/Rising_putter.ogg")
ruta_max_score = os.path.join(directory_carpeta, "puntuacion.db")

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT,
K_ESCAPE,
K_SPACE,
K_p,
KEYDOWN,
QUIT,
RLEACCEL
)

# Level
level = 1
#Score
global score
score = 0
#Time
time = 500
#Lives
lives = 3

#Fuente
font_game = pygame.font.SysFont("comicsans",30)
font_intro = pygame.font.SysFont("comicsans", 50)
font_end = pygame.font.SysFont("comicsans", 80)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((75, 25))
        #self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load(ruta_jet).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.sonidoRising = pygame.mixer.Sound(ruta_rising)
        self.sonidoFalling = pygame.mixer.Sound(ruta_falling)


    # Move the sprite based on user keypresses
    def update(self, pressed_keys):            
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.sonidoRising.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.sonidoFalling.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((20, 10))
        #self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load(ruta_missile).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
                )
        )
        v_a = 2 * level
        v_b = 10 + (3 * level)
        self.speed = random.randint(v_a, v_b)   

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        global score
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            score = score + 20
#Clase Cloud
class Cloud(pygame.sprite.Sprite):            
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(ruta_cloud).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
                )
        )
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
#Clase Misil
class Misil(pygame.sprite.Sprite):
    def __init__(self):
        super(Misil, self).__init__()
        self.surf = pygame.image.load(ruta_laser).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    def update(self):
        self.rect.x += 10
            
# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load(ruta_apoxode)
pygame.mixer.music.play(loops=-1)

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Create a custom event for adding a new cloud      
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#Create a custom event for background
CHANGE_BACKGROUND = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_BACKGROUND, 20000)
rgb_current = (135, 206, 250)

# Instantiate player.
player = Player()

def connexion():
    try:
        sqliteConnection = sqlite3.connect((os.path.join(ruta_max_score)))
        return sqliteConnection
    except Error:
        print(Error)

con = connexion()

def leersql():
    cursor = con.cursor()
    cursor.execute("SELECT score FROM puntuacion")
    row = cursor.fetchone()
    return row[0]

def updatesql():
    curs = con.cursor()
    if leersql() < score:
        curs.execute("update puntuacion set score = "+str(score))
        print("Nuevo high score:")
        curs.execute("select * from puntuacion")
        con.commit()
        row = curs.fetchone()
        print(row[0])
 
def sql_insert(score):
    cursorobj = con.cursos()
    if leersql() == 0:
        cursorobj.execute(
            'INSERT INTO puntuacion VALUES({})'.format(score))
    if leersql > score:
        return
    else:
        updatesql()

    con.comit()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()  
laser_list = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True
background = True
intro = True
end = True

#Menu intro
while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((0,0,0))
    intro_label = font_intro.render("Press p to play", 1, (0,150,0))
    screen.blit(intro_label,(225, 200))

    scoremax_label = font_intro.render(f"Score Max: {leersql()}", 1, (0,150,0))
    screen.blit(scoremax_label, (200, 300))

    tecla = pygame.key.get_pressed()

    if tecla[pygame.K_p]:
        intro = False
    pygame.display.update()

# Main loop
while running:
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)

    time = int(200 + ( 1000 / level))

    level = int(score/50)
    if level < 1:
        level = 1
        
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:

            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                laser = Misil()
                laser.rect.x = player.rect.x 
                laser.rect.y = player.rect.y 

                laser_list.add(laser)
                all_sprites.add(laser)
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        # Add a new enemy?
        elif event.type == ADDENEMY:
            #Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(enemies)

        elif event.type == ADDCLOUD:
            #Create clouds
            new_cloud = Cloud()
            clouds.add(new_cloud) 
            all_sprites.add(clouds)

        elif event.type == CHANGE_BACKGROUND:
            print("Background")
            if background is True:
                print("True -> False")
                background = False
                rgb_current = 0, 0, 0
            elif background is False:
                print("False -> True")
                background = True
                rgb_current = 135, 206, 250
    

    for laser in laser_list:
        meteor_hit_list = pygame.sprite.spritecollide(laser, enemies, True)
        for meteor in meteor_hit_list:
            all_sprites.remove(laser)
            laser_list.remove(laser)
            score += 2
            print(score)
        if laser.rect.x < -10:
            all_sprites.remove(laser)
            laser_list.remove(laser)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    laser_list.update()

    # Update cloud position
    clouds.update()

    # Update screen day/night
    screen.fill(rgb_current)

    # Put text on screen ( level )
    level_label = font_game.render(f"Level: {level}", 1, (255,255,255))
    screen.blit(level_label, (620,10))

    # Put text on screen ( score )
    score_label = font_game.render(f"Score: {score}", 1, (255,255,255))
    screen.blit(score_label, (620,50))

    # Put text on screen ( lives )
    lives_label = font_game.render(f"Lives: {lives}", 1, (255,255,255))
    screen.blit(lives_label, (620,90))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Check if any enemies have collided with the player
    if pygame.sprite.spritecollide(player, enemies, True):
        #If so, then remove the player and stop the loop
        sonidoCollision = pygame.mixer.Sound(ruta_collision)
        sonidoCollision.play()
        
        lives -= 1
    
        if lives == 0:

            connexion()
            print("Puntuació máxima: ",leersql())
            updatesql()
            
            player.kill()
            running = False
            pygame.mixer.music.stop()

    # Update the display
    pygame.display.flip()

#GameOver
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        screen.fill((0,0,0))
        gameover_label = font_intro.render("GAME OVER", 1, (0,150,0))
        endscore_label = font_game.render(f"Score: {score}", 1, (0,150,0))
        screen.blit(gameover_label,(250, 200))
        screen.blit(endscore_label,(300, 300))

        pygame.display.update()

pygame.mixer.quit()
pygame.quit()