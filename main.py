import pygame as pg
import sys
import math
import random
from ults import *
pg.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
white = (255, 255, 255)
black = (0, 0, 0)
pg.mouse.set_visible(False)

#화면 설정
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN, pg.DOUBLEBUF)

#궁극기 목
"""둔화: 1, 속박: 2, 기절: 3, 에어본: 4, 시아 축소: 5, 도발: 100"""
ults = [[("lux", 220, 0), ("browm", 0, 3)], [("teemo", 160, 1), ("katlin", 300, 0), ("missfortune", 550, 0)], [("ashe", 150, 3),
("galio", 0, 4), ("nami", 150, 4)], [("nocturne", 0, 5), ("pyke", 670, 0), ("gragas", 300, 4), ("maokai", 0, 2)], [("jinx", 300, 0),
("ezreal", 400, 0), ("orn", 80, 4), ("kogmaw", 299, 1)], [("seokjaewook", 9999, 100)]]

#기본 변수
class system:
    display = pg.display.Info()
    width = display.current_w
    height = display.current_h
    fps = 120

#글자 표시 함수
def text(arg, x, y):
    font = pg.font.Font(None, 100)
    text = font.render(arg, True, white)
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


#배경 설정 함수
def loadBackground(screen, name):
    name = 'figures/'+name
    background = pg.image.load(name)
    background = pg.transform.scale(background, (system.width, system.height))
    screen.blit(background, (0, 0))

#캐릭터 클래스
class Player:
    def __init__(self, x, y, ceta, v, headx, heady, moving):
        self.xpos = float(x)
        self.ypos = float(y)
        self.ceta = float(ceta)
        self.v = float(v)
        self.headx = float(headx)
        self.heady = float(heady)
        self.moving = moving
        self.health = 1000.0

    def get_rect(self):
        return pg.Rect(self.xpos, self.ypos, 6, 6)

    def display(self): # 화면에 좌표 출력
        loadBackground(screen, 'background.png')
        pg.draw.circle(screen, white, (int(self.xpos), int(self.ypos)), 40)
        pg.draw.circle(screen, black, (int(self.xpos+10*math.cos(self.ceta+0.5)), int(self.ypos+10*math.sin(self.ceta+0.5))), 3)
        pg.draw.circle(screen, black, (int(self.xpos+10*math.cos(self.ceta-0.5)), int(self.ypos+10*math.sin(self.ceta-0.5))), 3)

    def movetohead(self): # 마우스로 좌표 이동
        headx = self.xpos + self.v*math.cos(self.ceta)
        heady = self.ypos + self.v*math.sin(self.ceta)
        if (headx - self.headx) * (self.xpos - self.headx) <= 0:
            headx = self.headx
        if (heady - self.heady) * (self.ypos - self.heady) <= 0:
            heady = self.heady
        self.xpos = headx
        self.ypos = heady

#제목
pg.display.set_caption("어결석")
image = pg.image.load(r'figures/background.jpg')
player = Player(200.0, 200.0, 0, 20, 200.0, 200.0, False)



# 게임 루프의 주기 결정할 객체 생성
clock = pg.time.Clock()



# 게임 메인 루프
ult_time = random.randint(0, 300)
t = 0 # 궁 실행 시간
t2=0 # 게임 실행 시간
level = 0 # 레벨
while True:
    t2 += 1
    ult_time += 1
    clock.tick(system.fps) # 초당 프레임(FPS) 설정
    #화면 표시
    screen.fill(white)
    player.display()

    #마우스 인식
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            player.moving = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
            player.moving = True


    # 체력 확인
    if player.health < 1000:
        player.health += 0.03
        if player.health <= 0:
            print("Game over")
            break

    #캐릭터 이동
    if player.moving:
        player.display()
        player.headx = float(mouse_pos[0])
        player.heady = float(mouse_pos[1])
        movecursor = pg.image.load(r'figures/cursor.png')
        screen.blit(movecursor, (int(player.headx-20), int(player.heady-20)))
        if player.headx != player.xpos or player.heady != player.ypos:
            if player.heady > player.ypos:
                player.ceta = math.acos((player.headx - player.xpos) / math.sqrt((player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))
            else:
                player.ceta = -math.acos((player.headx - player.xpos) / math.sqrt((player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))

    # 체력 표시
    pg.draw.rect(screen, (0, 0, 200), (0.2 * system.width, 0.87 * system.height, 0.6 * system.width * player.health / 1000, 0.08 * system.height))
    text("Health: {}".format(int(player.health)), system.width / 2.0, 0.8 * system.height)

    # 궁 발사
    ult_time, t = lux(ult_time, t, screen, system, player)
    # 화면 갱신
    player.movetohead()
    pg.display.flip()

