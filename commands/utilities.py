import discord
from discord.ext import commands

class Utilities(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def holder(self, ctx):
		await ctx.send(f'WIP')

def setup(client):
	client.add_cog(Utilities(client))
