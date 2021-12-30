
from settings import *
import sqlite3 as sq3 
from pyautogui import *

global db
global sql
db = sq3.connect('database.db')
sql = db.cursor()

try:
	f = open('login.txt', 'r')
	login = f.read()
	f.close()
except:
	alert('Error 500-ISE (Для полноценной игры сделайте слудующие действия: \n1. Нажмите ПКМ по ярлыку "Клеточный Воин"\n2. Выберите и нажмите на пункт "Расположение файла"\n3. Найдите файл "login.txt" и напишите там свое имя пользователя)')
	exit()

count = sql.execute(f'SELECT square FROM users WHERE login = "{login}"').fetchone()[0]
if count >= 25 and count < 30:
    text_map = [
        '............',
        '...11111....',
        '...11111....',
        '...11111....',
        '...11111....',
        '...11111....',
         '............'
    ]
elif count >= 30 and count < 35:
    text_map = [
        '............',
        '...111111...',
        '...111111...',
        '...111111...',
        '...111111...',
        '...111111...',
        '............'
    ]
elif count >= 35 and count < 40:
    text_map = [
        '............',
        '...1111111..',
        '...1111111..',
        '...1111111..',
        '...1111111..',
        '...1111111..',
        '............'
    ]
elif count >= 40 and count < 45:
    text_map = [
        '............',
        '..11111111..',
        '..11111111..',
        '..11111111..',
        '..11111111..',
        '..11111111..',
        '............'
    ]
elif count >= 45 and count < 50:
    text_map = [
        '............',
        '.111111111..',
        '.111111111..',
        '.111111111..',
        '.111111111..',
        '.111111111..',
        '............'
    ]
elif count >= 50:
	text_map = [
        '............',
        '.1111111111.',
        '.1111111111.',
        '.1111111111.',
        '.1111111111.',
        '.1111111111.',
        '............'
    ]

world_map = {}
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'
                