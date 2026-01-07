import pygame as pg
import numpy as np

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# constants
pi = np.pi
UNIT = 80
DOT_SIZE = 4
THICKNESS = 1200

# non-constants
offset = 0
invisible_color = pg.Color("darkgreen")


running = True
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # per-frame variables
    ms_coord = pg.mouse.get_pos()

    X = np.linspace(ms_coord[0] - UNIT*pi, ms_coord[0] + UNIT*pi, THICKNESS)
    Y = UNIT * np.sin(X / UNIT + offset)

    X_left = np.linspace(0., X[0], THICKNESS)[:-1]
    Y_left = UNIT * np.sin(X_left / UNIT + offset)

    X_right = np.linspace(X[-1], WIDTH, THICKNESS)[1:]
    Y_right = UNIT * np.sin(X_right / UNIT + offset)


    # RENDER YOUR GAME HERE

    # draw axes
    pg.draw.line(screen, "yellow", (WIDTH//2, 0.), (WIDTH//2, HEIGHT))
    pg.draw.line(screen, "yellow", (0., HEIGHT//2), (WIDTH, HEIGHT//2))

    pg.draw.line(screen, "cyan", (0., HEIGHT//2 + UNIT), (WIDTH, HEIGHT//2 + UNIT))
    pg.draw.line(screen, "cyan", (0., HEIGHT//2 - UNIT), (WIDTH, HEIGHT//2 - UNIT))

#    pg.draw.line(screen, "cyan", [ms_coord[0], 0.], [ms_coord[0], HEIGHT])
#    pg.draw.line(screen, "cyan", [ms_coord[0] + UNIT*pi, 0.], [ms_coord[0] + UNIT*pi, HEIGHT])
#    pg.draw.line(screen, "cyan", [ms_coord[0] - UNIT*pi, 0.], [ms_coord[0] - UNIT*pi, HEIGHT])

    # draw unit steps
    unit_x_offset = CENTER[0] % UNIT
    unit_y_offset = CENTER[1] % UNIT
    for unit_x in range(unit_x_offset, WIDTH - unit_x_offset + 1, UNIT):
        pg.draw.circle(screen, "cyan", [unit_x, HEIGHT//2], DOT_SIZE)
    for unit_y in range(unit_y_offset, HEIGHT - unit_y_offset + 1, UNIT):
        pg.draw.circle(screen, "cyan", [WIDTH//2, unit_y], DOT_SIZE)

    # draw the function(s)
    for x, y in zip(X, Y):
        pg.draw.circle(screen, "green", CENTER + [x - CENTER[0], y], DOT_SIZE)

        ratio = min(1, abs(ms_coord[0] - x) / (pi * UNIT))
        clr = np.array([255 * (1 - ratio) ** 2, 0, 255])
        pg.draw.line(screen, clr, CENTER + [x - CENTER[0], y], CENTER + [x - CENTER[0], UNIT])
    for x, y in zip(X_right, Y_right):
        pg.draw.circle(screen, invisible_color, [x, y + CENTER[1]], DOT_SIZE)

        ratio = min(1, abs(ms_coord[0] - x) / (pi * UNIT))
        clr = np.array([255 * (1 - ratio) ** 2, 0, 255])
        pg.draw.line(screen, clr, CENTER + [x - CENTER[0], y], CENTER + [x - CENTER[0], UNIT])
    for x, y in zip(X_left, Y_left):
        pg.draw.circle(screen, invisible_color, [x, y + CENTER[1]], DOT_SIZE)

        ratio = min(1, abs(ms_coord[0] - x) / (pi * UNIT))
        clr = np.array([255 * (1 - ratio) ** 2, 0, 255])
        pg.draw.line(screen, clr, CENTER + [x - CENTER[0], y], CENTER + [x - CENTER[0], UNIT])

    # flip() the display to put your work on screen
    pg.display.flip()

    ## UPDATE
    kp = pg.key.get_pressed()
    if kp[pg.K_SPACE]:
        offset += 4 * (pi/180)

    clock.tick(60)  # limits FPS to 60

pg.quit()

