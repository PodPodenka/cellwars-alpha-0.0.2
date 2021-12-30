import pygame
from settings import *
from player import Player
import math
from map import world_map
from drawing import Drawing
import sqlite3 as sq3
import random as r
from win10toast import ToastNotifier
from tkinter import *
from tkinter import messagebox
import pyautogui as pg
import os
from mainru import *

# база данных по юзерам и прогресса юзера

global db
global sql
db = sq3.connect('database.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS users (
	login TEXT,
	password TEXT, 
	square INT, 
	cash BIGINT, 
	zavody BIGINT, 
	ferms BIGINT, 
	status TEXT, 
	fighters INT,
	gosudarstvo_zahvacheno INT,
	live_mark_per INT,
	villagers INT,
	quests INT
)""")

db.commit()
'''
global login
login = input('Введите свой логин: ')
if login is None:
	print('Вы не зарегестрировались. Предлагаем вам зарегестрироваться')
	reg()
'''
# регестрация
def reg():
	new_login = pg.prompt('Логин: ')
	password = pg.password('Пароль: ', mask='*')

	sql.execute(f"SELECT login FROM users WHERE login = '{new_login}'")

	if new_login is None:
		pg.alert('Error 405-MNA (Логин не можеть быть пустым)')
		quit()
	if sql.fetchone() is None:
		sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_login, password, 25, 1000, 10, 5, 'Новичок', 100, False, 100, 500, 0))
		db.commit()
		login = new_login
		pg.alert('Поздравляем! Вы зарегестрировались успешно! Площадь вашего государства на данный момент составляет 25 клеток.')
	else:
		pg.alert('Error 405-MNA (Пользователь уже зарегестрирован)')

		for value in sql.execute("SELECT * FROM users"):
			pg.alert('Имя пользователя ' + value[0] + ' уже существует!')

# бонус за игру в "числа" в виде 5 клеток площади
def try_luck():
	if login == 'dev':
		sql.execute(f'UPDATE users SET gosudarstvo_zahvacheno = {True} WHERE login = "{login}"')
		db.commit()

	sql.execute(f"SELECT login FROM users WHERE login = '{login}'")
	if sql.fetchone() is None:
		pg.alert('Вы не зарегестрировались. Предлагаем вам зарегестрироваться')
		reg()
	else:
		number = r.randint(1, 10)
		player_number = int(pg.prompt('Введите число от 1 до 10: '))

		if player_number == number:
			sqr = sql.execute(f"SELECT square FROM users WHERE login = '{login}'").fetchone()[0]

			pg.alert('Вы выиграли и получили 5 клеток площади государства в подарок!\nЧисло бота: ' + str(number))
			sql.execute(f'UPDATE users SET square = {sqr + 5} WHERE login = "{login}"')
			db.commit()
		else:
			pg.alert('Вы проиграли!\nЧисло бота: ' + str(number))

def play():
	pygame.init()
	sc = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.mouse.set_visible(False)
	sc_map = pygame.Surface(MINIMAP_RES)
	pygame.display.set_caption('Игра: Клеточные воины')

	clock = pygame.time.Clock()
	player = Player()
	drawing = Drawing(sc, sc_map)

	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
		player.movement(clock)
		sc.fill(BLACK)

		pygame.draw.rect(sc, BLACK, (0, 0, WIDTH, HALF_HEIGHT))
		pygame.draw.rect(sc, BLACK, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

		# ray_casting(sc, player.pos, player.angle)

		pygame.draw.circle(sc, GREEN, (int(player.x), int(player.y)), 12)
		pygame.draw.line(sc, GREEN, player.pos, (player.x + WIDTH * math.cos(player.angle),
												 player.y + WIDTH * math.sin(player.angle)), 2)
		for x, y in world_map:
			pygame.draw.rect(sc, RED, (x, y, TILE, TILE), 2)
		drawing.fps(clock)
		drawing.mini_map(player)
		if SHOW_FPS == True:
			drawing.fps2(clock)

		pygame.display.flip()
		clock.tick(FPS)

def show_statistics():
	#login = pg.prompt('Введите ваш логин для отображения информации: ')

	cash = sql.execute('SELECT cash FROM users WHERE login == ?', (login,)).fetchone()
	square = sql.execute('SELECT square FROM users WHERE login == ?', (login,)).fetchone()
	zavody = sql.execute('SELECT zavody FROM users WHERE login == ?', (login,)).fetchone()
	ferms = sql.execute('SELECT ferms FROM users WHERE login == ?', (login,)).fetchone()
	fighters = sql.execute('SELECT fighters FROM users WHERE login == ?', (login,)).fetchone()
	zahvat = sql.execute('SELECT gosudarstvo_zahvacheno FROM users WHERE login == ?', (login,)).fetchone()
	villagers = sql.execute('SELECT villagers FROM users WHERE login == ?', (login,)).fetchone()

	percent = sql.execute('SELECT live_mark_per FROM users WHERE login == ?', (login,)).fetchone()
	pg.alert('Ваше финансовое состояние: ' + str(cash[0]) + ',\nВаша площадь государства: ' + str(square[0]) + ',\n Ваше колличество войск: ' + str(fighters[0]) + ',\n Ваше состояние столицы: ' + str(zahvat[0]) + ',\n Ваше колличество жителей: ' + str(villagers[0]) + ',\n Процент настроения слоя населения: ' + str(percent[0]) + '%.\n')
	'''
	if percent[0] < 50:
		notify('Клеточные войны', 'Жители недовольны! Уровень настроения жителей меньше 50%! ('+str(percent[0])+'%)', 4)
	elif percent[0] > 50:
		notify('Клеточные войны', 'Жителей вашего государства всё устраивает! Процент настроения жителей: ('+str(percent[0])+'%)', 4)
	'''
def sd():
	isExit = pg.confirm('Вы действительно хотите выйти из игры?', buttons=['Да', 'Нет'])
	if isExit == 'Да':
		exit()
	else:
		pass


# шаблон пуш-сообщения
def notify(title, text, dur):
	toast = ToastNotifier()
	toast.show_toast(title, text, duration=dur, icon_path="icon.ico")

def delete_account():
	isDelete = pg.confirm('Эта функция позволяет добровольно удалить аккунт\nи учётную запись, пренадлежащую вам\nВы действительно хотите это сделать?', buttons=['Да', 'Нет'])
	if isDelete == 'Да':
		try:
			sql.execute(f"DELETE FROM users WHERE login = '{login}'")
			db.commit()
		except:
			pg.alert('Error 500-ISE (Не удалось удалить аккаунт)')
	else:
		pass

def show_users():
	number = 0
	for i in sql.execute('SELECT login FROM users'):
		number += 1
		pg.alert(f'{number}: {i[0]}')

def browser():
	os.system('C:/Users/glebp/Desktop/Podenka-inc/browserru/dist/mainru.exe')

def rename_account():
	new_login = pg.prompt('Введите новое имя пользователя:')
	new_login_acc = pg.prompt('Подтвердите новое имя пользователя:')
	if new_login == new_login_acc:
		sql.execute(f'SELECT login FROM users WHERE login = "{new_login}"')
		if sql.fetchone() is None:
			sql.execute(f'UPDATE users SET login = "{new_login}" WHERE login = "{login}"')
			db.commit()

			f = open('login.txt', 'w')
			f.write(new_login)
			f.close()

			pg.alert('Успешно!')

			isPassChange = pg.confirm('Хотите ли вы изменить пароль от аккаунта?', buttons=['Да', 'Нет'])
			if isPassChange == 'Да':
				new_password = pg.password('Введите новый пароль:')
				new_password_acc = pg.prompt('Подтвердите новый пароль:')
				if new_password == new_password_acc:
					sql.execute(f'UPDATE users SET password = "{new_password}" WHERE login = "{new_login}"')
					db.commit()
				else:
					pg.alert('Вы не подтвердили свой пароль')
			else:
				pass
		else:
			pg.alert('Это имя уже занято')
	else:
		pg.alert('Вы не подтвердили имя пользователя')

def change_account():
	new_login = pg.prompt('Введите логин:')
	sql.execute(f'SELECT login FROM users WHERE login = "{new_login}"')
	if sql.fetchone() is None:
		pg.alert('Этого имени не существует')
	else:
		new_pass = pg.password('Введите пароль:')
		passw = sql.execute(f'SELECT password FROM users WHERE login = "{new_login}"').fetchone()[0]
		if new_pass == passw:
			f = open('login.txt', 'w')
			f.write(new_login)
			f.close()
		else:
			pg.alert('Введён неверный пароль')

def open_settings():
	os.startfile('C:/Users/glebp/Desktop/Podenka-inc/settings.py')
	pg.alert('В этапе alpha и beta версий вы можете изменять настройки через код и менять игру как хотите')

# создание окна

def mainwindow():
	window = Tk()
	window.geometry(f"540x560+100+200")
	window.title('Клеточные воины')
	window.wm_attributes('-alpha', 1.0)
	window.resizable(width=False, height=False)

	canvas = Canvas(window, height=500, width=500)
	canvas.pack()

	frame = Frame(window)
	frame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.7)

	frame2 = Frame(window)
	frame2.place(relx=0.75, rely=0.05, relwidth=0.7, relheight=0.7)

	acc = Label(frame, text=f'Выполнен вход как: {login}', bg='white', font=40)
	acc.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
	acc.pack()

	menu = Label(frame, text='Меню функций:', bg='white', font=40)
	menu.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
	menu.pack()

	btn2 = Button(frame, text='Играть', command=play)
	btn2.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn2.pack()

	btn3 = Button(frame, text='Испытать удачу', command=try_luck)
	btn3.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn3.pack()

	btn4 = Button(frame, text='Показать статистику', command=show_statistics)
	btn4.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn4.pack()

	btn6 = Button(frame, text='Удалить аккаунт', command=delete_account)
	btn6.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn6.pack()

	btn7 = Button(frame, text='Таблица пользлвателей', command=show_users)
	btn7.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn7.pack()

	btn9 = Button(frame, text='Настройки', command=open_settings)
	btn9.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn9.pack()

	btn1 = Button(frame, text='Переименовать аккаунт', command=rename_account)
	btn1.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn1.pack()

	btn10 = Button(frame, text='Создать новый аккаунт', command=reg)
	btn10.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn10.pack()

	btn11 = Button(frame, text='Сменить аккаунт', command=change_account)
	btn11.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn11.pack()

	btn5 = Button(frame, text='Выйти', command=sd)
	btn5.place(x=10, y=10, relx=0.15, rely=1, relwidth=1, relheight=0.7)
	btn5.pack()

	window.mainloop()

f = open('login.txt')
login = f.read()
f.close()
mainwindow()