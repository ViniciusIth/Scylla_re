import sqlite3
import discord
from discord.ext import commands
from bot_functions import compare_roles, getchan, compare_perms
import datetime as dt
import random

db = sqlite3.connect('./data/bot.db')
cs = db.cursor()

class Member_events(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.now = dt.datetime.now().strftime("%d/%m/%Y, %H:%M")
		self.imgfl = ['.jpg', '.png', '.gif']


# Member exit/entrace
	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		print('==== Member Join Event ====')
		user: discord.User = member
		print(f'Membro = {member}')

		channel = self.client.get_channel(getchan('wel_chan'))
		cs.execute(f'''
			INSERT INTO members (id)
			Values ({user.id})
		''')

		with open('./data/wel_img.txt', encoding='utf-8') as wel_img:
			img = wel_img.read()
			img = random.choice(list(map(str, img.split('\n'))))
		print(f'gif = {img}')

		msg = discord.Embed(title='Bem vinda(o)!', description='Dê uma olhada no canal <#823942540779716610> e depois pegue seus cargos em <#821145600098566144>.')
		msg.set_image(url=img)
		msg.set_author(name=member, icon_url=member.avatar_url)
		msg.set_footer(text=f'ID do usuário: {member.id}')

		await channel.send(embed=msg)


		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		print('==== Member Remove Event ====')
		now = dt.datetime.now().strftime("%d/%m/%Y, %H:%M")
		print(f'Membro = {member}')

		channel = self.client.get_channel(getchan('exi_chan'))
		cs.execute(f'''
			DELETE FROM members WHERE id = {member.id}
		''')
		
		msg = discord.Embed(description=f'O membro `{member.name}` saiu do servidor\nid = {member.id}')
		msg.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
		msg.set_footer(text=f'Snek House • {self.now}')
		await channel.send(embed=msg)
		

		print('==== End Event ====\n')


# Member messages
	@commands.Cog.listener()
	async def on_message_delete(self, deleted: discord.Message):
		if deleted.channel.id in [807399203050618910, 848921468233449522, 865392238723727371]:
			return
		else:
			print('==== Message Delete Event ====')
			channel = self.client.get_channel(getchan('del_chan'))

			msg = discord.Embed(
				title='Mensagem Deletada', description=f'🗑 **Mensagem de {deleted.author.mention} no canal {deleted.channel.mention}.**', color=0x010000)

			if deleted.content:
				msg.add_field(name='Mensagem', value=deleted.content, inline=False)

			if deleted.attachments and deleted.attachments[0].filename[-3:] not in self.imgfl:
				msg.add_field(name='Attachments', value = ''.join(deleted.attachments[0].url), inline=False)

			if deleted.attachments and deleted.attachments[0].filename[-3:] in self.imgfl:
				msg.set_image(url=deleted.attachments[0].url)
				msg.add_field(name='Attachments', value = ''.join(deleted.attachments[0].url), inline=False)

			msg.set_author(name=deleted.author,
						   icon_url=deleted.author.avatar_url)
			msg.set_footer(text=f'Snek House • {self.now}')

			await channel.send(embed=msg)
	
			print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_message_edit(self, old: discord.Message, new: discord.Message):
		if old.content == new.content or new.author.bot:
			return
		now = dt.datetime.now().strftime("%d/%m/%Y, %H:%M")
		print('==== Message Edit Event ====')
		channel = self.client.get_channel(getchan('del_chan'))

		msg = discord.Embed(title='Mensagem Editada', description=f':pencil2: **Mensagem de {new.author.mention} no canal {new.channel.mention}.  [Jump Message]({new.jump_url})**', color=0x010000)
		if '```' in old.content or '```' in new.content:
			msg.add_field(name='Antiga', value=f'{old.content}', inline=False)
			msg.add_field(name='Nova', value=f'{new.content}', inline=False)
		else:
			msg.add_field(name='Antiga', value=f'```{old.content}```', inline=False)
			msg.add_field(name='Nova', value=f'```{new.content}```', inline=False)
		if new.attachments and new.attachments[0].filename[-3:] not in self.imgfl:
			msg.add_field(name='Attachments', value = ''.join(new.attachments[0].url), inline=False)

		msg.set_author(name=new.author, icon_url=new.author.avatar_url)
		msg.set_footer(text=f'Snek House • {self.now}')

		await channel.send(embed=msg)

		print('==== End Event ====\n')

# Member updates
	@commands.Cog.listener()
	async def on_member_update(self, old: discord.Member, new: discord.Member):
		if old.nick == new.nick and old.roles == new.roles:
			return

		print('==== Member Update Event ====')
		
		channel: discord.TextChannel = self.client.get_channel(getchan('log_chan'))

		print(f'Membro: {new.name}#{new.discriminator}')
		msg = discord.Embed(name='Membro atualizado')
		msg.set_author(name=f'{new.name}#{new.discriminator}', icon_url=new.avatar_url)


		if old.nick != new.nick:
			print('Tipo: Apelido')
			msg.add_field(name='Nick alterado', value=f'alterado de `{old.display_name}` para `{new.display_name}`.')
	
		if old.roles != new.roles:
			print('Tipo: Cargos')
			new_roles = compare_roles(old.roles, new.roles)
			msg.add_field(name='Cargos alterados', value=new_roles)

		msg.set_footer(text=f'Snek House • {self.now}')



		await channel.send(embed=msg)
		print('==== End Event ====\n')


def setup(client):
	client.add_cog(Member_events(client))
