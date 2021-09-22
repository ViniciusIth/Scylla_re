import os
import random
import subprocess
import aiohttp

from webserver import thread_run
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

subprocess.call('cls', shell=True)
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '..', case_insensitive = True, intents = intents)
load_dotenv()

@client.event
async def on_ready():
	# thread_run()
	# keep_alive.start()
	try:
		Bot_stats.start()
	except:
		pass
	print('Conexão alcançada com sucesso')

@tasks.loop(minutes=5)
async def Bot_stats():
	with open('./data/bot_stats.txt', encoding='utf8') as frases:
		text = frases.read()
		bot_stats = list(map(str, text.split('\n')))
	await client.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(bot_stats)))

@tasks.loop(minutes=30)
async def keep_alive():
	async with aiohttp.ClientSession() as session:
		async with session.get('https://Scyllare.karonpa.repl.co') as response:
			if response.status == 200:
				print('Status: Online')


for file in os.listdir('./commands'):
	if file.endswith('.py'):
		client.load_extension(f'commands.{file[:-3]}')

client.run(os.environ['TOKEN'])
