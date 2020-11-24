import pygame.gfxdraw
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
PLAYER_RADIUS = 20
BUILDING_HEALTH = 1600
SPEED_BULLET = 70
SPEED_MULTIPLIER = 20
SPEED_DISCRIMINATOR = 4
OMEGA = 2 * math.pi / 5

red = (255, 0, 0)
green = (0, 255, 0)
bullets = []
bullet_timer = 50
bullet_timer_default = 7
arrows = []
arrow_timer = 50
arrow_timer_default = 7

# 화면 설정
screen = pg.display.set_mode((0, 0), pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN)

# 궁극기 목록
"""둔화: 1, 속박: 2, 기절: 3, 에어본: 4, 시아 축소: 5, 도발: 100"""
ults = [[("lux", 220, 0), ("browm", 0, 3)], [("teemo", 160, 1), ("katlin", 300, 0), ("missfortune", 550, 0)],
        [("ashe", 150, 3),
         ("galio", 0, 4), ("nami", 150, 4)],
        [("nocturne", 0, 5), ("pyke", 670, 0), ("gragas", 300, 4), ("maokai", 0, 2)], [("jinx", 300, 0),
                                                                                       ("ezreal", 400, 0),
                                                                                       ("orn", 80, 4),
                                                                                       ("kogmaw", 299, 1)],
        [("seokjaewook", 9999, 100)]]


