#import gameplay as gp
import sqlite3 as sq3
import os
import pygame
from settings import *
from map import world_map
from drawing import Drawing
from player import Player
from db import Drawing1

db = sq3.connect('database.db')
sql = db.cursor()

def for_dev():
	command = input()
	if command == 'show users':
		for i in sql.execute('SELECT login, square FROM users'):
			print(i)

	elif command == 'delete user':
		global login
		login = input('Username: ')

		sql.execute(f"DELETE FROM users WHERE login = '{login}'")
		db.commit()
		print('Deleted!')
	elif command == 'add user':
		login = input('Username: ')
		password = input('Password: ')

		sql.execute(f"SELECT login FROM users WHERE login = '{login}'")
		if sql.fetchone() is None:
			sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (login, password, 25, 0, 0, 0, 0, 0, 0, 100, 100, 0))
			db.commit()
			print('Created!')
	
		else:
			print('Error 1: User \'' + login + '\' is already have')

			for value in sql.execute("SELECT * FROM users"):
				print('Error 1: User ' + login + ' is already have')
	elif command == 'show all db':
		data = sql.execute('SELECT * FROM users').fetchall()
		print(data)
		
	elif command == 'benchmark':
		objects = int(input('Enter a force count of the benchmrk: '))
		pygame.init()
		pygame.display.set_caption('Игра: Клеточные воины')
		sc = pygame.display.set_mode((WIDTH, HEIGHT))
		sc_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
		clock = pygame.time.Clock()
		player = Player()
		drawing = Drawing(sc, sc_map)
		drawing1 = Drawing1(sc, sc_map)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			player.movement()
			sc.fill(BLACK)

			drawing1.fps(clock)
			drawing.mini_map(player)

			for a in range(objects):
				pygame.draw.circle(sc, GREEN, (int(player.x), int(player.y)), 12)
				pygame.draw.line(sc, GREEN, player.pos, (player.x + WIDTH * math.cos(player.angle),
													 player.y + WIDTH * math.sin(player.angle)), 2)
			for x, y in world_map:
				pygame.draw.rect(sc, RED, (x, y, TILE, TILE), 2)

			pygame.display.flip()
			clock.tick()
	

	elif command == 'show crypted db':
		os.system('type database.db')
		print('')

	elif command == 'quit':
		exit()

	#elif command == 'test run':
		#gp.main()

	else:
		print("CommandError: Command '" + command + "' not found")

def run():
	for_dev()


while True:
	run()