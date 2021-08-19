import sqlite3
import numpy as np

def rstr(text):
	remove = {60: None, 62: None, 35: None, 64: None, 38: None, 33: None}
	text = (text.translate(remove))
	return int(text)

def getchan(row):
	db = sqlite3.connect('./data/bot.db'); print('Banco de dados aberto.')
	cursor = db.execute(f'SELECT {row} FROM server')
	show = ''.join(cursor.fetchone())
	print('Canal acessado:', show)
	return int(show)

def compare_perms(old, new):
	old_val = []
	new_val = []
	if old == new:
		return False
	else:
		for op in old:
			old_val.append(op)
		for np in new:
			if np not in old_val:
				if np[1] == True:
					new_val.append(f'✔️ {np[0]}')
				else:
					new_val.append(f'❌ {np[0]}')
		return '\n'.join(new_val)

def compare_roles(old, new):
	old_val = []
	new_val = []
	final_lstr = []

	for i in old:
		old_val.append(i)
	for i in new:
		new_val.append(i)

	removed_list = list(set(old_val) - set(new_val))
	added_list = list(set(new_val) - set(old_val))

	if added_list != []:
		for i in added_list:
			final_lstr.append(f'✔️  {i}')
	if removed_list != []:
		for i in removed_list:
			final_lstr.append(f'❌ {i}')

	final_lstr = '\n'.join(final_lstr)

	return final_lstr
