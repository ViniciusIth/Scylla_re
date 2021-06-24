import discord
from discord.ext import commands
import bot_functions as bf
import random

class Member_events(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_join(self, member):
		print('==== Member Join Event ====')
		print(f'member = {member}')
		channel = self.client.get_channel(bf.getchan('wel_chan'))

		#Embed member join
		with open('./data/wel_img.txt', encoding='utf-8') as wel_img:
			img = wel_img.read()
			img = random.choice(list(map(str, img.split('\n'))))
		msg = discord.Embed(title='Bem vinda(o)!', description='Dê uma olhada no canal <#823942540779716610> e depois pegue seus cargos em <#821145600098566144>.')
		msg.set_image(url=img)
		msg.set_author(name=member, icon_url=member.avatar_url)
		msg.set_footer(text=f'ID do usuário')

		await channel.send(embed = msg)
		print('==== End Event ====\n')

	@commands.Cog.listener()
	async def on_member_exit(self, member):
		print('==== Member Remove Event ====')
		print(f'member = {member}')
		channel = self.client.get_channel(bf.getchan('exi_chan'))

		await channel.send(f'O membro {member} de id {member.id} acaba de sair do servidor.')
		print('==== End Event ====\n')

def setup(client):
	client.add_cog(Member_events(client))
