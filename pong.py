import pygame
import time
import random

# COLLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 900, 500
FPS = 60

pygame.font.init()
pygame.mixer.init()
game_font = pygame.font.Font("PressStart2P-Regular.ttf", 42)

class Pong:
    def __init__(self, display):
        self.display = display
        self.isRunning = False
        self.midLine = pygame.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT)

        self.player = Player()
        self.enemy = Enemy()
        self.ball = Ball(self)

        self.points1, self.points2 = 0, 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

        keys_pressed = pygame.key.get_pressed()
        self.player.update(keys_pressed)
        self.enemy.update(self.ball.rect.y)
        self.ball.update(self.player.rect, self.enemy.rect)

    def draw(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, WHITE, self.midLine)
        self.player.draw(self.display)
        self.enemy.draw(self.display)
        self.ball.draw(self.display)

        player_text = game_font.render(f"{self.points1}", False, WHITE)
        self.display.blit(player_text, (WIDTH / 2 - 50, 50))

        enemy_text = game_font.render(f"{self.points2}", False, WHITE)
        self.display.blit(enemy_text, (WIDTH / 2 + 25, 50))

        pygame.display.update()

    def run(self):
        self.isRunning = True
        clock = pygame.time.Clock()
        while self.isRunning:
            clock.tick(FPS)
            self.update()
            self.draw()

        label = label = game_font.render("Empate!", False, WHITE)

        if self.points1 > self.points2:
            label = game_font.render("Ganhou!", False, WHITE)
        elif self.points1 < self.points2:
            label = game_font.render("Perdeu!", False, WHITE)

        self.display.blit(label, (WIDTH / 2 - 100, 200))
        pygame.display.update()
        time.sleep(1)

    def restart(self):
        self.player = Player()
        self.enemy = Enemy()
        self.ball = Ball(self)
        if self.points1 >= 5 or self.points2 >= 5:
            self.isRunning = False
        self.draw()
        time.sleep(1)

    def win(self):
        self.points1 += 1
        self.restart()

    def lost(self):
        self.points2 += 1
        self.restart()


class Player:
    VELOCITY = 5
    W, H = 8, 80

    def __init__(self):
        self.color = WHITE
        self.rect = pygame.Rect(5, (HEIGHT / 2) - (Player.H / 2), Player.W, Player.H)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)

    def update(self, keys_pressed):
        if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and self.rect.y - Player.VELOCITY > 0:
            self.rect.y -= Player.VELOCITY
        if (keys_pressed[pygame.K_s] or keys_pressed[
            pygame.K_DOWN]) and self.rect.y + Player.VELOCITY + self.rect.height < HEIGHT:
            self.rect.y += Player.VELOCITY


class Enemy:
    VELOCITY = 5
    W, H = 8, 80

    def __init__(self):
        self.color = WHITE
        self.rect = pygame.Rect(WIDTH - 5 - Enemy.W, (HEIGHT / 2) - (Player.H / 2), Player.W, Player.H)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)

    def update(self, target):
        if target < self.rect.y and self.rect.y - Player.VELOCITY > 0:
            self.rect.y -= Enemy.VELOCITY
        elif target > self.rect.y and self.rect.y + Player.VELOCITY + self.rect.height < HEIGHT:
            self.rect.y += Enemy.VELOCITY


class Ball:
    Radius = 10

    def __init__(self, game):
        self.color = WHITE
        self.game = game
        self.pong_sound = pygame.mixer.Sound("pong.ogg")
        self.score_sound = pygame.mixer.Sound("score.ogg")

        random.seed()

        self.xVelocity = -5
        self.yVelocity = random.random() * 5 + 2

        self.rect = pygame.Rect(WIDTH / 2 - 20 - Ball.Radius, HEIGHT / 2 - Ball.Radius, Ball.Radius * 2,
                                Ball.Radius * 2)

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.rect.x + Ball.Radius, self.rect.y + Ball.Radius), Ball.Radius)

    def update(self, ret1, ret2):
        if self.rect.y + self.yVelocity < 0 or self.rect.y + self.rect.height + self.yVelocity > HEIGHT:
            self.yVelocity = -self.yVelocity
        self.rect.y += self.yVelocity

        if self.rect.x + self.xVelocity < 0:
            pygame.mixer.Sound.play(self.score_sound)
            self.game.lost()

        if self.rect.x + self.rect.width + self.xVelocity > WIDTH:
            pygame.mixer.Sound.play(self.score_sound)
            self.game.win()

        self.rect.x += self.xVelocity

        if ret1.colliderect(self.rect):
            pygame.mixer.Sound.play(self.pong_sound)
            self.xVelocity *= -1
            self.xVelocity += 1
        if ret2.colliderect(self.rect):
            pygame.mixer.Sound.play(self.pong_sound)
            self.xVelocity *= -1
            if self.yVelocity > 0:
                self.yVelocity += 1
            else:
                self.yVelocity -= 1


def about(display):
    about_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)

    line1 = about_font.render("Olá, nós somos Rafael Lacerda", False, WHITE)
    line2 = about_font.render("e Gabriel Oliveira. Somos es-", False, WHITE)
    line3 = about_font.render("tudandtes do COTUCA e fizemos", False, WHITE)
    line4 = about_font.render("esse jogo em python usando a ", False, WHITE)
    line5 = about_font.render("biblioteca pygame, bom jogo!", False, WHITE)
    exit_label = about_font.render("> Exit", False, WHITE)

    exit = True
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    exit = False
        display.fill(BLACK)
        display.blit(line1, (WIDTH / 2 - 350, 50))
        display.blit(line2, (WIDTH / 2 - 350, 75))
        display.blit(line3, (WIDTH / 2 - 350, 100))
        display.blit(line4, (WIDTH / 2 - 350, 125))
        display.blit(line5, (WIDTH / 2 - 350, 150))
        display.blit(exit_label, (WIDTH- 200, 450))
        pygame.display.update()



def main():
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    play_label = game_font.render("Play", False, WHITE)
    about_label = game_font.render("About", False, WHITE)
    exit_label = game_font.render("Exit", False, WHITE)
    cursor_label = game_font.render('>', False, WHITE)

    run = True
    cursor = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and cursor > 0:
                    cursor -= 1
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and cursor < 2:
                    cursor += 1
                if event.key == pygame.K_KP_ENTER:
                    if cursor == 0:
                        game = Pong(display)
                        game.run()
                    if cursor == 1:
                        about(display)
                    if cursor == 2:
                        run = False
        display.fill(BLACK)
        display.blit(cursor_label, (WIDTH / 2 - 120, 150 + 75 * cursor))
        display.blit(play_label, (WIDTH / 2 - 75, 150))
        display.blit(about_label, (WIDTH / 2 - 75, 225))
        display.blit(exit_label, (WIDTH / 2 - 75, 300))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()

# 20154
# 20734
