import bot_functions as bf
import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect("./data/bot.db")
cs = db.cursor()

class Mod_utilities(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=('purge', 'del'), help='Deleta uma quantidade especifíca de mensagens.')
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount: int, member:discord.User=None):
		try:
		#Command
			if not member:
				await ctx.channel.purge(limit=amount)
				await ctx.send(f'{amount} mensagens deletadas', delete_after=3)
			else:
				todel = []
				ctx.message.delete()
				async for msg in ctx.channel.history():
					if len(todel) == amount:
						break
					if msg.author == member:
						todel.append(msg)
				await ctx.channel.delete_messages(todel)
				await ctx.send(f'{len(todel)} mensagens deletadas', delete_after=3)
		except Exception as e:
			ctx.send('Ops, algo deu errado o-o.', e)
		finally:
		#Embed Log
			embed_log=discord.Embed(title="Mensagens deletadas", description=f"{amount} mensagens foram deletadas do canal {ctx.channel}", color=discord.Colour.light_grey())
			embed_log.set_footer(text=f"By {ctx.author}")
			print('==== Mass Delete Event ====')
			await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
			print('==== End Event ====\n')

#TODO detect if member was kicked or if it's not possible
	@commands.command(help='Expulsa um membro do servidor')
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member:discord.User, *, reason=None):
	#Embed Membro
		embed_send=discord.Embed(title='Expulso', description='Você foi expulso do servidor Snek House.', color=discord.Colour.random())
		if reason == None:
			pass
		else:
			embed_send.add_field(name='motivo', value=reason, inline=False)
		embed_send.set_footer(text=f'By {ctx.author}')
	#Embed Log
		embed_log=discord.Embed(title='Expulso', description=f'{member} foi expulso do servidor Snek House.', color=discord.Colour.red())
		if reason == None:
			pass
		else:
			embed_log.add_field(name='motivo', value=reason, inline=False)
		embed_log.set_footer(text=f'By {ctx.author}')
	#Comando
		print('==== Member Kick Event ====')
		await ctx.send(f'{member} kickado do servidor.\nMotivo: {reason}', delete_after=5)
		await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
		await member.send(embed=embed_send)
		await ctx.guild.kick(member)
		print('==== End Event ====\n')

	@commands.command(help='Bane um membro do servidor e desbane imediatamente, útil para apagar mensagens.')
	@commands.has_guild_permissions(ban_members=True)
	async def softban(self, ctx, member:discord.User, *, reason = None):
	#Embed Membro
		embed_send=discord.Embed(title='Expulso', description='Você foi expulso do servidor Snek House.', color=discord.Colour.random())
		if reason == None:
			pass
		else:
			embed_send.add_field(name='motivo', value=reason, inline=False)
		embed_send.set_footer(text=f'By {ctx.author}')
	#Embed Log
		embed_log=discord.Embed(title='Softban', description=f'{member} tomou um softban.', color=discord.Colour.red())
		if reason == None:
			pass
		else:
			embed_log.add_field(name='motivo', value=reason, inline=False)
		embed_log.set_footer(text=f'By {ctx.author}')
	#Comando
		print('==== Softban Event ====')
		await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
		await member.send(embed=embed_send)
		await ctx.guild.unban(member)
		await ctx.guild.ban(member)
		print('==== End Event ====\n')


# TODO ban should say if it can ban or not
	@commands.command(help='Bane um membro do servidor.')
	@commands.has_guild_permissions(ban_members=True)
	async def ban(self, ctx, member:discord.User, *, reason = None):
	#Embed Membro
		embed_send=discord.Embed(title='Banido', description='Você foi banido do servidor Snek House.', color=discord.Colour.random())
		if reason == None:
			pass
		else:
			embed_send.add_field(name='motivo', value=reason, inline=False)
		embed_send.set_footer(text=f'By {ctx.author}')
	#Embed Log
		embed_log=discord.Embed(title='Ban', description=f'{member} foi banido.', color=discord.Colour.red())
		if reason == None:
			pass
		else:
			embed_log.add_field(name='motivo', value=reason, inline=False)
		embed_log.set_footer(text=f'By {ctx.author}')
	#Comando
		print('==== Member Ban Event ====')
		await member.send(embed=embed_send)
		await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
		await ctx.guild.ban(member)
		print('==== End Event ====\n')

	@commands.command(help='Desbane um membro do servidor.')
	@commands.has_guild_permissions(ban_members=True)
	async def unban(self, ctx, member:discord.User):
	#Embed Log
		embed_log=discord.Embed(title='Unban', description=f'{member} foi desbanido.', color=discord.Colour.red())
		embed_log.set_footer(text=f'By {ctx.author}')
	#Comando
		print('==== Member Unban Event ====')
		await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
		await ctx.guild.unban(member)
		print('==== End Event ====\n')

def setup(client):
	client.add_cog(Mod_utilities(client))
