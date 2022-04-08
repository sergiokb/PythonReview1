import pygame
import random

screen_width = 600
screen_height = 600
fps = 20
sw = 20
aw = sw
speed = sw

black = (0, 0, 0)
white = (255, 255, 255)
green = (60, 200, 10)
red = (255, 10, 10)
yellow = (250, 200, 20)

pygame.init()
pygame.mixer.init()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def run():
    tail = []
    length = 1

    class Snake(pygame.sprite.Sprite):
        vx = speed
        vy = 0

        def __init__(self, w):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((w, w))
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2

        def update(self):
            keystate = pygame.key.get_pressed()
            if (keystate[pygame.K_LEFT] or keystate[pygame.K_a]) and self.vx == 0:
                self.vx = -speed
                self.vy = 0
            elif (keystate[pygame.K_RIGHT] or keystate[pygame.K_d]) and self.vx == 0:
                self.vx = speed
                self.vy = 0
            elif (keystate[pygame.K_UP] or keystate[pygame.K_w]) and self.vy == 0:
                self.vx = 0
                self.vy = -speed
            elif (keystate[pygame.K_DOWN] or keystate[pygame.K_s]) and self.vy == 0:
                self.vx = 0
                self.vy = speed

            self.rect.x += self.vx
            self.rect.y += self.vy

            tail.append([self.rect.x, self.rect.y])
            if length < len(tail):
                del tail[0]

            if self.rect.left >= screen_width:
                self.rect.left = 0
            if self.rect.top >= screen_height:
                self.rect.top = 0
            if self.rect.left < 0:
                self.rect.right = screen_width
            if self.rect.top < 0:
                self.rect.bottom = screen_height

    class Barrier(pygame.sprite.Sprite):
        def __init__(self, bw, bh):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((bw, bh))
            self.image.fill(green)
            self.rect = self.image.get_rect()
            self.rect.x = (random.randrange(0, screen_width - self.rect.width) // sw) * sw
            self.rect.y = (random.randrange(0, screen_height - self.rect.height) // sw) * sw

    class Apple(pygame.sprite.Sprite):
        def __init__(self, aw):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((aw, aw))
            self.image.fill(red)
            self.rect = self.image.get_rect()
            self.rect.x = round((random.randrange(self.rect.width, screen_width - self.rect.width)) / sw) * sw
            self.rect.y = round((random.randrange(self.rect.height, screen_height - self.rect.height)) / sw) * sw
            if pygame.sprite.spritecollide(self, barriers, False):
                self.change()

        def change(self):
            self.rect.x = round((random.randrange(self.rect.width, screen_width - self.rect.width)) / sw) * sw
            self.rect.y = round((random.randrange(self.rect.height, screen_height - self.rect.height)) / sw) * sw
            if pygame.sprite.spritecollide(self, barriers, False):
                self.change()

    def draw_tail(w, tail):
        for t in tail[:-1]:
            pygame.draw.rect(screen, white, [t[0], t[1], w, w])

    all_sprites = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    apples = pygame.sprite.Group()
    snake = Snake(sw)
    for i in range(1):
        b1 = Barrier(20, 220)
        b2 = Barrier(220, 20)
        all_sprites.add(b1)
        all_sprites.add(b2)
        barriers.add(b1)
        barriers.add(b2)
    for i in range(1):
        a = Apple(20)
        all_sprites.add(a)
        apples.add(a)

    all_sprites.add(snake)

    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        all_sprites.update()
        g = [snake.rect.x, snake.rect.y]
        hits = pygame.sprite.spritecollide(snake, barriers, False)
        for i in tail[:-1]:
            if i == g:
                running = False
        if hits:
            running = False
        eats = pygame.sprite.spritecollide(snake, apples, False)
        if eats:
            length += 1
            a.change()
        screen.fill(black)
        all_sprites.draw(screen)
        draw_text(screen, str(length - 1), 50, 40, 20)
        draw_tail(sw, tail)
        pygame.display.flip()
    global score
    score = length - 1


ar5 = pygame.font.SysFont('arial', 50)


class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(ar5.render(option, True, green))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, red, option_rect)
            surf.blit(option, option_rect)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

menu = Menu()
menu.append_option("Play", run)
menu.append_option("Quit", quit)

playing = True
first_time = True
while playing:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu.switch(-1)
            elif event.key == pygame.K_DOWN:
                menu.switch(1)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                menu.select()
                first_time = False
    screen.fill(black)
    menu.draw(screen, 100, 100, 75)
    if not first_time:
        draw_text(screen, "YOU DIED", 100, 300, 300)
        draw_text(screen, str(score), 100, 300, 440)
    pygame.display.flip()

pygame.quit()

