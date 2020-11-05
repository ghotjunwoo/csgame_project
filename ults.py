#궁극기 정보를 정리하 있다.
import pygame as pg
import random
t1, t2 = 0, 0
p1, p2x, p2y = 0, 0, 0

def lux(ult_time, screen, system, player):
    global t1, p1
    # print("t1:" + str(t1))
    if ult_time > 300 and t1 <= 255:
        if ult_time == 301: p1 = player.xpos + random.randrange(-150, 50, 8)
        ult = pg.draw.rect(screen, (255, 255, t1), (p1, 0, 70, 2 * system.width))
        t1 += 5
        if t1 >= 200 and ult.colliderect(player.get_rect()):
            player.health -= 220
            t1 = 0
            ult_time = 0
        if t1 == 255:
            t1 = 0
            ult_time = 0
    return ult_time

def pyke(ult_time, screen, system, player):
    global t2, p2x, p2y
    print("t2:" + str(t2))

    if ult_time > 300 and t2 <= 255:
        if ult_time == 301:
            p2x = player.xpos + 110
            p2y = player.ypos - 170

        ult1 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x -100, p2y, 70, 350))
        ult2 = pg.draw.rect( screen, (0, 255, 255 - t2), (p2x-250, p2y+150, 350, 70))
        t2 += 5
        if t2 >= 200 and (ult1.colliderect(player.get_rect()) or ult2.colliderect(player.get_rect())):
            player.health -= 670
            t2 = 0
            ult_time = 0
        if t2 == 255:
            t2 = 0
            ult_time = 0
    return ult_time