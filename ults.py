#궁극기 정보를 정리하고 있다.
import random
import math
import pygame as pg

t1, t2 = 90, 130
p1, p2x, p2y = 0, 0, 0

"""
궁극기 양식
ult_name(ult_time, screen, system, player)
"""

#럭스 궁
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

#파이크 궁
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