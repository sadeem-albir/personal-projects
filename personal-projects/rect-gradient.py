import pygame as pg
import numpy as np

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

colors_original = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        for _ in range(100)]
colors = colors_original[:10]
w_offset = WIDTH * (1/8)
h_offset = HEIGHT * (1/8)
pixel_size = 5
rows = int( (HEIGHT - 2*h_offset) // pixel_size )
cols = int( (WIDTH - 2*w_offset) // pixel_size )


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
    for i in range(rows):
        for j in range(cols):
            pg.draw.rect(screen,
                    colors[(i+j) % len(colors)],
                    pg.Rect((j*pixel_size + w_offset, i*pixel_size + h_offset), (pixel_size, pixel_size))
            )

    # flip() the display to put your work on screen
    pg.display.flip()

    ## UPDATE YOUR GAME HERE
    kp = pg.key.get_pressed()
    if kp[pg.K_UP] and len(colors) < len(colors_original):
        colors = colors_original[:len(colors)+1]
        pg.time.delay(10)
    elif kp[pg.K_DOWN] and len(colors) > 1:
        colors = colors[:len(colors)-1]
        pg.time.delay(10)

    clock.tick(60)  # limits FPS to 60

pg.quit()

