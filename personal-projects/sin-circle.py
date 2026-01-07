import pygame as pg
import numpy as np

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

def dist(p1, p2):
#    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** (1/2)
    return np.sqrt(np.dot(p2 - p1, p2 - p1))

def ang2vec(t):
    return np.array([np.cos(t), np.sin(-t)])

def std_angle(t):
    return t * -1 if t < 0. else t + 2*(np.pi - t)

## CONSTANTS
PI = np.pi

n_points = 800
points = np.linspace(0., 2*PI, n_points + 1)[:-1]
radius = 400

fixed_sin_r = radius / 8
sin_r = fixed_sin_r


running = True
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    ms_coord = np.array(pg.mouse.get_pos())
    sin_r_ratio = (dist(ms_coord, CENTER) - radius) / fixed_sin_r
    sin_r = fixed_sin_r * min(max(-1., sin_r_ratio), 1.)

    ms_angle = std_angle(np.atan2(*list(reversed(ms_coord - CENTER))))

    for i, pt in enumerate(points):
        pt_ctr = CENTER + (radius + sin_r * np.cos((pt - ms_angle)*12)) * ang2vec(pt)
        out_ctr = CENTER + (radius + fixed_sin_r) * ang2vec(pt)
        in_ctr = CENTER + (radius - fixed_sin_r) * ang2vec(pt)
        pg.draw.circle(screen, "cyan", pt_ctr, 4)
        pg.draw.circle(screen, "white", out_ctr, 4)
        pg.draw.circle(screen, "white", in_ctr, 4)
    pg.draw.line(screen, "orange",
            CENTER + (radius - fixed_sin_r) * ang2vec(ms_angle),
            CENTER + (radius + fixed_sin_r) * ang2vec(ms_angle),
            width=4)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(60)  # limits FPS to 60

pg.quit()

