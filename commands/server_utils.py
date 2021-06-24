import sqlite3

from discord.ext import commands

db = sqlite3.connect('./data/bot.db')
cs = db.cursor()

class Server_utils(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.has_any_role(820285412920000543, 820285688313675796)
	async def set_invite(self, ctx, invite):
		ctx.send('wip')


	@commands.command()
	@commands.has_any_role(820285412920000543, 820285688313675796)
	async def set_welchan(self, ctx, chanid):
		ctx.send('wip')


def setup(client):
	client.add_cog(Server_utils(client))
