import sqlite3

import discord
from discord.ext import commands

db = sqlite3.connect('./data/bot.db')
cs = db.cursor()

class Server_management(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(help='Define o invite do server no Banco de dados.')
	@commands.has_guild_permissions(administrator=True)
	async def setinvite(self, ctx, invite):
		if 'https://discord.com/invite/' in invite:
			cs.execute(f'''
			UPDATE server 
			SET invite = "{invite}"
			''')
			db.commit()
			await ctx.send('O convite foi alterado com sucesso... provavelmente.')
		else:
			await ctx.send('O convite deve estar no formato `https://discord.com/invite/#######`')


	@commands.command(help='Define o canal de boas vindas do server no Banco de dados.')
	@commands.has_guild_permissions(administrator=True)
	async def setwelchan(self, ctx, chanid: discord.TextChannel):
		cs.execute(f'''
		UPDATE server
		SET wel_chan = {chanid.id}
		''')
		db.commit()
		await ctx.send('Canal de boas vindas atualizado com sucesso... provavelmente.')


	@commands.command(help='Define o canal de saída do server no Banco de dados.')
	@commands.has_guild_permissions(administrator=True)
	async def setexichan(self, ctx, chanid: discord.TextChannel):
		cs.execute(f'''
		UPDATE server
		SET exi_chan = {chanid.id}
		''')
		db.commit()
		await ctx.send('Canal de saída atualizado com sucesso... provavelmente.')


	@commands.command(help='Define o canal de log do server no Banco de dados.')
	@commands.has_guild_permissions(administrator=True)
	async def setlog(self, ctx, chanid: discord.TextChannel):
		cs.execute(f'''
		UPDATE server
		SET log_chan = {chanid.id}
		''')
		db.commit()
		await ctx.send('Canal de logs atualizado com sucesso... provavelmente.')


	@commands.command(help='Define o canal de mensagens deletadas do server no Banco de dados.')
	@commands.has_guild_permissions(administrator=True)
	async def setdel(self, ctx, chanid: discord.TextChannel):
		cs.execute(f'''
		UPDATE server
		SET del_chan = {chanid.id}
		''')
		db.commit()
		await ctx.send('Canal de mensagens deletados atualizado com sucesso... provavelmente.')


def setup(client):
	client.add_cog(Server_management(client))
