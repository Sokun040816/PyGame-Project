import pygame


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invenders')
logo = pygame.image.load(r'D:/Sokun/PyGame/Image/2. Space Inveders/ufo.png')
pygame.display.set_icon(logo)
clock = pygame.time.Clock()
FBS = 64

background = pygame.image.load(r'D:/Sokun/PyGame/Image/2. Space Inveders/background.png')
background_sound = pygame.mixer.Sound(r'D:/Sokun/PyGame/Image/2. Space Inveders/background.wav')

class Player(object):
    space = pygame.image.load(r'D:/Sokun/PyGame/Image/2. Space Inveders/player.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 7

    def key_event(self, keys):
        if keys[pygame.K_SPACE]:
            if len(bullets) < 1:
                bullets.append(Bullet(round(self.x + self.width //4  ), round(self.y + self.width // 4)))

        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.velocity
        elif keys[pygame.K_d] and self.x < WIDTH - self.width:
            self.x += self.velocity

    def draw(self, screen):
        screen.blit(self.space, (self.x, self.y))

class Bullet(object):
    shoot = pygame.image.load(r'D:/Sokun/PyGame/Image/2. Space Inveders/bullet.png')
    laser = pygame.mixer.Sound(r'D:/Sokun/PyGame/Image/2. Space Inveders/laser.wav')
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 10
    
    def draw(self, screen):
        screen.blit(self.shoot, (self.x, self.y))
    
    def bullet_rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

import random

class Enemy(object):
    enemy = pygame.image.load(r'D:/Sokun/PyGame/Image/2. Space Inveders/enemy.png')
    explosion = pygame.mixer.Sound(r'D:/Sokun/PyGame/Image/2. Space Inveders/explosion.wav')

    def __init__(self, y, width, height):
        self.width = width
        self.height = height
        self.x = random.randint(0, WIDTH - 60)
        self.y = y
        self.velocity = 5
        self.target_y = self.y + 100
        self.target_left = self.x + 100  # or set to 740 for the first move
        self.target_right = self.x 

        self.target_x = 740
        self.direction = 1 
        self.state = 'fall'
 
    def draw(self, screen):
            self.move()
            screen.blit(self.enemy, (self.x, self.y))
        
    def move(self):
        if self.state == 'fall':
            self.y += self.velocity
            if self.y >= self.target_y:
                self.y = self.target_y
                self.state = 'move'
                # Set next horizontal target
                if self.direction == 1:
                    self.target_x = 740
                else:
                    self.target_x = 30
        elif self.state == 'move':
            self.x += self.velocity * self.direction
            if (self.direction == 1 and self.x >= self.target_x) or (self.direction == -1 and self.x <= self.target_x):
                self.x = self.target_x
                self.state = 'fall'
                self.target_y = self.y + 100
                self.direction *= -1  # Reverse direction

        # Reset if off screen
        if self.y > HEIGHT:
            self.x = random.randint(0, WIDTH - 60)
            self.y = 0
            self.state = 'fall'
            self.target_y = self.y + 100
            self.direction = 1    

    def enemy_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def redraw_game():
    global monsters, score, game_over, game_start

    text_score = font.render(f'Score : {score}', True, (255,255,255))
    screen.blit(text_score,(10,10))

    # Game over if any monster reaches the bottom
    for monsters in monster:
        if monsters.y + monsters.height >= HEIGHT:
            game_over = True
            break

    if not(game_over):
        player.draw(screen)
        player.key_event(keys)

        for monsters in monster:
            monsters.draw(screen)

        for bullet in bullets[:]:
            for monsters in monster:
                if monsters.enemy_rect().colliderect(bullet.bullet_rect()):
                    score += 1
                    bullets.remove(bullet)
                    # Respawn this enemy at the top with a new random x
                    monsters.x = random.randint(0, WIDTH - monsters.width)
                    monsters.y = 0
                    monsters.state = 'fall' 
                    monsters.target_y = monsters.y + 100
                    monsters.direction = 1

                    monsters.explosion.play()
                    break  # Stop checking other enemies for this bullet

            bullet.draw(screen)
            if bullet.y > 0:   
                bullet.y -= bullet.velocity
                bullet.laser.play()
            else:
                #bullets.remove(bullet)
                bullets.pop(bullets.index(bullet))
    elif game_over:
        if game_over:
            if not pygame.mixer.get_busy():
                background_sound.play(-1)  # Loop
        else:
            background_sound.stop()
        if game_start:
            text_start = font.render('Press Enter to Start', True, (255,255,255))
            screen.blit(text_start, (WIDTH//2 - text_start.get_width()//2, HEIGHT//2 - text_start.get_height()//2))
        else:
            text_game_over = font.render('Game Over! Press Enter to play again', True, (255,255,255))
            screen.blit(text_game_over, (WIDTH//2 - text_game_over.get_width()//2, HEIGHT//2 - text_game_over.get_height()//2))

    pygame.display.update()   

player = Player(368, 500, 64, 64)

monster = [Enemy(0, 64, 64) for _ in range(5)]

bullets = []

score = 0

game_over = True
game_start = True

font = pygame.font.SysFont('Poppins', 50)


running = True
while running:

    clock.tick(FBS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if game_over and keys[pygame.K_RETURN]:
        score = 0
        monster = [Enemy(0, 64, 64) for _ in range(5)]
        bullets.clear()
        player.x, player.y = 368, 500
        game_over = False
        game_start = False  # <-- Add this line
        background_sound.stop()
    redraw_game()

    pygame.display.update()

pygame.display.quit()
