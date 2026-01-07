import pygame as pg
import numpy as np
import sys

pg.init()

WIDTH, HEIGHT = pg.display.get_desktop_sizes()[0]
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

inner_screen = pg.Rect((WIDTH//8, HEIGHT//8), (WIDTH - WIDTH//4, HEIGHT - HEIGHT//4))

## CONSTANTS
FPS = 20

## helper functions
def std_angle(t):
    if t < 0.:
        t *= -1
    else:
        t = 2*np.pi - t
    return t

def ang2vec(t):
    return np.array([np.cos(t), np.sin(-t)])

## all program sub-objects and variables
line_start_pt, line_end_pt = (np.array([inner_screen.x, inner_screen.y + (3/4)*inner_screen.h]),
        np.array([inner_screen.x + inner_screen.w, inner_screen.y + (1/4)*inner_screen.h]))
left_offset, right_offset = 0., 0.
offset_l1 = 0.
offset_l1_moving = True
n_pt = 267
offset_l2 = 0.
offset_l2_moving = True
pt_space = np.linspace(0., 1., n_pt)
step = 2


running = True
while running:
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                offset_l1_moving = not offset_l1_moving
            elif event.key == pg.K_p:
                offset_l2_moving = not offset_l2_moving
            elif event.key == pg.K_w and n_pt < 700:
                n_pt += 1
            elif event.key == pg.K_s and n_pt > 3:
                n_pt -= 1
            elif event.key == pg.K_1 and step > 1:
                step -= 1
            elif event.key == pg.K_2:
                step += 1

    ### PER-FRAME VARIABLES
    line_angle = std_angle(np.atan2(*list(reversed(line_end_pt - line_start_pt))))

    ## amplitude of the first-layer sine curve
    ampl_l1 = inner_screen.h // 4

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    pg.draw.rect(screen, "white", inner_screen, width=1) # container screen
    pg.draw.line(screen, "blue", line_start_pt, line_end_pt) # root line (acts as the root
                                                             # of the subsequent sine curves)

    for i, t in zip(range(0, len(pt_space[:-1 - step:step]), step), pt_space[:-1 - step:step]):
    ## checkpoint: loop-center
    ## not working as expected
#    for i, t in enumerate(pt_space[1:-3]):
        cycles = 2
        ms_x, ms_y = np.array(pg.mouse.get_pos())

        ## center_points are the points in the root line
        ## formula: v1 + t * (v2 - v1), where 0 <= t <= 1 and v1 = line_start_pt, v2 = line_end_pt
        try:
            ctr_pts = np.array([
                line_start_pt + pt_space[i+j] * (line_end_pt - line_start_pt)
            for j in range(step + 1)])
        except IndexError:
            print("crashed at", step)

        ## "sine-ifies" the amplitude of the nth-layer (first-layer in this case)
        ## visually, it turns a comb-looking set of perpendicular lines to curvedly scaled lines
        ## 
        ## |||||
        ## -----
        ## |||||
        ## 
        ## becomes approximately
        ## 
        ## | | |
        ## -----
        ##  | | 
        ## 
        ## to see a better demonstration of this concept, change the value of this variable to '1' or '-1'
        ## and see its effect on the nth-layer sine curve
        ampl_sin_l1 = np.array([pt_space[i+j] * cycles * 2*np.pi for j in range(step + 1)])

        ## L1 outer_points are the points of the root (first-layer) sine curve (biggest one)
        outer_pts_l1 = np.array([
            (ctr_pts[j] +
                ampl_l1 * np.sin(offset_l1 + ampl_sin_l1[j]) * ang2vec(line_angle + np.pi/2))
        for j in range(step + 1)])

        ## draw the first-layer sine curve
        for j in range(step):
            pg.draw.line(screen, "cyan", outer_pts_l1[j], outer_pts_l1[j+1])

        ## calculate the angles of each two closest points in the first-layer sine curve
        angs_l1 = np.array([ std_angle(np.atan2(*list(reversed(outer_pts_l1[j] - outer_pts_l1[j-1]))))
                for j in range(len(outer_pts_l1) - 1, 0, -1)])
        ## offset the calculated angle by pi/2 to draw the second-layer sine curve, essentially
        ## perpendicularizing the branch-sine to treat the root-sine as its local x-axis
        angs_l1 += np.pi/2

        ## the amplitude of the second-layer sine curve
        ampl_l2 = abs(ms_y - inner_screen.centery) / 6

        ## mid-points of each two closest points in the first-layer sine curve
        ## close-up visual:
        ##                                             ^ layer2_amplitude * 1
        ##                                             | perpendicularized offset (angs_l2)
        ## (*p1 layer1_sine)-------------------(p_mid layer2_sine )-------------------(*p2 layer1_sine)
        ##                                             | perpendicularized offset (angs_l2)
        ##                                             v layer2_amplitude * -1
        ## side-note: since the y-value increases down in graphics, the above visual may not fully represent
        ## the computation formula exactly as it looks: it shows the ideal representation when the center
        ## is (0, 0) and y increases upward. Simple adjustments have to be made to compensate this
        ## (such as rendering (CENTER + vector) instead of (vector) and sin(-t) instead of sin(t) ).
        mid_pts_l1 = np.array([(outer_pts_l1[j] + outer_pts_l1[j+1]) / 2 for j in range(len(outer_pts_l1) - 1)])

        ampl_sin_l2 = np.array([pt_space[i + j]*300*ampl_l1*2*np.pi for j in range(len(outer_pts_l1) - 1)])

        outer_pts_l2 = np.array([mid_pts_l1[j] +
                ampl_l2 * (np.sin(ampl_sin_l2[j] + offset_l2)) * ang2vec(angs_l1[j])
                for j in range(len(outer_pts_l1) - 1)])

        ## checkpoint
        # in_sin_coords_l2 = ## checkpoint

        for j in range(len(outer_pts_l1)-2):
            pg.draw.line(screen, ["white", "green"][i % 2],
                    outer_pts_l2[j],
                    outer_pts_l2[j+1]
            )
            pg.draw.circle(screen, "orange", outer_pts_l2[j], 4)
            pg.draw.circle(screen, "orange", outer_pts_l2[j+1], 4)

        if offset_l2_moving:
            offset_l2 -= (1/24 + (int(offset_l1_moving) * 0.06 )) * np.pi/180


    # flip() the display to put your work on screen
    pg.display.flip()

    ## UPDATE
    screen_w, screen_h = screen.get_width(), screen.get_height()
    inner_screen = pg.Rect((screen_w//8, screen_h//8), (screen_w - screen_w//4, screen_h - screen_h//4))
#    p1, p2 = (np.array([inner_screen.x, inner_screen.y + (1/2)*inner_screen.h + left_offset]),
#        np.array([inner_screen.x + inner_screen.w, inner_screen.y + (1/2)*inner_screen.h + right_offset]))

    if pg.mouse.get_pressed()[0]:
        # left_offset = pg.mouse.get_pos()[1] - inner_screen.centery
        p1 = np.array(pg.mouse.get_pos())
    if pg.mouse.get_pressed()[2]:
        # right_offset = pg.mouse.get_pos()[1] - inner_screen.centery
        p2 = np.array(pg.mouse.get_pos())

    if offset_l1_moving:
        offset_l1 += np.pi/180

    kp = pg.key.get_pressed()
    if kp[pg.K_UP] and n_pt < 700:
        n_pt += 1
    if kp[pg.K_DOWN] and n_pt > 3:
        n_pt -= 1

    # print(n_pt)

    clock.tick(FPS)  # limits FPS to 60

pg.quit()

