import pygame.gfxdraw
import sys
import math
import random
from ults import *

pg.init()

# 게임에 쓰이는 정보를 적어놨다.
white = (255, 255, 255)
black = (0, 0, 0)
pg.mouse.set_visible(False)
BULLET_RADIUS = 10      #총알 크기
BULLET_DAMAGE = 100     #총알 데미지
SPEED_BULLET = 70       #총알 속도
PLAYER_RADIUS = 20      #주인공 크기
BUILDING_HEALTH = 1600      #빌딩크기
SPEED_MULTIPLIER = 20
SPEED_DISCRIMINATOR = 4
OMEGA = 2 * math.pi / 5     # 레이져 각속도

red = (255, 0, 0)
green = (0, 255, 0)
bullets = []        #총알 리스트
bullet_timer = 50       #총알이 교체되는 시간
bullet_timer_default = 7
arrows = []     #초록색 공 리스트
arrow_timer = 50        #초록색 공이 교체되는 시간
arrow_timer_default = 7
manyarrows = []     #빨간색 공 리스트
manyarrow_timer = 50        #빨간색 공이 교체되는 시간
manyarrow_timer_default = 2

# 화면 설정
screen = pg.display.set_mode((0, 0), pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN)


# 기본 변수
class system:
    # 게임창을 노트북 크기에 맞춤
    display = pg.display.Info()
    width = display.current_w
    height = display.current_h
    fps = 120

    def __init__(self):
        pass

    # 이미지 이름 설정
    def load_img(self, name):
        name = 'figures/' + name
        return pg.image.load(name)

    # 음악 이름 설정
    def play_music(self, name, volume=1, fadeout=0):
        name = './audios/' + name
        pg.mixer.init()
        pg.mixer.music.load(name)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play()
        if fadeout != 0:
            pg.mixer.music.fadeout(fadeout)

    # 음악 세기 설정
    def play_sound(self, name, volume=1) -> None:
        name = './audios/' + name
        sound = pg.mixer.Sound(name)
        sound.set_volume(volume)
        pg.mixer.Sound.play(sound)

    # 바탕화면 설정
    def load_background(self, screen, name):
        background = self.load_img(name)
        background = pg.transform.scale(background, (self.width, self.height))
        screen.blit(background, (0, 0))

    # 돌아가는 각도 계산(360도 기준)
    def rad_to_deg(self, angle):
        angle = -(angle * (360 / (2 * 3.141592)))
        while angle < 0 or angle >= 360:
            if angle < 0:
                angle += 360
            elif angle >= 360:
                angle -= 360
        return int(angle)

    # 레이져 구현(시작점, 끝점, 각도 설정)
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
#위치, 폰트, 크기, 색깔 설정
def text(arg, x, y, size, color, font="dinalternate.ttf") -> None:
    # 폰트 설정 없을 시 기본폰트로 설정
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

    # 타워가 받는 데미지 구현
    def get_damage(self):
        self.health -= BULLET_DAMAGE
        # 타워가 무너지는 소리 구현
        if self.health < BUILDING_HEALTH / 2 and self.state == 0:
            self.state = 1
            system.play_sound('collapse_1.wav', 1.1)
        if self.health < BUILDING_HEALTH / 4 and self.state == 1:
            self.state = 2
            system.play_sound('collapse_1.wav', 1.1)
        # 타워 체력이 0이 되면 클리어
        if self.health <= 0:
            return False

    # 화면에 타워 표시
    def display(self):
        building = system.load_img('building' + str(stage) + '_' + str(self.state) + '.png')
        screen.blit(building, (int(self.x), int(self.y)))

    # 스테이지가 넘어갈 경우 타워 체력 회복
    def heal(self):
        building.health = BUILDING_HEALTH
        self.state = 0


# 총알 클래스
class Bullet:
    # 위치, 크기, 속도 설정
    def __init__(self, x, y, sx, sy, col=red):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.col = col
        self.radius = BULLET_RADIUS
        self.show = True

    #위치 업데이트
    def update_position(self):
        self.x += self.sx
        self.y += self.sy

    def display(self):
        pg.draw.circle(screen, self.col, (int(self.x), int(self.y)), BULLET_RADIUS)

    def isout(self):
        return not ((0 <= self.x <= system.width) and (0 <= self.y <= system.height))


