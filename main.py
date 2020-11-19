import pygame as pg
import sys
import math
import random
from ults import *
pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
pg.mouse.set_visible(False)
BULLET_RADIUS = 10
BULLET_DAMAGE = 30
ARROW_DAMAGE = 100
ARROW_RADIUS = 20
PLAYER_RADIUS = 20
BUILDING_HEALTH = 3000
SPEED_BULLET = 70
SPEED_ARROW = 70
SPEED_MULTIPLIER = 20
SPEED_DISCRIMINATOR = 4

red = (255, 0, 0)
green = (0, 255, 0)
bullets=[]
bullet_timer = 50
bullet_timer_default = 7
arrows=[]
arrow_timer = 50
arrow_timer_default = 7

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
    def load_img(self, name):
        name = 'figures/' + name
        return pg.image.load(name)
    def loadBackground(self, screen, name):
        background = self.load_img(name)
        background = pg.transform.scale(background, (self.width, self.height))
        screen.blit(background, (0, 0))

    def rad_to_deg(self, angle):
        angle = -(angle * (360 / (2 * 3.141592)))
        while angle < 0 or angle >= 360:
            if angle < 0:
                angle += 360
            elif angle >= 360:
                angle -= 360
        return int(angle)

#글자 표시 함수
def text(arg, x, y, size, color):
    font = pg.font.Font(None, size)
    text = font.render(arg, True, color)
    textRect = text.get_rect()
    textRect.centerx = int(x)
    textRect.centery = int(y)
    screen.blit(text, textRect)

class vec:
    def __init__(self,x,y):
        self.angle='tan-1(y/x)'
        self.x=x
        self.y=y


#건물 클래스
class Building:
    def __init__(self, x, y, health):
        self.x = x - 130
        self.y = y - 130
        self.health = health
        self.images = [system.load_img('building.png'), system.load_img('building_1.png'), system.load_img('building_2.png')]
        self.state = 0
    def get_damage(self):
        self.health -= BULLET_DAMAGE
        if self.health < BUILDING_HEALTH / 2:
            self.state = 1
        if self.health < BUILDING_HEALTH / 4:
            self.state = 2
        if self.health <= 0:
            return False
    def display(self):
        building = self.images[self.state]
        screen.blit(building, (self.x, self.y))

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
    def isout(self): return not((0<=self.x<=system.width) and (0<=self.y<=system.height))

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
    def display(self):
        pg.draw.circle(screen, self.col, (int(self.x), int(self.y)), ARROW_RADIUS)
    def isout(self): return not((0<=self.x<=system.width) and (0<=self.y<=system.height))

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
        system.loadBackground(screen, 'new_background.png')
        character = system.load_img('character.png')
        character = pg.transform.rotate(character, system.rad_to_deg(self.ceta) - 90)
        screen.blit(character, (int(self.xpos) - 100, int(self.ypos) - 100))


    def movetohead(self): # 마우스로 좌표 이동
        headx = self.xpos + self.v*math.cos(self.ceta)
        heady = self.ypos + self.v*math.sin(self.ceta)
        if (headx - self.headx) * (self.xpos - self.headx) <= 0:
            headx = self.headx
        if (heady - self.heady) * (self.ypos - self.heady) <= 0:
            heady = self.heady
        self.xpos = headx
        self.ypos = heady

    def shoot_bullet(self):
        # print("Shooting")
        return Bullet(self.xpos,self.ypos,SPEED_BULLET*math.cos(self.ceta),SPEED_BULLET*math.sin(self.ceta))

    def shoot_arrow(self):
        #print("Shooting")
        return Arrow(system.width / 2, system.height / 2,-SPEED_ARROW*math.cos(self.ceta),-SPEED_ARROW*math.sin(self.ceta))

#환경 변수!!!!!
system = system()

#제목
pg.display.set_caption("돌격! 타워")
# image = pg.image.load(r'figures/background.jpg')
player = Player(system.width / 1.5, system.height / 3, 0, 20, 200.0, 200.0, False)
building = Building(system.width / 2, system.height / 2, BUILDING_HEALTH)


# 게임 루프의 주기 결정할 객체 생성
clock = pg.time.Clock()
running = False
happy = False

