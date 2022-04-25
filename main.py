import pygame
from colors import black
import parameters
from parameters import screen, clock, fps
from menu import Menu
from drawing import draw_text
from run import run

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Snake")

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
        draw_text(screen, str(parameters.score), 100, 300, 440)
    pygame.display.flip()

pygame.quit()

