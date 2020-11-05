#궁극기 정보를 정리하 있다.
import pygame as pg

def lux(ult_time, t, screen, system, player):
    if ult_time > 300 and t <= 255:
        ult = pg.draw.rect(screen, (255, 255, t), (0.5 * system.width, 0, 70, 2 * system.width))
        t += 5
        if t >= 200 and ult.colliderect(player.get_rect()):
            player.health -= 220
            t = 0
            ult_time = 0
        if t == 255:
            t = 0
            ult_time = 0
        ult1 = pg.draw.rect(screen, (0, 255, 255 - t), (0.5 * system.width, 0.5 * system.height, 70, 350))
        ult2 = pg.draw.rect( screen, (0, 255, 255 - t), (0.5 * system.width-150, 0.5 * system.height+150, 350, 70))
        t += 5
        if t >= 200 and ult1.colliderect(player.get_rect()) or ult1.colliderect(player.get_rect()):
            player.health -= 220
            t = 0
            ult_time = 0
        if t == 255:
            t = 0
            ult_time = 0
    return ult_time, t
    # 화면 갱신