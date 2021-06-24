import sqlite3
from PIL import ImageColor

def rstr(text):
	remove = {60: None, 62: None, 35: None, 64: None, 38: None, 33: None}
	text = (text.translate(remove))
	return int(text)

def getchan(row):
	db = sqlite3.connect('./data/bot.db'); print('Banco de dados aberto.')
	cursor = db.execute(f'SELECT {row} FROM server')
	show = ''.join(cursor.fetchone())
	print('Canal acessado:', show)
	db.close(); print('Banco de dados fechado.')
	return int(show)

def hex_to_rgbit(col):
	rgb = []
	col = str(col)
	col = ImageColor.getcolor(col, 'RGB')
	for cor in col:
		rgb.append(cor)
	print(rgb[0], rgb[1], rgb[2])
	return int(rgb[0]), int(rgb[1]), int(rgb[2])

def hex_to_rgbint(hex):
	str(hex)
	rgb = list(ImageColor.getcolor(hex, 'RGB'))
	rgbint = ''.join(map(str, rgb))
	return int(rgbint)

hex_to_rgbint('#0090ff')
