import pygame as pg
import numpy as np

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

## helper functions
def map_range(x, r1, r2): # maps point x from range r1 to range r2
    a, b = r1
    c, d = r2
    return ( (x-a)/(b-a) ) * (d-c) + c

PI = np.pi

angles = np.linspace(0., 2*PI, 255*3)[:-1]
radius = HEIGHT//3
th_offset = PI/12

running = True
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEWHEEL:
            th_offset += (event.y * 0.01)
            th_offset = min(max(0, th_offset), PI)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    ms_coord = pg.mouse.get_pos()
    ms_th = np.atan2(ms_coord[1] - CENTER[1], ms_coord[0] - CENTER[0])
    if ms_th < 0:
        ms_th *= -1
    else:
        ms_th += 2 * (PI - ms_th)

    for i, th in enumerate(angles):
        r = ( map_range(th, [4*PI/3, 2*PI], [0., 1.]) if 4*PI/3 <= th < 2*PI else
              map_range(th, [0., 2*PI/3], [1., 0.]) if 0. <= th <= 2*PI/3 else 0.
        )
        g = ( map_range(th, [0., 2*PI/3], [0., 1.]) if 0. <= th < 2*PI/3 else
              map_range(th, [2*PI/3, 4*PI/3], [1., 0.]) if 2*PI/3 <= th <= 4*PI/3 else 0.
        )
        b = ( map_range(th, [2*PI/3, 4*PI/3], [0., 1.]) if 2*PI/3 <= th < 4*PI/3 else
              map_range(th, [4*PI/3, 2*PI], [1., 0.]) if 4*PI/3 <= th <= 2*PI else 0.
        )

        color = np.array((r, g, b)) * 255.
        if ms_th - th_offset <= th <= ms_th + th_offset:
            # pg.draw.line(screen, color, CENTER, CENTER + radius * np.array([np.cos(th), np.sin(-th)]))
            pg.draw.circle(screen, color, CENTER + radius * np.array([np.cos(th), np.sin(-th)]), 10)

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(60)  # limits FPS to 60

pg.quit()

