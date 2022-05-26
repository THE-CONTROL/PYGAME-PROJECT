import pygame
from pygame.locals import*
import random
pygame.init()

screen = pygame.display.set_mode((876, 657), )
pygame.display.set_caption("NORTHERN LIGHTS")
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
pygame_icon = pygame.image.load('opening bg.jpg')
pygame.display.set_icon(pygame_icon)

flying_player = [pygame.image.load("Fly (1).png").convert(), pygame.image.load("Fly (2).png").convert()]
shooting_player = [pygame.image.load("Shoot (1).png").convert(), pygame.image.load("Shoot (2).png").convert(),
                   pygame.image.load("Shoot (3).png").convert(), pygame.image.load("Shoot (4).png").convert(),
                   pygame.image.load("Shoot (5).png").convert()]
dead_player = pygame.image.load("Dead (1).png").convert()
background1 = pygame.image.load("BG.png")
background2 = pygame.image.load("opening bg.jpg")

move_count = 0
score = 0

font = pygame.font.SysFont("pacifico", 27, True)
font1 = pygame.font.SysFont("quicksand", 14, True)
font2 = pygame.font.SysFont("georgia", 40, True)

pygame.mixer.music.load("Lana Del Rey – Watercolor Eyes.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_pos(4)
bullet_sound = pygame.mixer.Sound("gun-gunshot-01.wav")
hit_sound = pygame.mixer.Sound("gun-gunshot-02.wav")


def hit():
    if player.health > 0:
        player.health -= 1
    else:
        player.alive = False


def dead():
    player.surf.blit(dead_player, (player.rect.left, player.rect.top))
    end_text = font.render(f"GAME OVER!", True, (0, 0, 0))
    end_text_rect = end_text.get_rect()
    screen.blit(end_text, (screen_rect.centerx - end_text_rect.centerx,
                           screen_rect.centery - (end_text_rect.centery + 50)))
    end_text1 = font.render(f"Your Score: {score}", True, (0, 0, 0))
    end_text1_rect = end_text1.get_rect()
    screen.blit(end_text1, (screen_rect.centerx - end_text1_rect.centerx,
                            screen_rect.centery - end_text1_rect.centery))
    end_text2 = font.render("Press HOME to play again and ESC to quit...", True, (0, 0, 0))
    end_text2_rect = end_text2.get_rect()
    screen.blit(end_text2, (screen_rect.centerx - end_text2_rect.centerx,
                            screen_rect.centery - end_text2_rect.centery + 50))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((89, 61))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.health = 10
        self.alive = True

    def update(self):
        global move_count
        pressed_keys = pygame.key.get_pressed()

        if move_count + 1 >= 20:
            move_count = 0

        if not player.alive:
            player.surf.blit(shooting_player[move_count // 4], (0, 0))

        if pressed_keys[K_UP]:
            if self.rect.top <= 20:
                player.surf.blit(flying_player[move_count // 10], (0, 0))
                self.rect.top = 20
                move_count = 0

            else:
                player.surf.blit(flying_player[move_count // 10], (0, 0))
            self.rect.move_ip(0, -15)

        elif pressed_keys[K_DOWN]:
            if self.rect.bottom >= screen_rect.bottom - 75:
                player.surf.blit(flying_player[move_count // 10], (0, 0))
                self.rect.bottom = screen_rect.bottom - 75
                move_count = 0

            else:
                player.surf.blit(flying_player[move_count // 10], (0, 0))
                self.rect.move_ip(0, 15)

        else:
            player.surf.blit(flying_player[move_count // 10], (0, 0))

        pygame.draw.rect(screen, (255, 0, 0), (player.rect.left + 22, player.rect.top + 5, 50, 10))
        pygame.draw.rect(screen, (0, 128, 0), (player.rect.left + 22, player.rect.top + 5,
                                               50 - (5 * (10 - player.health)), 10))


class Info:
    def __init__(self):
        self.started = False
        self.bullets = []
        self.end = False

    def reset(self):
        global score
        global gameplay
        player.surf.blit(dead_player, (player.rect.left, player.rect.top))
        self.started = False
        player.alive = True
        player.health = 10
        for element in enemies:
            element.kill()
        self.end = False
        player.rect.top = 0
        score = 0
        gameplay = True

    def start_level(self):
        self.started = True


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemies, self).__init__()
        self.surf = pygame.image.load("dino-spaceship-flying-game-character.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_rect.right + 20, screen_rect.right + 100),
                random.randint(70, screen_rect.bottom - 90),
            )
        )
        self.speed = -5

    def update(self):
        self.rect.move_ip(self.speed, 0)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((22, 23))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8
        self.bullets = []

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


player = Player()

enemies = pygame.sprite.Group()

projectile = Projectile(round(player.rect.right - 12), round(player.rect.centery + 84), 3,
                        (218, 165, 32))

game_info = Info()

ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, (score // 2) + 1000)


def draw_screen():
    global bullet

    screen.blit(background1, screen_rect)

    creator_name2 = font1.render("Created by: CONTROL", True, (0, 0, 0))
    screen.blit(creator_name2, (screen_rect.right - 117, screen_rect.bottom - 20))

    for element in enemies:
        screen.blit(element.surf, element.rect)

    for bullet in projectile.bullets:
        bullet.draw()

    pause_text = font.render("Press BACKSPACE to pause...", True, (0, 0, 0))
    screen.blit(pause_text, (30, screen_rect.bottom - 30))

    if player.alive:
        player.update()
        enemies.update()
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (30, screen_rect.bottom - 60))
    else:
        game_info.end = True

    if game_info.end:
        dead()


opener = True
gameplay = True
running = True
while running:
    draw_screen()

    clock.tick((score // 2) + 20)

    while not game_info.started:
        pygame.init()

        for event in pygame.event.get():
            screen.blit(background2, screen_rect)

            while opener:
                game_name1 = font2.render("NORTHERN LIGHTS", True, (0, 0, 0))
                game_name1_rect = game_name1.get_rect()
                screen.blit(game_name1, (screen_rect.centerx - game_name1_rect.centerx,
                                         screen_rect.centery - (game_name1_rect.centery + 100)))
                pygame.display.update()
                pygame.time.delay(5000)
                opener = False
                break

            game_name1 = font2.render("NORTHERN LIGHTS", True, (0, 0, 0))
            game_name1_rect = game_name1.get_rect()
            screen.blit(game_name1, (screen_rect.centerx - game_name1_rect.centerx,
                                     screen_rect.centery - (game_name1_rect.centery + 200)))

            quit_text = font.render("Press ESCAPE to quit...", True, (0, 0, 0))
            quit_text_rect = quit_text.get_rect()
            screen.blit(quit_text, (screen_rect.centerx - quit_text_rect.centerx,
                                    screen_rect.centery - quit_text_rect.centery))

            if gameplay:
                start_text = font.render("Press BACKSPACE to start...", True, (0, 0, 0))
                start_text_rect = start_text.get_rect()
                screen.blit(start_text, (screen_rect.centerx - start_text_rect.centerx,
                                         screen_rect.centery - start_text_rect.centery - 50))
            else:
                start_text = font.render("Press BACKSPACE to resume...", True, (0, 0, 0))
                start_text_rect = start_text.get_rect()
                screen.blit(start_text, (screen_rect.centerx - start_text_rect.centerx,
                                         screen_rect.centery - start_text_rect.centery - 50))

            creator_name = font1.render("Created by: CONTROL", True, (0, 0, 0))
            screen.blit(creator_name, (screen_rect.right - 117, screen_rect.bottom - 20))

            pygame.display.flip()

            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()

                elif event.key == K_BACKSPACE:
                    game_info.start_level()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_SPACE:
                if player.alive:
                    projectile.bullets.append(Projectile(round(player.rect.right - 12),
                                                         round(player.rect.centery + 36), 3,
                                                         (218, 165, 32)))
                    pygame.time.set_timer(event.key, (score // 2) + 40)
                    bullet_sound.play()
                    player.surf.blit(shooting_player[move_count // 4], (0, 0))

            elif event.key == K_HOME:
                if game_info.end:
                    game_info.reset()

            if event.key == K_BACKSPACE:
                if game_info.started:
                    game_info.started = False
                    gameplay = False
                else:
                    game_info.started = True

        elif event.type == ADD_ENEMY:
            new_enemy = Enemies()
            if player.alive:
                enemies.add(new_enemy)

        for bullet in projectile.bullets:
            if player.alive:
                if bullet.x < screen_rect.right:
                    bullet.x += bullet.vel
                else:
                    projectile.bullets.pop(projectile.bullets.index(bullet))
            else:
                projectile.bullets.clear()

        if player.alive:
            for item in projectile.bullets:
                for entity in enemies:
                    if item.y < entity.rect.bottom:
                        if item.y > entity.rect.top:
                            if item.x < entity.rect.right:
                                if item.x > entity.rect.left:
                                    hit_sound.play()
                                    projectile.bullets.pop(projectile.bullets.index(item))
                                    entity.kill()
                                    score += 1

        if player.alive:
            for entity in enemies:
                if entity.rect.right <= 0:
                    hit()
                    entity.kill()

    screen.blit(player.surf, (player.rect.left, player.rect.top + 20))

    pygame.display.flip()

pygame.quit()
