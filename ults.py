#궁극기 정보를 정리하고 있다.
import pygame as pg
import random
import math
t1, t2 = 90, 130
p1, p2x, p2y = 0, 0, 0
OMEGA = 2 * math.pi  / 5


"""
궁극기 양식
ult_name(ult_time, screen, system, player)
"""

def lux(ult_time, screen, system, player):
    global t1, p1
    # print("t1:" + str(t1))
    if ult_time > 50 and t1 <= 255:
        if ult_time == 51: p1 = player.xpos + random.randrange(-150, 50, 8)
        ult = pg.draw.rect(screen, (255, 255, t1), (p1, 0, 70, 2 * system.width))
        t1 += 5
        if t1 >= 200 and ult.colliderect(player.get_rect()):
            player.health -= 220
            t1 = 90
            ult_time = 0
        if t1 == 255:
            t1 = 90
            ult_time = 0
    return ult_time

def pyke(ult_time, screen, system, player):
    global t2, p2x, p2y

    if ult_time > 80 and t2 <= 255:
        if ult_time == 81:
            rand_loc = random.randrange(-100, 100, 8)
            p2x = player.xpos + 110 + rand_loc
            p2y = player.ypos - 170 + rand_loc

        ult1 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x -100, p2y, 70, 350))
        ult2 = pg.draw.rect( screen, (0, 255, 255 - t2), (p2x-250, p2y+150, 350, 70))
        t2 += 5
        if t2 >= 200 and (ult1.colliderect(player.get_rect()) or ult2.colliderect(player.get_rect())):
            player.health -= 670
            t2 = 130
            ult_time = 0
        if t2 == 255:
            t2 = 130
            ult_time = 0
    return ult_time

def laser(ult_time, screen, system, player):
    time = ult_time / 70
    theta = OMEGA * (time)
    X0 = (int(system.width / 2), int(system.height / 2))
    X1 = (int(system.width) * math.cos(theta) * 1.5, int(system.width) * math.sin(theta) * 1.5)
    (ul, ur, bl,br) = system.draw_line(X0, X1, 10, (150, 0, 0))
    l = ((ul[0] + bl[0]) / 2., (ul[1] + bl[1]) / 2.)
    r = ((ur[0] + br[0]) / 2., (ur[1] + br[1]) / 2.)
    hit = ((r[1] - l[1]) / (r[0] - l[0])) * (player.xpos - l[0]) + l[1]
    if hit - 10 <= player.ypos <= hit + 10 and (player.xpos - l[0]) * (X1[0] - l[0]) > 0:
        player.health -= 120