# 캐릭터 클래스
class Player:

    # 위치, 캐릭터 정보 설정
    def __init__(self, x, y, ceta, v, headx, heady, moving):
        self.xpos = float(x)
        self.ypos = float(y)
        self.theta = float(ceta)
        self.v = float(v)
        self.head_x = float(headx)
        self.head_y = float(heady)
        self.moving = moving
        self.health = 1000.0
        self.cc_status = 0

    def get_rect(self):
        return pg.Rect(int(self.xpos) - 10, int(self.ypos) - 10, 20, 20)

    # 화면에 좌표 출력
    def display(self):
        system.load_background(screen, 'new_background.png')
        character = system.load_img('character.png')
        character = pg.transform.rotate(character, system.rad_to_deg(self.theta) - 90)
        screen.blit(character, (int(self.xpos) - 100, int(self.ypos) - 100))

    # 마우스로 좌표 이동
    def movetohead(self):
        headx = self.xpos + self.v * math.cos(self.theta)
        heady = self.ypos + self.v * math.sin(self.theta)
        if (headx - self.head_x) * (self.xpos - self.head_x) <= 0:
            headx = self.head_x
        if (heady - self.head_y) * (self.ypos - self.head_y) <= 0:
            heady = self.head_y
        center_x = system.width / 2 - 40
        center_y = system.height / 2 - 15
        if abs(headx - center_x) <= 200 and abs(heady - center_y) <= 200:
            if headx - center_x + 200 < 20:
                headx = center_x - 201
            if headx - center_x - 200 > -20:
                headx = center_x + 201
            if heady - center_y + 200 < 20:
                heady = center_y - 201
            if heady - center_y - 200 > -20:
                heady = center_y + 201
        self.xpos = headx
        self.ypos = heady

    def shoot_bullet(self):
        return Bullet(self.xpos, self.ypos, SPEED_BULLET * math.cos(self.theta), SPEED_BULLET * math.sin(self.theta))

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
ult_time_light = random.randint(0, 300)
ult_time_cross = random.randint(0, 300)
ult_time_mushroom = 0

t = 0  # 궁 실행 시간
t2 = 0  # 게임 실행 시간
t4 = -200
level = 0  # 레벨

t3 = 0  # 로딩 화면 지속 시간

#게임 시작
while True:
    t2 += 1

    #스테이지 시작 시 화면
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
        text("제작사: 원숭이 Games", system.width / 2, system.height / 2 - 80, 50, white, "jejugothic.ttf")
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
        ult_time_light += 1
        ult_time_cross += 1
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
            player.head_x = float(mouse_pos[0])
            player.head_y = float(mouse_pos[1])
            cursor = system.load_img('cursor.png')
            screen.blit(cursor, (int(player.head_x - 20), int(player.head_y - 20)))
            if player.head_x != player.xpos or player.head_y != player.ypos:
                if player.head_y > player.ypos:
                    player.theta = math.acos((player.head_x - player.xpos) / math.sqrt(
                        (player.head_x - player.xpos) ** 2 + (player.head_y - player.ypos) ** 2))
                else:
                    player.theta = -math.acos((player.head_x - player.xpos) / math.sqrt(
                        (player.head_x - player.xpos) ** 2 + (player.head_y - player.ypos) ** 2))

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
            if (building.x + 50 <= bullet.x <= building.x + 350) and (building.y + 50 <= bullet.y <= building.y + 350):
                building.health -= BULLET_DAMAGE
                bullets.pop(index)
                life = building.get_damage()
                #각 스테이지 별 타워 설정
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
        if 1 <= stage <= 3:
            building.display()

        # 각 스테이지의 장애물 표시
        if stage == 1:
            ult_time_light = light(ult_time_light, screen, system, player)
            ult_time_cross = cross(ult_time_cross, screen, system, player)
        elif stage == 2:
            ult_time_mushroom += 1
            laser(t2, screen, system, player)
            ult_time_cross = cross(ult_time_cross, screen, system, player)
            ult_time_mushroom = mushroom(ult_time_mushroom, t2, screen, system, player)
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

            for index, manyarrow in enumerate(manyarrows):
                if (player.xpos <= manyarrow.x <= player.xpos + 200) and (player.ypos <= manyarrow.y <= player.ypos + 200):
                    player.health -= MANYARROW_DAMAGE

            arrow_timer -= 0.5
            if arrow_timer == 0:
                arrows += arrow_launcher(t2, screen, system, player)
                arrow_timer = arrow_timer_default
            for index, arrow in enumerate(arrows):
                arrow.update_position()
                arrow.display(screen)
                if arrow.isout(system):
                    arrows.pop(index)

            manyarrow_timer -= 0.5
            if manyarrow_timer == 0:
                manyarrows += ezreal(t2, screen, system, player)
                manyarrow_timer = manyarrow_timer_default
            for index, manyarrow in enumerate(manyarrows):
                manyarrow.update_position()
                manyarrow.display(screen)
                if manyarrow.isout(system):
                    manyarrows.pop(index)


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
    #게임 패배 화면
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
    #게임 클리어 화면
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
