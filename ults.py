# 궁극기 정보를 정리하고 있다.

import random
import math
import pygame as pg

t1, t2, t3 = 90, 130, 110
p1, p2x, p2y = 0, 0, 0
red = (255, 0, 0)
green = (0, 255, 0)

ARROW_DAMAGE = 100
ARROW_RADIUS = 20
SPEED_ARROW = 70

OMEGA = 2 * math.pi  / 5

t4 = -1000
teemos = []

"""
궁극기 양식
ult_name(ult_time, screen, system, player)
"""



# 럭스 궁
def lux(ult_time, screen, system, player):
    global t1, p1, t4
    # print("t1:" + str(t1))
    print(ult_time, t4 + 50)
    if ult_time < t4 + 50:
        player.cc_status = 1
    elif ult_time == t4 + 50:
        player.cc_status = 0
        t4 = -1000
    if ult_time > 50 and t1 <= 255:
        if ult_time == 51:
            p1 = player.xpos + random.randrange(-150, 50, 8)
        ult = pg.draw.rect(screen, (255, 255, t1), (p1, 0, 70, 2 * system.width))
        t1 += 5
        if t1 >= 200 and ult.colliderect(player.get_rect()):
            player.health -= 220
            t1 = 90
            ult_time = 0
            t4 = 0
        if t1 == 255:
            t1 = 90
            ult_time = 0
    return ult_time



# 파이크 궁
def pyke(ult_time, screen, system, player):
    global t2, p2x, p2y

    if ult_time > 80 and t2 <= 255:
        if ult_time == 81:
            rand_loc = random.randrange(-100, 100, 8)
            p2x = player.xpos + 110 + rand_loc
            p2y = player.ypos - 170 + rand_loc
            system.play_sound('pyke.wav', 0.4)


        ult1 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x - 100, p2y, 70, 350))
        ult2 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x - 250, p2y + 150, 350, 70))
        t2 += 5
        if t2 >= 200 and (ult1.colliderect(player.get_rect()) or ult2.colliderect(player.get_rect())):
            player.health -= 670
            t2 = 130
            ult_time = 0
        if t2 == 255:
            t2 = 130
            ult_time = 0
    return ult_time

class Arrow:
    def __init__(self, x, y, sx, sy, col=green):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.col = col
        self.radius = ARROW_RADIUS
        self.show = True

    def update_position(self):
        self.x += self.sx
        self.y += self.sy

    def display(self, screen):
        pg.draw.circle(screen, self.col, (int(self.x), int(self.y)), ARROW_RADIUS)

    def isout(self, system):
        return not ((0 <= self.x <= system.width) and (0 <= self.y <= system.height))


def ashe(t, screen, system, player):
    def shoot_arrowlu():

        return Arrow(0, 0, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10)

    def shoot_arrowru():
        return Arrow(system.width, 0, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10)

    def shoot_arrowld():
        return Arrow(0, system.height, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10)

    def shoot_arrowrd():
        return Arrow(system.width, system.height, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10)

    arrows = [shoot_arrowlu(), shoot_arrowld(), shoot_arrowrd(), shoot_arrowru()]
    return arrows

def laser(ult_time, screen, system, player):
    time = ult_time / 70
    theta = OMEGA * (time)
    X0 = (int(system.width / 2), int(system.height / 2))
    X1 = (int(system.width) * math.cos(theta) * 1.5, int(system.width) * math.sin(theta) * 1.5)
    (ul, ur, bl, br) = system.draw_line(X0, X1, 10, (150, 0, 0))
    l = ((ul[0] + bl[0]) / 2., (ul[1] + bl[1]) / 2.)
    r = ((ur[0] + br[0]) / 2., (ur[1] + br[1]) / 2.)
    hit = ((r[1] - l[1]) / (r[0] - l[0])) * (player.xpos - l[0]) + l[1]
    if hit - 10 <= player.ypos <= hit + 10 and (player.xpos - l[0]) * (X1[0] - l[0]) > 0:
        player.health -= 120

class Teemo:
    life = 500

    def __init__(self, x, y, g_time):
        self.x = x - 25
        self.y = y - 25
        self.g_time = g_time
        self.ult = None

    def display(self, time, screen):
        if self.g_time + self.life >= time:
            t = self.g_time + self.life - time
            self.ult = pg.draw.rect(screen, (255, 255 - t * 0.5, 255 - t * 0.5), (self.x, self.y, 50, 50))

    def get_rect(self):
        return self.ult


def teemo(ult_time, time, screen, system, player):
    global teemos
    if ult_time == 61:
        teemos += [
            Teemo(player.xpos + random.randrange(-250, 250, 8), player.ypos + random.randrange(-250, 250, 8), time) for
            _ in range(3)]
        ult_time = 0

    for index, teemo in enumerate(teemos):
        teemo.display(time, screen)
        if teemo.get_rect().colliderect(player.get_rect()):
            player.health -= 100
            teemos.pop(index)

    return ult_time
