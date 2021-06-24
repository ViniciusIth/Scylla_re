import discord
from discord.ext import commands

import bot_functions as bf

class Server_log(commands.Cog):
	def __init__(self, client):
		self.client = client

# channel log
	@commands.Cog.listener()
	async def on_guild_channel_create(self, chan):
		print('==== Channel Create Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Canal criado', description=f'O canal {chan.mention} foi criado')
		msg.add_field(name='Tipo', value=f'{chan.type}', inline=True)
		msg.add_field(name='Categoria', value=f'{chan.category}', inline=True)

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, chan):
		print('==== Channel Delete Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Canal deletado', description=f'O canal `{chan.name}` foi deletado')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

# role log
	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		print('==== Role Create Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Novo cargo criado', color=discord.Color.dark_gold(),)
		msg.add_field(name=role.name, value=f'Cor: {role.colour} \nID: {role.id}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_role_update(self, old, new):
		print('==== Role update Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Cargo modificado', color=discord.Color(bf.hex_to_rgbint(new.color)))
		msg.add_field(name=f'Antigo = {old.name}', value=f'Cor: {old.colour} \nPermissões: {old.permissions} \nSeparado: {old.hoist}', inline=False)
		msg.add_field(name=f'Novo = {new.name}', value=f'Cor: {new.colour} \nPermissões: {new.permissions} \nSeparado: {new.hoist}', inline=False)
		msg.set_footer(text=f'posição = {new.position}')

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		print('==== Role Delete Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Cargo deletado', color=discord.Color.dark_gold(),)
		msg.add_field(name=role.name, value=role.color)

		await channel.send(embed=msg)
		print('==== End Event ====\n')

# invite log
	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		print('==== Invite Create Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Convite criado', description=invite.url)
		msg.add_field(name='Criador:', value=invite.inviter)
		msg.add_field(name='Usos max.:', value=invite.max_uses)
		msg.add_field(name='Duração:', value=f'{round(invite.max_age / 60)}min')

		if int(invite.max_uses) == 0:
			msg.add_field(name='Usos max.:', value=invite.max_uses+1)

		await channel.send(embed=msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_invite_delete(self, invite):
		print('==== Invite Delete Event ====')
		channel = self.client.get_channel(bf.getchan('log_chan'))

		#Embed log
		msg = discord.Embed(title='Convite deletado/expirado')
		msg.add_field(name='URL:', value=invite.url)

		await channel.send(embed=msg)
		print('==== End Event ====\n')

def setup(client):
	client.add_cog(Server_log(client))
