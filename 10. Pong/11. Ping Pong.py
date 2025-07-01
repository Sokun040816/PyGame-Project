import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong')
icon = pygame.image.load(r'D:/Sokun/PyGame/Image/10. Pong/icon.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont(None, 72)  # You can change size as needed

score_1 = 0
score_2 = 0

clock = pygame.time.Clock()
FPS = 64


SOFT_RED = (249, 84, 84)
BRIGHT_BLUE = (13, 146, 244)
MOSS_GREEN = (159, 200, 126)
DEEP_RED = (198, 46, 46)



class Player_1(object):
    def __init__(self):
        self.width = 25
        self.height = 125
        self.x = 700
        self.y = HEIGHT // 2 - self.height // 2
        self.velocity = 7
    
    def draw(self):
        self.event_key(keys)
        #self.collision(circle_x, circle_y, radius, rect)

        return pygame.draw.rect(screen, SOFT_RED, (self.x, self.y, self.width, self.height))
    
    def event_key(self, keys):

        if keys[pygame.K_SPACE]:

            global score_1, score_2
            if ball.x + ball.radius < 0 :
                # Respawn toward player_1 (right) after 3 seconds
                ball.x = WIDTH // 2 - ball.radius // 2
                ball.y = HEIGHT // 2 - ball.radius // 2
                ball.velocity_x = 20
                ball.velocity_y = 5
                score_1 += 1

            elif ball.x - ball.radius > WIDTH :
                # Respawn toward player_2 (left) after 3 seconds
                ball.x = WIDTH // 2 - ball.radius // 2
                ball.y = HEIGHT // 2 - ball.radius // 2
                ball.velocity_x = -20
                ball.velocity_y = 5
                score_2 += 1

        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.velocity
        elif keys[pygame.K_s] and self.y < HEIGHT - self.height:
            self.y += self.velocity

class Player_2(object):
    def __init__(self):
        self.width = 25
        self.height = 125
        self.x = 100
        self.y = HEIGHT // 2 - self.height // 2
        self.velocity = 5
    
    def draw(self):
        return pygame.draw.rect(screen, BRIGHT_BLUE, (self.x, self.y, self. width, self.height))

    def AI_move(self):
        paddle_center = self.y + self.height // 2
        distance = ball.y - paddle_center
        
        if abs(distance) > self.velocity:
            self.y += self.velocity if distance > 0 else -self.velocity
        else:
            self.y += distance
        self.y = max(0, min(HEIGHT - self.height, self.y))


class Ball(object):
    def __init__(self):
        self.radius = 15
        self.x = WIDTH // 2 - self.radius // 2
        self.y = HEIGHT // 2 - self.radius // 2
        self.velocity_x = 20
        self.velocity_y = 5

        self.waiting = True
        self.wait_start_time = 0
    
    def draw(self):
        ball.move()
        ball.bound_player(player_1)
        ball.bound_player(player_2)
        ball.bound_wall()
        
        return pygame.draw.circle(screen, DEEP_RED,(self.x, self.y), self.radius)
    
    def move(self):
        
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def bound_player(self, player):
        # Ball hits player paddle
        player_rect = player.draw()
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
        if player_rect.colliderect(ball_rect):
            # Ball is moving right (toward player_1)
            if self.velocity_x > 0:
                self.x = player.x - self.radius  # Place ball to the left of the paddle
            # Ball is moving left (toward player_2)
            else:
                self.x = player.x + player.width + self.radius  # Place ball to the right of the paddle

            self.velocity_x *= -1
            offset = (self.y - (player.y + player.height // 2))
            self.velocity_y += int(offset // 8)
            max_speed = 5
            self.velocity_y = max(-max_speed, min(max_speed, self.velocity_y))

    def bound_wall(self):
        # Bounce off top wall
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity_y *= -1
            

        # Bounce off bottom wall
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.velocity_y *= -1

def redraw_game():

    player_1.draw()
    player_2.draw()
    player_2.AI_move()
    ball.draw()

    # Render updated scores
    text_score_1 = font.render(str(score_1), True, SOFT_RED)
    text_score_2 = font.render(str(score_2), True, BRIGHT_BLUE)
    screen.blit(text_score_1, (WIDTH - 50, 100))
    screen.blit(text_score_2, (50, 100))

    if ball.x + ball.radius > 0 and ball.x - ball.radius > WIDTH :
        font_round = pygame.font.SysFont('Popins', 50)
        text_round = font_round.render(('Press Space for go Next round'), True, BRIGHT_BLUE)
        text_rect = text_round.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_round, text_rect)

    pygame.display.update()


player_1 = Player_1()
player_2 = Player_2()
ball = Ball()

running = True
while running:
    screen.fill(MOSS_GREEN)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    redraw_game()

pygame.quit()