from settings import *
import pygame
import math
from pyautogui import *
import up
import sqlite3 as sq3
from drawing import Drawing

class Player:
    global db
    global sql
    db = sq3.connect('database.db')
    sql = db.cursor() 

    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self, clock):
        f = open('login.txt', 'r')
        login = f.read()
        f.close()

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        if keys[pygame.K_c]:
            alert('Точка выбранна!')
            posx = position()[0]
            posy = position()[1]
        if keys[pygame.K_z]:
            what = confirm('Что вы хотите сделать?', buttons=['Завоевать', 'Колонизировать'])
            if what == 'Завоевать':
                up.conquer()
            else:
                up.colonize()
        if keys[pygame.K_h]:
            alert('Помощь:\nПередвижение - W, A, S, D\nВыбрать точку - C,\nИзменить угол обзора - Стрелки вправо, влево\nРасширить територрию - Z\nВвести чит-код - P')
        if keys[pygame.K_p]:
            code = prompt('Введите чит-код:')
            if 'plusmoney' in code:
                cashh = sql.execute(f'SELECT cash FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {cashh * 2} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'plusfighters' in code:
                fight = sql.execute(f'SELECT fighters FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET fighters = {fight * 2} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'minusmoney' in code:
                cashh = sql.execute(f'SELECT cash FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {cashh // 2} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'minusfighters' in code:
                fight = sql.execute(f'SELECT fighters FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET fighters = {fight // 2} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'setsqtozero' in code:
                fight = sql.execute(f'SELECT square FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET square = {25} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'setcustomsquare' in code:
                number = int(prompt('Введите значение: '))
                fight = sql.execute(f'SELECT square FROM users WHERE login = "{login}"').fetchone()[0]
                sql.execute(f'UPDATE users SET square = {number} WHERE login = "{login}"')
                db.commit()
                alert('Успешно!')
            elif 'showcurrentfps' in code:
                alert(f'{clock.get_fps()} FPS')
            else:
                alert(f'Чит-код "{code}" не существует')