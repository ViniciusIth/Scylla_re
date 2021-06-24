import bot_functions as bf
import discord
from discord.ext import commands

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
		except commands.errors as errr:
			ctx.send('Ops, algo deu errado o-o.', errr)
		finally:
		#Embed Log
			embed_log=discord.Embed(title="Mensagens deletadas", description=f"{amount} mensagens foram deletadas do canal {ctx.channel}", color=discord.Colour.light_grey())
			embed_log.set_footer(text=f"By {ctx.author}")
			await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)

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
		await member.send(embed=embed_send)
	#Embed Log
		embed_log=discord.Embed(title='Expulso', description=f'{member} foi expulso do servidor Snek House.', color=discord.Colour.red())
		if reason == None:
			pass
		else:
			embed_log.add_field(name='motivo', value=reason, inline=False)
		embed_log.set_footer(text=f'By {ctx.author}')
		await self.client.get_channel(bf.getchan('log_chan')).send(embed=embed_log)
	#Comando
		await ctx.send(f'{member} kickado do servidor.\n {reason}', delete_after=2)


def setup(client):
	client.add_cog(Mod_utilities(client))
