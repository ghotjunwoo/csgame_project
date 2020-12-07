# 장애물 정보를 정리하고 있다.

import random
import math
import pygame as pg

t1, t2, t3 = 90, 130, 110
p1, p2x, p2y = 0, 0, 0
red = (255, 0, 0)
green = (0, 255, 0 )

ARROW_DAMAGE = 100
ARROW_RADIUS = 20
SPEED_ARROW = 70
MANYARROW_DAMAGE = 8
MANYARROW_RADIUS = 20
SPEED_MANYARROW = 10

OMEGA = 2 * math.pi / 5

t4 = -1000
mushrooms = []

"""
장애물 양식
ult_name(ult_time, screen, system, player)
"""



# 레이저 장애물
def light(ult_time, screen, system, player):
    global t1, p1, t4
    light_image = system.load_img('light_4.png')
    # 둔화 상태 관리
    if ult_time < t4 + 50:
        player.cc_status = 1  # 둔화 상태 적용
    elif ult_time == t4 + 50:

        player.cc_status = 0
        t4 = -1000
    if ult_time > 50 and t1 <= 255:
        if ult_time == 51:
            # 변수 초기화
            p1 = player.xpos + random.randrange(-150, 50, 8)
            system.play_sound('swoosh.wav', 0.93)  # 효과음 재생
        ult = pg.draw.rect(screen, (255, 255, t1), (p1, 0, 50, 2 * system.width))  # 직사각형 표시
        screen.blit(light_image, (p1, system.width * 0.5 - 1000))  # 위치 해당하는 사진 표시
        t1 += 5
        # 충돌 여부 확인
        if t1 >= 200 and ult.colliderect(player.get_rect()):
            player.health -= 220  # 체력 감소
            t1 = 90
            ult_time = 0
            t4 = 0
        if t1 == 255:
            t1 = 90
            ult_time = 0
    return ult_time


# 십자가 장애물
def cross(ult_time, screen, system, player):
    global t2, p2x, p2y

    if ult_time > 80 and t2 <= 255:
        if ult_time == 81:
            # 변수 초기화
            rand_loc = random.randrange(-100, 100, 8)
            p2x = player.xpos + 110 + rand_loc
            p2y = player.ypos - 170 + rand_loc
            system.play_sound('cross.wav', 0.4)  # 효과음 재생

        ult1 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x - 100, p2y, 70, 350))
        ult2 = pg.draw.rect(screen, (0, 255, 255 - t2), (p2x - 250, p2y + 150, 350, 70))

        t2 += 5
        #충돌 여부 확인
        if t2 >= 200 and (ult1.colliderect(player.get_rect()) or ult2.colliderect(player.get_rect())):
            player.health -= 670
            t2 = 130
            ult_time = 0
        if t2 == 255:
            t2 = 130
            ult_time = 0
    return ult_time

#화살 클래스
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

class Manyarrow:
    def __init__(self, x, y, sx, sy, col=red):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.col = col
        self.radius = MANYARROW_RADIUS
        self.show = True

    def update_position(self):
        self.x += self.sx
        self.y += self.sy

    def display(self, screen):
        pg.draw.circle(screen, self.col, (int(self.x), int(self.y)), MANYARROW_RADIUS)

    def isout(self, system):
        return not ((0 <= self.x <= system.width) and (0 <= self.y <= system.height))

#화살 발사
def arrow_launcher(t, screen, system, player):
    def shoot_arrow_lu():
        return Arrow(0, 0, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10, (0, 255, 255))

    def shoot_arrow_ru():
        return Arrow(system.width, 0, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10, (0, 255, 255))

    def shoot_arrow_ld():
        return Arrow(0, system.height, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10, (0,255,255))

    def shoot_arrow_rd():
        return Arrow(system.width, system.height, -SPEED_ARROW * math.cos(random.randint(0, 70) / 10),
                     -SPEED_ARROW * math.sin(random.randint(0, 70) / 10) / 10, (0,255,255))

    arrows = [shoot_arrow_lu(), shoot_arrow_ld(), shoot_arrow_rd(), shoot_arrow_ru()]
    return arrows


def ezreal(t, screen, system, player):
    def shoot_manyarrow1():

        return Manyarrow(0, 0, -SPEED_MANYARROW * math.cos(0.01*t), -SPEED_MANYARROW * math.sin(t*0.01))

    def shoot_manyarrow2():

        return Manyarrow(0, 0, -SPEED_MANYARROW * math.cos(0.01*t+3.14/4), -SPEED_MANYARROW * math.sin(t*0.01)+3.14/4)

    def shoot_manyarrow3():

        return Manyarrow(0, 0, -SPEED_MANYARROW * math.cos(0.01*t+3.14/4*2), -SPEED_MANYARROW * math.sin(t*0.01)+3.14/4*2)

    def shoot_manyarrow4():

        return Manyarrow(0, 0, -SPEED_MANYARROW * math.cos(0.01*t+3.14/4*3), -SPEED_MANYARROW * math.sin(t*0.01)+3.14/4*3)

    manyarrows = [shoot_manyarrow1(), shoot_manyarrow2(), shoot_manyarrow3(), shoot_manyarrow4()]
    return manyarrows

#레이저
def laser(ult_time, screen, system, player):
    time = ult_time / 7
    theta = OMEGA * time
    x0 = (int(system.width / 2), int(system.height / 2))
    x1 = (int(system.width) * math.cos(theta) * 1.5, int(system.width) * math.sin(theta) * 1.5)
    (ul, ur, bl, br) = system.draw_line(x0, x1, 10, (150, 0, 0))
    left = ((ul[0] + bl[0]) / 2., (ul[1] + bl[1]) / 2.)
    right = ((ur[0] + br[0]) / 2., (ur[1] + br[1]) / 2.)
    hit = ((right[1] - left[1]) / (right[0] - left[0])) * (player.xpos - left[0]) + left[1]

    if hit - 10 <= player.ypos <= hit + 10 and (player.xpos - left[0]) * (x1[0] - left[0]) > 0:
        player.health -= 120

#버섯 클래스
class Mushroom:
    life = 500

    def __init__(self, x, y, g_time):
        self.x = x - 25
        self.y = y - 25
        self.g_time = g_time
        self.ult = None

    def display(self, time, screen, system):
        if self.g_time + self.life >= time:
            t = self.g_time + self.life - time
            teemo_image = system.load_img('Teemo.bomb.png')
            self.ult = pg.draw.rect(screen, (255, 255 - t * 0.5, 255 - t * 0.5), (self.x, self.y, 50, 50))
            screen.blit(teemo_image, (self.x + 5 , self.y + 4))
#             mushroom_image = system.load_img('mushroom.png')
#             self.ult = pg.draw.rect(screen, (255, 255 - t * 0.5, 255 - t * 0.5), (self.x, self.y, 50, 50))
#             screen.blit(mushroom_image, (self.x - 105, self.y - 55))

    def get_rect(self):
        return self.ult

#버섯 장애물
def mushroom(ult_time, time, screen, system, player):
    global mushrooms
    if ult_time == 61:
        mushrooms += [
            Mushroom(player.xpos + random.randrange(-250, 250, 8), player.ypos + random.randrange(-250, 250, 8), time)
            for
            _ in range(3)]
        ult_time = 0

    for index, mushroom in enumerate(mushrooms):
        mushroom.display(time, screen, system)
        if mushroom.get_rect().colliderect(player.get_rect()):
            player.health -= 100
            system.play_sound('mushroom.wav')
            mushrooms.pop(index)

    return ult_time
