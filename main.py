import os
import random
import subprocess

import discord
from discord.ext import commands, tasks

subprocess.call('cls', shell=True)
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '..', case_insensitive = True, intents = intents)

@client.event
async def on_ready():
	Bot_stats.start()
	print('Conexão alcançada com sucesso')

@tasks.loop(minutes=5)
async def Bot_stats():
	with open('./data/bot_stats.txt', encoding='utf8') as frases:
		text = frases.read()
		bot_stats = list(map(str, text.split('\n')))
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(random.choice(bot_stats)))

@client.command()
async def test(ctx):
	ctx.send('Nenhum teste configurado.')

for file in os.listdir('./commands'):
	if file.endswith('.py'):
		client.load_extension(f'commands.{file[:-3]}')

client.run(os.getenv('TOKEN'))