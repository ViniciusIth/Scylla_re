import datetime as dt
import sqlite3

import bot_functions as bf
import discord
from discord.ext import commands

db = sqlite3.connect('./data/bot.db')
cs = db.cursor()

class Server_log(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.now = dt.datetime.now().strftime("%d/%m/%Y, %H:%M")

# channel log
	@commands.Cog.listener()
	async def on_guild_channel_create(self, chan):
		print('==== Channel Create Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))
		
		msg = discord.Embed(title='➕ Canal/Categoria', description=f'{chan.mention} foi criado')
		msg.add_field(inline=False, name='Tipo', value=f'{chan.type}')
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, chan):
		print('==== Channel Delete Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='🗑️ Canal deletado', description=f'O canal `{chan.name}` foi deletado')
		msg.set_footer(text=f'Snek House • {self.now}')
		await channel.send(embed=msg)
		print('==== End Event ====\n')


# role log
	@commands.Cog.listener()
	async def on_guild_role_create(self, role: discord.Role):
		print('==== Role Create Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Novo cargo criado', description=f'O cargo {role.mention} foi criado.', colour=discord.Colour.from_rgb(role.colour.r, role.colour.g, role.colour.b),)
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_role_update(self, old: discord.Role, new: discord.Role):
		print('==== Role update Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))
		perms = bf.compare_perms(old.permissions, new.permissions)
		

		#Embed log
		msg = discord.Embed(title=f'🔧 Cargo modificado', colour=discord.Colour.from_rgb(new.colour.r, new.colour.g, new.colour.b))
		if perms != False:
			msg.add_field(inline=False, name='Permissões', value=perms)
		if old.colour != new.colour:
			msg.add_field(inline=False, name='Cor', value=new.colour)
		if old.hoist != new.hoist:
			msg.add_field(inline=False, name='Separado', value=new.hoist)
		if old.mentionable != new.mentionable:
			msg.add_field(inline=False, name='Mencionável', value=new.mentionable)
		if old.name != new.name:
			msg.add_field(inline=False, name='Nome', value=new.name)
		if perms == False and old.colour == new.colour and old.hoist == new.hoist and old.mentionable == new.mentionable and old.name == new.name:
			return
		

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		print('==== Role Delete Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Cargo deletado', description=f'O cargo `{role.name}` foi deletado.', colour=discord.Colour.from_rgb(role.colour.r, role.colour.g, role.colour.b),)
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

# invite log
	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		print('==== Invite Create Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Convite criado', description=invite.url)
		msg.add_field(inline=False, name='Criador:', value=invite.inviter)
		if int(invite.max_uses) == 0:
			msg.add_field(inline=False, name='Usos max.:', value=invite.max_uses+1)
		else:
			msg.add_field(inline=False, name='Usos max.:', value=invite.max_uses)
		msg.add_field(inline=False, name='Duração:', value=f'{round(invite.max_age / 60)}min')
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_invite_delete(self, invite):
		print('==== Invite Delete Event ====')
		
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Convite deletado/expirado')
		msg.add_field(inline=False, name='URL:', value=invite.url)
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

def setup(client):
	client.add_cog(Server_log(client))
