import numpy as np
import pygame as pg

def get_vlen(v):
    return np.hypot(*(v["vtx"] - v["ctr"]))

def align_vector(v, p):
        p_fmt = p - v["ctr"]
        p_fmt_len = np.sqrt(np.dot(p_fmt, p_fmt)) if p_fmt.any() else 0.001
        v["vtx"] = (p_fmt / p_fmt_len) * v["len"]

def draw_vector(v, surf, engulfed=True, visible=True, filled=False):
    xy_flipped = list( reversed(v["vtx"] ) )
    v_angle = np.atan2(*xy_flipped)
    r = v_angle + 170*(np.pi/180)
    l = v_angle - 170*(np.pi/180)
    a_len = 15

    if visible:
        pg.draw.line(surf, v["clr"], v["ctr"], v["ctr"] + v["vtx"])
        pg.draw.line(surf, v["clr"], v["ctr"] + v["vtx"],
                v["ctr"] + v["vtx"] + np.array([a_len*np.cos(r), a_len*np.sin(r)]))
        pg.draw.line(surf, v["clr"], v["ctr"] + v["vtx"],
                v["ctr"] + v["vtx"] + np.array([a_len*np.cos(l), a_len*np.sin(l)]))
    if engulfed:
        t1 = (3/4)*np.pi
        t2 = (7/4)*np.pi
        t3 = (1/4)*np.pi
        t4 = (5/4)*np.pi
        p1 = v["ctr"] + [v["len"] * np.cos(t1), -v["len"] * np.sin(t1)]
        p2 = v["ctr"] + [v["len"] * np.cos(t2), -v["len"] * np.sin(t2)]
        p3 = v["ctr"] + [v["len"] * np.cos(t3), -v["len"] * np.sin(t3)]
        p4 = v["ctr"] + [v["len"] * np.cos(t4), -v["len"] * np.sin(t4)]
        pg.draw.circle(surf, "white", v["ctr"], v["len"], width=int(not filled))
#        pg.draw.line(screen, "red", p1, p2)
#        pg.draw.line(screen, "red", p3, p4)
