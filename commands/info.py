from operator import truediv
import discord
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(help='Mostra a latência.')
	async def ping(self, ctx):
		await ctx.send(f'pong! Isso levou `{round(self.client.latency * 1000)}ms`')

	@commands.command()
	async def info(self, ctx, new: discord.Role):
		ctx.send('testado')

def setup(client):
	client.add_cog(Info(client))