# 게임 메인 루프
ult_time_lux = random.randint(0, 300)
ult_time_pyke = random.randint(0, 300)
t = 0 # 궁 실행 시간
t2 = 0 # 게임 실행 시간
t3 = 0
level = 0 # 레벨
ccstatus = 0
screen.fill(black)
text("Dolgyuk Tower", screen.get_rect().centerx, screen.get_rect().centery, 100, white)
text("Press any key to start", system.width / 2, system.height / 2 + 70, 60, white)
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


    # 주인공 타격 확인-화살
    for index, arrow in enumerate(arrows):
        if (player.xpos <= arrow.x <= player.xpos + 200) and (player.ypos <= arrow.y <= player.ypos + 200):
            #player.health -= ARROW_DAMAGE
            t3 = t2
            arrows.pop(index)
        if t3 + 350 > t2:
            ccstatus = 3

    #마우스 인식


    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        mouse_pos = pg.mouse.get_pos()
        if ccstatus == 0:
            player.moving = True
        elif ccstatus == 3:
            player.moving = False


    # 체력 확인
    if player.health < 1000:
        player.health += 0.3
        if player.health <= 0:
            print("Game over")
            running = False

    #캐릭터 이동
    if player.moving:
        player.display()
        player.headx = float(mouse_pos[0])
        player.heady = float(mouse_pos[1])
        movecursor = system.load_img('cursor.png')
        screen.blit(movecursor, (int(player.headx-20), int(player.heady-20)))
        if player.headx != player.xpos or player.heady != player.ypos:
            if player.heady > player.ypos:
                player.ceta = math.acos((player.headx - player.xpos) / math.sqrt((player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))
            else:
                player.ceta = -math.acos((player.headx - player.xpos) / math.sqrt((player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))

    #총알 발사
    bullet_timer -= 1
    if bullet_timer == 0:
        bullets.append(player.shoot_bullet())
        bullet_timer = bullet_timer_default

    #총알 이동 및 나갈시 제거
    for index,bullet in enumerate(bullets):
        bullet.update_position()
        bullet.display()
        if bullet.isout(): bullets.pop(index)

    # 화살 발사
    arrow_timer -= 1
    if arrow_timer == 0:
        arrows.append(player.shoot_arrow())
        arrow_timer = arrow_timer_default

    # 화살 이동 및 나갈시 제거
    for index, arrow in enumerate(arrows):
        arrow.update_position()
        arrow.display()
        if arrow.isout(): arrows.pop(index)

    # 장애물 표시 & 타격 확인-총알
    for index, bullet in enumerate(bullets):
        if (building.x <= bullet.x <= building.x + 200) and (building.y <= bullet.y <= building.y + 200):
            building.health -= BULLET_DAMAGE
            life = building.get_damage()
            if life is not None:
                happy = True
                running = False
            print(building.health)
            bullets.pop(index)
    building.display()

    # 궁 발사

    '''ult_time_lux = lux(ult_time_lux, screen, system, player)
    ult_time_pyke = pyke(ult_time_pyke, screen, system, player)
    ult_time_ash = ash(ult_time_pyke, screen, system, player)'''


    #럭스 궁 사진 - 임시
    # luxult =  ge.load(r'figures/lux.png')
    # pg.transform.scale(luxult, (70, int(system.height * 1.1)))
    # screen.blit(luxult, (0, 0))

    # 체력 표시
    # 플레이어 체력
    pg.draw.rect(screen, (220, 220, 220), (int(0.14 * system.width), int(0.87 * system.height), int(0.4 * system.width), int(0.05 * system.height)))
    pg.draw.rect(screen, (0, 0, 200), (int(0.14 * system.width), int(0.87 * system.height), int(0.4 * system.width * player.health / 1000), int(0.05 * system.height)))
    text("Health: {}".format(int(player.health)), system.width / 4.2, 0.83 * system.height, 60, black)
    # 타워 체력
    pg.draw.rect(screen, (233, 0, 0), (int(building.x) + 40, int(building.y), 260 * building.health / BUILDING_HEALTH, 10))

    # 화면 갱신
    player.movetohead()
    pg.display.flip()

if not happy:
    screen.fill(black)
    text("G      G", int(system.width / 2), int(system.height / 2), 100, white)
    text("Press [X] to exit", int(system.width / 2), int(system.height / 2) + 80, 50, white)

    pg.display.flip()
else:
    screen.fill(white)
    text("LEVEL CLEAR", int(system.width / 2), int(system.height / 2), 100, black)
    text("Press [X] to exit", int(system.width / 2), int(system.height / 2) + 70, 60, black)

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


