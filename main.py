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
BULLET_RADIUS = 5
PLAYER_RADIUS = 20
SPEED_BULLET=10
SPEED_MULTIPLIER = 20
SPEED_DISCRIMINATOR = 4
red = (255, 0, 0)
green = (0, 255, 0)
bullets=[]
bullet_timer = 100
bullet_timer_default = 100

#화면 설정
screen = pg.display.set_mode((0, 0),pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN)

#궁극기 목록
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
    def loadBackground(screen, name):
        name = 'figures/' + name
        background = pg.image.load(name)
        background = pg.transform.scale(background, (system.width, system.height))
        screen.blit(background, (0, 0))

    def rad_to_deg(angle):
        angle = -(angle * (360 / (2 * 3.141592)))
        while angle < 0 or angle >= 360:
            if angle < 0:
                angle += 360
            elif angle >= 360:
                angle -= 360
        return int(angle)

#글자 표시 함수
def text(arg, x, y):
    font = pg.font.Font(None, 100)
    text = font.render(arg, True, white)
    textRect = text.get_rect()
    textRect.centerx = int(x)
    textRect.centery = int(y)
    screen.blit(text, textRect)

class vec:
    def __init__(self,x,y):
        self.angle='tan-1(y/x)'
        self.x=x
        self.y=y

#총알 클래스
class Bullet:
    def __init__(self, x, y, sx, sy, col=red):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.col = col
        self.radius = BULLET_RADIUS
        self.show = True
    def update_position(self):
        self.x += self.sx
        self.y += self.sy
    def display(self):
        pg.draw.circle(screen, self.col, (int(self.x), int(self.y)), BULLET_RADIUS)
    def isout(self): return not((0<=self.x<=SCREEN_WIDTH) and (0<=self.y<=SCREEN_HEIGHT))


#배경 설정 함수


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
        return pg.Rect(int(self.xpos) - 10, int(self.ypos) - 10, 20, 20)

    def display(self): # 화면에 좌표 출력
        system.loadBackground(screen, 'background.png')
        character = pg.image.load('figures/character.png')
        character = pg.transform.rotate(character, system.rad_to_deg(self.ceta) - 90)
        screen.blit(character, (int(self.xpos) - 100, int(self.ypos) - 100))
        # pg.draw.circle(screen, white, (int(self.xpos), int(self.ypos)), 40)
        # pg.draw.circle(screen, black, (int(self.xpos+10*math.cos(self.ceta+0.5)), int(self.ypos+10*math.sin(self.ceta+0.5))), 5)
        # pg.draw.circle(screen, black, (int(self.xpos+10*math.cos(self.ceta-0.5)), int(self.ypos+10*math.sin(self.ceta-0.5))), 5)

    def movetohead(self): # 마우스로 좌표 이동
        headx = self.xpos + self.v*math.cos(self.ceta)
        heady = self.ypos + self.v*math.sin(self.ceta)
        if (headx - self.headx) * (self.xpos - self.headx) <= 0:
            headx = self.headx
        if (heady - self.heady) * (self.ypos - self.heady) <= 0:
            heady = self.heady
        self.xpos = headx
        self.ypos = heady

    def shoot(self):
        print("Shooting")
        return Bullet(self.xpos,self.ypos,SPEED_BULLET*math.cos(self.ceta),SPEED_BULLET*math.sin(self.ceta))

#제목
pg.display.set_caption("어결석")
image = pg.image.load(r'figures/background.jpg')
player = Player(system.width / 2, system.height / 2, 0, 20, 200.0, 200.0, False)



# 게임 루프의 주기 결정할 객체 생성
clock = pg.time.Clock()


# 게임 메인 루프
ult_time_lux = random.randint(0, 300)
ult_time_pyke = random.randint(0, 300)
t = 0 # 궁 실행 시간
t2=0 # 게임 실행 시간
level = 0 # 레벨
running = False
screen.fill(black)
text("Eu Gyeol Seok", screen.get_rect().centerx, screen.get_rect().centery)
pg.display.flip()

while not running:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            running = True

while running:
    t2 += 1
    ult_time_lux += 1
    ult_time_pyke += 1
    clock.tick(system.fps) # 초당 프레임(FPS) 설정
    #화면 표시
    screen.fill(white)
    player.display()

    #마우스 인식
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        mouse_pos = pg.mouse.get_pos()
        player.moving = True
        # if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
        #     player.moving = True
        # elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
        #     player.moving = True


    # 체력 확인
    if player.health < 1000:
        player.health += 0.9
        if player.health <= 0:
            print("Game over")
            running = False

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

    #총알 발사
    bullet_timer -= 1
    if bullet_timer == 0:
        bullets.append(player.shoot())
        bullet_timer = bullet_timer_default

    #총알 이동 및 나갈시 제거
    for index,bullet in enumerate(bullets):
        bullet.update_position()
        bullet.display()
        if bullet.isout(): bullets.pop(index)

    # 궁 발사

    ult_time_lux = lux(ult_time_lux, screen, system, player)
    ult_time_pyke = pyke(ult_time_pyke, screen, system, player)

    # 체력 표시

    #럭스 궁 사진 - 임시
    # luxult = pg.image.load(r'figures/lux.png')
    # pg.transform.scale(luxult, (70, int(system.height * 1.1)))
    # screen.blit(luxult, (0, 0))
    pg.draw.rect(screen, (0, 0, 200), (int(0.2 * system.width), int(0.87 * system.height), int(0.6 * system.width * player.health / 1000), int(0.08 * system.height)))
    text("Health: {}".format(int(player.health)), system.width / 2.0, 0.8 * system.height)

    # 화면 갱신
    player.movetohead()
    pg.display.flip()

screen.fill(black)
text("G      G", screen.get_rect().centerx, screen.get_rect().centery)
pg.display.flip()


#X나 종료 누르면 종료
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_x:
                pg.quit()
                sys.exit(0)


