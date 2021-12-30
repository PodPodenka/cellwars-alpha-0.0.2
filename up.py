from pyautogui import * 
from random import *
import sqlite3 as sq3 

global db
global sql
db = sq3.connect('database.db')
sql = db.cursor()
try:
	f = open('login.txt', 'r')
	login = f.read()
	f.close()
except:
	pass

def conquer():
	isGZ = sql.execute(f"SELECT gosudarstvo_zahvacheno FROM users WHERE login = '{login}'").fetchone()[0]
	if isGZ == True:
		number = randint(1, 2)
		# rsquare = randint(5, 10)
		# rfighters = randint(10, 1000)
		if number == 1:
			sqrs = sql.execute(f"SELECT square FROM users WHERE login = '{login}'").fetchone()[0]
			sqrf = sql.execute(f"SELECT fighters FROM users WHERE login = '{login}'").fetchone()[0]
			rsquare = randint(5, 10)
			rfighters = randint(10, 1000)
			rfighters2 = randint(10, 1000)

			sql.execute(f'UPDATE users SET square = {sqrs + rsquare} WHERE login = "{login}"')
			db.commit()

			sql.execute(f'UPDATE users SET fighters = {sqrf + rfighters} WHERE login = "{login}"')
			db.commit()

			sql.execute(f'UPDATE users SET fighters = {sqrf - rfighters2} WHERE login = "{login}"')
			db.commit()

			alert(f'Успешная попытка завоевать територрии!\nВы получили {rsquare} клеток площади, {rfighters} войск с завоёванных територрий и потеряли {rfighters2} войск в бою')
		else:
			alert('Неудачная попытка завоевать територрии!')
	else:
		alert('У вас нет захваченной столицы!')

def colonize():
	number = randint(1, 2)
	rsquare = randint(1, 5)
	rfighters = randint(5, 500)
	if number == 1:
		sqrs = sql.execute(f"SELECT square FROM users WHERE login = '{login}'").fetchone()[0]
		sqrf = sql.execute(f"SELECT fighters FROM users WHERE login = '{login}'").fetchone()[0]

		sql.execute(f'UPDATE users SET square = {sqrs + rsquare} WHERE login = "{login}"')
		db.commit()

		sql.execute(f'UPDATE users SET fighters = {sqrf + rfighters} WHERE login = "{login}"')
		db.commit()

		alert(f'Успешная попытка колонизировать територрии!\nВы получили {rsquare} клеток площади и {rfighters} войск с колонизированых територрий')
	else:
		alert('Неудачная попытка колонизировать територрии!')