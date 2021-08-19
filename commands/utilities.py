import asyncio
from datetime import datetime as dt

import sqlite3
import discord
from discord.ext import commands

db = sqlite3.connect('./data/bot.db')
cs = db.cursor()

class Utilities(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['who', 'memberinfo', 'minfo'], help='Dá informações específicas sobre o membro.')
	async def whois(self, ctx, user: discord.User = None):
		user = user or ctx.author

		member: discord.Member = ctx.guild.get_member(user.id)

		mention = []
		for role in member.roles:
			if role.id != 803630429512269824:
				mention.append(role.mention)
		tmention = ', '.join(mention)

		act = ''
		customStatus = ''
		for a in member.activities:
			if isinstance(a, discord.CustomActivity):
				customStatus = a
			if isinstance(a, discord.Game):
				act = f'Jogando: {a}'
			elif isinstance(a, discord.Streaming):
				act = f'Streamando: {a}'
			elif isinstance(a, discord.Spotify):
				act = f'Ouvindo: {a.title} - {", ".join(a.artists)}'
		if not act:
			act = ' ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ '
		if not customStatus:
			customStatus = ' ~ ~ Não há nenhum status personalizado ~ ~ '

		perms = []
		for p in member.guild_permissions:
			if p[1] == True:
				perms.append(f'✅ {p[0]}')
			else: 
				pass

			tperms = '\n'.join(perms)
			if tperms.find('administrator') != -1:
				tperms = '✅ administrator (Todas as permissões)'

		msg = discord.Embed(title=f'Informações do usuário')
		msg.set_thumbnail(url=user.avatar_url)
		msg.add_field(name='Username', value=f'```{user.name}#{user.discriminator}```')
		msg.add_field(name='ID', value=f'```{user.id}```')
		msg.add_field(name=f'Cargos [{len(mention)}]', value=tmention, inline=False)
		msg.add_field(name='Nickname', value=f'```{member.nick}```')
		msg.add_field(name='Status', value=f'```{member.status}```')
		msg.add_field(name='Atividade', value=f'```{act}```', inline=False)
		msg.add_field(name=f'Status Personalizado', value=f'```{customStatus}```', inline=False)
		msg.add_field(name=f'Permissões Globais', value=f'```{tperms}```', inline=False)
		msg.add_field(name='Registrado em', value=f'```{user.created_at.strftime("%d/%m/%Y, %H:%M")}```')
		msg.add_field(name='Entrou em', value=f'```{member.joined_at.strftime("%d/%m/%Y, %H:%M")}```')

		await ctx.send(embed=msg)

	@commands.command()
	async def emoji(self, ctx, emoji: discord.Emoji):
		await ctx.send(emoji.url)

	@commands.command(help='Envia o link de convite do servidor.')
	async def invite(self, ctx):
		invite = cs.execute('SELECT invite FROM server').fetchone()
		await ctx.send(''.join(invite))
		db.commit(); db.close()

def setup(client):
	client.add_cog(Utilities(client))