# 기본 변수
class system:
    display = pg.display.Info()
    width = display.current_w
    height = display.current_h
    fps = 120

    def __init__(self):
        pass

    def load_img(self, name):
        name = 'figures/' + name
        return pg.image.load(name)

    def play_music(self, name, volume=1, fadeout=0):
        name = './audios/' + name
        pg.mixer.init()
        pg.mixer.music.load(name)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play()
        if fadeout != 0:
            pg.mixer.music.fadeout(fadeout)

    def play_sound(self, name, volume=1) -> None:
        name = './audios/' + name
        sound = pg.mixer.Sound(name)
        sound.set_volume(volume)
        pg.mixer.Sound.play(sound)

    def load_background(self, screen, name):
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

    def draw_line(self, start, end, thickness, color):
        center = ((start[0] + end[0]) / 2., (start[1] + end[1]) / 2.)
        length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        angle = math.atan2(start[1] - end[1], start[0] - end[0])
        ul = (center[0] + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
              center[1] + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        ur = (center[0] - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
              center[1] + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
        bl = (center[0] + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
              center[1] - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        br = (center[0] - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
              center[1] - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
        pg.gfxdraw.aapolygon(screen, (ul, ur, br, bl), color)
        pg.gfxdraw.filled_polygon(screen, (ul, ur, br, bl), color)
        return ul, ur, bl, br


# 글자 표시 함수
def text(arg, x, y, size, color, font="dinalternate.ttf") -> None:
    if font is not None:
        font = "./fonts/" + font
    font = pg.font.Font(font, size)
    text = font.render(arg, True, color)
    text_rect = text.get_rect()
    text_rect.centerx = int(x)
    text_rect.centery = int(y)
    screen.blit(text, text_rect)


# 건물 클래스
class Building:
    def __init__(self, x, y, health):
        self.x = x - 205
        self.y = y - 187
        self.health = health

        self.state = 0

    def get_damage(self):
        self.health -= BULLET_DAMAGE
        if self.health < BUILDING_HEALTH / 2 and self.state == 0:
            self.state = 1
            system.play_sound('collapse_1.wav', 1.1)
        if self.health < BUILDING_HEALTH / 4 and self.state == 1:
            self.state = 2
            system.play_sound('collapse_1.wav', 1.1)
        if self.health <= 0:
            return False

    def display(self):
        building = system.load_img('building' + str(stage) + '_' + str(self.state) + '.png')
        screen.blit(building, (int(self.x), int(self.y)))

    def heal(self):
        building.health = BUILDING_HEALTH
        self.state = 0


# 총알 클래스
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

    def isout(self):
        return not ((0 <= self.x <= system.width) and (0 <= self.y <= system.height))


# 캐릭터 클래스
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
        self.cc_status = 0

    def get_rect(self):
        return pg.Rect(int(self.xpos) - 10, int(self.ypos) - 10, 20, 20)

    def display(self):  # 화면에 좌표 출력
        system.load_background(screen, 'new_background.png')
        character = system.load_img('character.png')
        character = pg.transform.rotate(character, system.rad_to_deg(self.ceta) - 90)
        screen.blit(character, (int(self.xpos) - 100, int(self.ypos) - 100))

    def movetohead(self):  # 마우스로 좌표 이동
        headx = self.xpos + self.v * math.cos(self.ceta)
        heady = self.ypos + self.v * math.sin(self.ceta)
        if (headx - self.headx) * (self.xpos - self.headx) <= 0:
            headx = self.headx
        if (heady - self.heady) * (self.ypos - self.heady) <= 0:
            heady = self.heady
        widthmid = system.width / 2
        heightmid = system.height / 2
        if abs(headx - widthmid) <= 130 and abs(heady - heightmid) <= 130:
            if headx - widthmid + 130 < 20:
                headx = widthmid - 131
            if headx - widthmid - 130 > -20:
                headx = widthmid + 131
            if heady - heightmid + 130 < 20:
                heady = heightmid - 131
            if heady - heightmid - 130 > -20:
                heady = heightmid + 131
        self.xpos = headx
        self.ypos = heady

    def shoot_bullet(self):
        return Bullet(self.xpos, self.ypos, SPEED_BULLET * math.cos(self.ceta), SPEED_BULLET * math.sin(self.ceta))

    def heal(self):
        player.health = 1000.0
        player.cc_status = 0


def load_game():
    pass


# 환경 변수!!!!!
system = system()

# 제목
pg.display.set_caption("돌격! 타워")
# image = pg.image.load(r'figures/background.jpg')
player = Player(system.width / 1.5, system.height / 3, 0, 20, 200.0, 200.0, False)
building = Building(system.width / 2, system.height / 2, BUILDING_HEALTH)
system.play_music("background.wav", 0.6)

# 게임 루프의 주기 결정할 객체 생성
clock = pg.time.Clock()
running = False
happy = False
stage = -1  # 레벨

# 게임 메인 루프
ult_time_lux = random.randint(0, 300)
ult_time_pyke = random.randint(0, 300)
t = 0  # 궁 실행 시간
t2 = 0  # 게임 실행 시간
t4 = -200
level = 0  # 레벨

t3 = 0  # 로딩 화면 지속 시

while True:
    t2 += 1
    if stage == -1:
        screen.fill(black)
        text("돌격!　타워", screen.get_rect().centerx, screen.get_rect().centery, 120, white, "hanrasan.ttf")
        text("[SPACE] Start Game", system.width / 2, system.height / 2 + 200, 50, white)
        text('[H] Help', system.width / 2, system.height / 2 + 250, 50, white)
        text('[C] Credits', system.width / 2, system.height / 2 + 300, 50, white)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    stage = 0.5
                if event.key == pg.K_h:
                    stage = 11
                if event.key == pg.K_c:
                    stage = 12

    elif stage == 11:
        screen.fill(black)
        text("주인공은 마우스가 움직이는 방향으로 이동합니다.", system.width / 2, system.height / 2 - 80, 50, white, "jejugothic.ttf")
        text("주인공의 목표는 총으로 타워를 부시는 것 입니다.", system.width / 2, system.height / 2, 50, white, "jejugothic.ttf")
        text("장애물을 맞으면 주인공의 체력이 닳거나 멈추니 주의하세요.", system.width / 2, system.height / 2 + 80, 50, white, "jejugothic.ttf")
        text("그럼...행운을빕니다!!!!!", system.width / 2, system.height / 2 + 160, 50, white, "jejugothic.ttf")
        text("[R]Return", system.width / 2, system.height / 2 + 240, 50, white)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    stage = -1

    elif stage == 12:
        screen.fill(black)
        text("제작사: 원숭이 Gaming", system.width / 2, system.height / 2 - 80, 50, white, "jejugothic.ttf")
        text("제작자: 김대순, 정재원, 이준우", system.width / 2, system.height / 2, 50, white, "jejugothic.ttf")
        text("[R]Return", system.width / 2, system.height / 2 + 80, 50, white)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    stage = -1

    elif stage == 0.5:
        if not running:
            t3 = t2
            running = True
        screen.fill(black)
        text("옛날 옛날 용사와 공주가 살았습니다.", int(system.width / 2), int(system.height / 2) - 110, 50, white, 'jejugothic.ttf')
        text("하지만 갑자기 악당이 나타나 공주를 납치해버리고 맙니다.", int(system.width / 2), int(system.height / 2) - 30, 50, white,
             'jejugothic.ttf')
        text("용사는 자신이 사랑하는 공주를 살리기 위해", int(system.width / 2), int(system.height / 2) + 50, 50, white,
             'jejugothic.ttf')
        text("총 두자루만 가지고 악당이 사는 타워를 무너뜨리러 갑니다.", int(system.width / 2), int(system.height / 2) + 130, 50, white,
             'jejugothic.ttf')
        text("어..  근데 이 총 앞으로밖에 안쏴지잖아...?", int(system.width / 2), int(system.height / 2) + 210, 50, white,
             'jejugothic.ttf')
        if t3 + 300 < t2:
            stage = 1
            t2 = 0
            running = False
    if 1 <= stage <= 3:
        clock.tick(system.fps)  # 초당 프레임(FPS) 설정
        screen.fill(white)
        ult_time_lux += 1
        ult_time_pyke += 1
        # 화면 표시
        player.display()

        # 마우스 인식
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            mouse_pos = pg.mouse.get_pos()
            if player.cc_status == 0:
                player.moving = True
                player.v = 20
            elif player.cc_status == 1:
                player.moving = True
                player.v = 10
            elif player.cc_status == 3:
                player.moving = False

        # 체력 확인
        if player.health < 1000:
            player.health += 0.3
            if player.health <= 0:
                print("Game over")
                stage = 0
                continue

        # 캐릭터 이동
        if player.moving:
            player.display()
            player.headx = float(mouse_pos[0])
            player.heady = float(mouse_pos[1])
            movecursor = system.load_img('cursor.png')
            screen.blit(movecursor, (int(player.headx - 20), int(player.heady - 20)))
            if player.headx != player.xpos or player.heady != player.ypos:
                if player.heady > player.ypos:
                    player.ceta = math.acos((player.headx - player.xpos) / math.sqrt(
                        (player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))
                else:
                    player.ceta = -math.acos((player.headx - player.xpos) / math.sqrt(
                        (player.headx - player.xpos) ** 2 + (player.heady - player.ypos) ** 2))

        # 스테이지 설명
        if not running:
            t3 = t2
            running = True
        if t3 + 100 > t2:
            if stage == 1:
                text('하늘에서 떨어지는 수많은 십자가들과 레이저들... 주인공은 잘 피해 타워를 부술 수 있을것인가..?', int(system.width / 2.),
                     int(system.height * 0.98), 35, (20, 20, 20), 'jejugothic.ttf')
            elif stage == 2:
                text('아닛, 타워 안에 또 타워가?! 이번에도 무시무시한 시계바늘 레이져와 독버섯들을 피해 타워를 부셔보자!!!', int(system.width / 2.),
                     int(system.height * 0.98), 35, black, 'jejugothic.ttf')
            elif stage == 3:
                text('벌써 마지막이구만...장애물들이 훨씬 어려워졌지만 무엇도 우리를 막을 순 없지!', int(system.width / 2.), int(system.height * 0.98),
                     35, black, 'jejugothic.ttf')

        # 총알 발사
        bullet_timer -= 1
        if bullet_timer == 0:
            bullets.append(player.shoot_bullet())
            bullet_timer = bullet_timer_default

        # 총알 이동 및 나갈시 제거
        for index, bullet in enumerate(bullets):
            bullet.update_position()
            bullet.display()
            if bullet.isout():
                bullets.pop(index)

        # 장애물 표시 & 타격 확인
        for index, bullet in enumerate(bullets):
            if (building.x <= bullet.x <= building.x + 200) and (building.y <= bullet.y <= building.y + 200):
                building.health -= BULLET_DAMAGE
                life = building.get_damage()
                if life is not None:
                    if stage == 1:
                        BUILDING_HEALTH = 3000
                        building.heal()
                        player.heal()
                        stage = 2
                        system.play_sound("laser.wav")
                        running = False
                        continue
                    elif stage == 2:
                        BUILDING_HEALTH = 5000
                        building.heal()
                        player.heal()
                        stage = 3
                        running = False
                        continue
                    elif stage == 3:
                        stage = 4
                        running = False
                        continue
                # print(building.health)
                bullets.pop(index)
        if 1 <= stage <= 3:
            building.display()

        # 궁 발사

        if stage == 1:
            ult_time_lux = lux(ult_time_lux, screen, system, player)
            ult_time_pyke = pyke(ult_time_pyke, screen, system, player)
        elif stage == 2:
            laser(t2, screen, system, player)
            ult_time_lux = lux(ult_time_lux, screen, system, player)
            ult_time_pyke = pyke(ult_time_pyke, screen, system, player)
        elif stage == 3:
            # 주인공 타격 확인-화살
            for index, arrow in enumerate(arrows):
                if (player.xpos <= arrow.x <= player.xpos + 200) and (player.ypos <= arrow.y <= player.ypos + 200):
                    player.health -= ARROW_DAMAGE
                    t4 = t2
                    arrows.pop(index)
                if t4 + 50 > t2:
                    player.cc_status = 3
                else:
                    player.cc_status = 0

            arrow_timer -= 0.5
            if arrow_timer == 0:
                arrows += ashe(t2, screen, system, player)
                arrow_timer = arrow_timer_default
            for index, arrow in enumerate(arrows):
                arrow.update_position()
                arrow.display(screen)
                if arrow.isout(system):
                    arrows.pop(index)

        # 체력 표시
        # 플레이어 체력
        pg.draw.rect(screen, (220, 220, 220), (
            int(0.14 * system.width), int(0.87 * system.height), int(0.4 * system.width), int(0.05 * system.height)))
        pg.draw.rect(screen, (0, 0, 200), (
            int(0.14 * system.width), int(0.87 * system.height), int(0.4 * system.width * player.health / 1000),
            int(0.05 * system.height)))
        text("Health: {}".format(int(player.health)), system.width / 4.2, 0.83 * system.height, 60, black)
        # 타워 체력
        system.draw_line((int(building.x) + 50, int(building.y) + 20),
                         (int(building.x) + 50 + 280 * building.health / BUILDING_HEALTH, int(building.y) + 20), 10,
                         (220, 0, 0))
        # 화면 갱신
        player.movetohead()
    elif stage == 0:
        screen.fill(black)
        text("G      G", int(system.width / 2), int(system.height / 2), 100, white)
        text("Press [X] to exit", int(system.width / 2), int(system.height / 2) + 80, 50, white)
        text("or Press [R] to retry", int(system.width / 2), int(system.height / 2) + 160, 50, white)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_x:
                    pg.quit()
                    sys.exit(0)
                elif event.key == pg.K_r:
                    stage = 1
                    running = False
                    player.heal()
                    BUILDING_HEALTH = 1600
                    building.heal()
                    print("RETRY")
    elif stage == 4:
        screen.fill(white)
        text("LEVEL CLEAR", int(system.width / 2), int(system.height / 2), 100, black)
        text("Press [X] to exit", int(system.width / 2), int(system.height / 2) + 70, 60, black)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_x:
                    pg.quit()
                    sys.exit(0)

    # 화면 갱신
    pg.display.flip()
