import pygame as pg
import math
import numpy as np

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

v1 = np.array([400., 0.])
ROTATION = lambda t: np.matrix([
    [np.cos(t), -np.sin(t)],
    [np.sin(t), np.cos(t)]
])
angle = 0
angle_moving = True
print((ROTATION(angle) @ v1).squeeze())

running = True
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                angle_moving = not angle_moving

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    pg.draw.line(screen, "white", CENTER, CENTER + v1)

    rotated_v1 = np.array(ROTATION(angle) @ v1).squeeze()
    pg.draw.line(screen, "white", CENTER, CENTER + rotated_v1)

    ## dp_* = dot-product something
    dp_line = np.array([CENTER[0] + rotated_v1[0], CENTER[1]])
    pg.draw.line(screen, "orange", CENTER + rotated_v1, dp_line)

    ## dot-product side length
    dp = np.dot(v1, rotated_v1)
    dp_sl = math.sqrt(abs(dp))
    pg.draw.rect(screen, "green" if dp > 0. else "red", pg.Rect(CENTER, (abs(dp_sl), abs(dp_sl))), width=1)

    # flip() the display to put your work on screen
    pg.display.flip()

    ## UPDATE
    if angle_moving:
        angle += math.pi/180

    clock.tick(60)  # limits FPS to 60

pg.quit()

