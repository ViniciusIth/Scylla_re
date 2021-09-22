from asyncio import TimeoutError as AsyncTimeOutError
import sqlite3
from discord import file
import qrcode
from io import BytesIO
from re import match, search
import string
from random import choice, randint

import discord
import asyncpraw
from qrcode.image.pil import PilImage
import wikipedia
from discord.ext import commands
from wikipedia.exceptions import DisambiguationError

db = sqlite3.connect("./data/bot.db")
cs = db.cursor()

class Utilities(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		aliases=["who", "memberinfo", "minfo"],
		help="Dá informações específicas sobre o membro.",
	)
	async def whois(self, ctx, user: discord.User = None):
		user = user or ctx.author

		member: discord.Member = ctx.guild.get_member(user.id)

		mention = []
		for role in member.roles:
			if role.id != 803630429512269824:
				mention.append(role.mention)
		tmention = ", ".join(mention)

		act = ""
		customStatus = ""
		for a in member.activities:
			if isinstance(a, discord.CustomActivity):
				customStatus = a
			if isinstance(a, discord.Game):
				act = f"Jogando: {a}"
			elif isinstance(a, discord.Streaming):
				act = f"Streamando: {a}"
			elif isinstance(a, discord.Spotify):
				act = f'Ouvindo: {a.title} - {", ".join(a.artists)}'
		if not act:
			act = " ~ ~ Aparentemente, o usuário não está fazendo nada ~ ~ "
		if not customStatus:
			customStatus = " ~ ~ Não há nenhum status personalizado ~ ~ "

		perms = []
		for p in member.guild_permissions:
			if p[1] == True:
				perms.append(f"✅ {p[0]}")
			else:
				pass

			tperms = "\n".join(perms)
			if tperms.find("administrator") != -1:
				tperms = "✅ administrator (Todas as permissões)"

		msg = discord.Embed(title=f"Informações do usuário")
		msg.set_thumbnail(url=user.avatar_url)
		msg.add_field(name="Username", value=f"```{user.name}#{user.discriminator}```")
		msg.add_field(name="ID", value=f"```{user.id}```")
		msg.add_field(name=f"Cargos [{len(mention)}]", value=tmention, inline=False)
		msg.add_field(name="Nickname", value=f"```{member.nick}```")
		msg.add_field(name="Status", value=f"```{member.status}```")
		msg.add_field(name="Atividade", value=f"```{act}```", inline=False)
		msg.add_field(
			name=f"Status Personalizado", value=f"```{customStatus}```", inline=False
		)
		msg.add_field(name=f"Permissões Globais", value=f"```{tperms}```", inline=False)
		msg.add_field(
			name="Registrado em",
			value=f'```{user.created_at.strftime("%d/%m/%Y, %H:%M")}```',
		)
		msg.add_field(
			name="Entrou em",
			value=f'```{member.joined_at.strftime("%d/%m/%Y, %H:%M")}```',
		)

		await ctx.send(embed=msg)

	@commands.command()
	async def emoji(self, ctx, emoji: discord.Emoji):
		await ctx.send(emoji.url)

	@commands.command(help="Envia o link de convite do servidor.")
	async def invite(self, ctx):
		invite = cs.execute("SELECT invite FROM server").fetchone()
		await ctx.send("".join(invite))

	# TODO Asynchrounous wiki function.
	@commands.command(help='Mostra um artigo sobre o assunto escolhido.')
	async def wiki(self, ctx, *, search):

		lang = "pt"
		if search[-3] == " ":
			if search[-2:] in wikipedia.languages():
				lang = search[-2:]
		wikipedia.set_lang(lang)

		searching = await ctx.send("Buscando...")

		try:
			page = wikipedia.page(search)
			summary = page.summary.partition("\n")[0]

			await searching.delete()
			msg = discord.Embed(
				title=page.title,
				description=summary + "\n\n" + f"[Ver o artigo]({page.url})",
			)
			msg.set_image(url=page.images[0])
			await ctx.send(embed=msg)

		except DisambiguationError as e:

			await searching.delete()
			msg = discord.Embed(
				title="Desambiguação",
				description="Sua pesquisa pode se referir aos seguintes resultados:\n\n"
				+ "\n".join(e.options)
				+ "\n\nSeja mais específico.",
			)
			await ctx.send(embed=msg)

		except wikipedia.exceptions.PageError:
			await searching.delete()
			await ctx.send(f"Não foi possivel encontrar a página `{search}`")

	@commands.command(help='Mostra uma postagem aleatória do subreddit escolhido entre os 50 melhores.')
	async def sub(self, ctx, *, subreddit):
		reddit = asyncpraw.Reddit(
			client_id="TI0_Tf0ZyJNY6AH7mq_9pg",
			client_secret="RPZ1FEQas9WFNkCQDBekGf84iYTQZQ",
			user_agent=(
				"Snekky 2.0.4 by u/inhister | https://github.com/Karonpa/Scylla_re"
			),
		)
		subreddit = await reddit.subreddit(subreddit.replace(" ", ""))

		searching = await ctx.send("Buscando...")

		try:
			await subreddit.load()

			sub_list = []

			if subreddit.over18:
				await ctx.send("Calma lá amigão, este subreddit não é FamIlY FrIenDlY")
				return

			async for submission in subreddit.hot(limit=50):
				if submission.url[-3:] in ["jpg", "png", "gif"]:
					sub_list.append(submission)

			submission = choice(sub_list)

			await submission.author.load()
			msg = discord.Embed(title=submission.title, url=f'https://www.reddit.com{submission.permalink}')
			msg.set_image(url=submission.url)
			msg.set_author(
				name=f"{submission.author} in r/{submission.subreddit}",
				icon_url=submission.author.icon_img,
			)
			msg.set_footer(text=f"🤌 {submission.score} | 💬 {submission.num_comments}")

			await searching.delete()
			await ctx.send(embed=msg)

		except:
			await searching.delete()
			await ctx.send("Não foi possivel encontrar esse subreddit")

	@commands.command(aliases=['r', 'dice'], help='Rola um dado')
	async def roll(self, ctx: commands.context.Context, roll):

		dice_pattern = r'(\d+|)d(\d+)(\+\+\d+|\-\-\d+|\d+|[\+\-]\d+|)'
		if match(dice_pattern, roll):
			vals_list = []
			modif_list = []

			sep = search(dice_pattern, roll)
			times = int(sep.group(1)) if sep.group(1) != '' else 1
			value = int(sep.group(2))
			modif = sep.group(3) or 0; mod = f'{modif[0]} {modif[1:]}' if modif != 0 else ''

			if times >= 100 or value >= 100000:
				await ctx.reply('A quantidade de dados não deve passar de 100000.')
				return

			for i in range(times):
				gen = randint(1, value)
				vals_list.append(gen)
				modif_list.append(f'{gen}+{modif}')

			if match(r'(\d+|)d(\d+)([\+\-]\d+|)', roll):
				result = eval(f'{sum(vals_list)}+{modif}')
			else:
				result = eval("+".join(modif_list))

			print(modif_list); print(vals_list); print(result)


			await ctx.reply(f'{result} ⟵ {sorted(vals_list, reverse=True)} {times}d{value} {mod}')


	@commands.command()
	async def password(self, ctx: commands.Context, lenght: int = 16, num: int = 5):
		nl = '\n'
		if lenght > 128 or num > 25:
			await ctx.send('Tamanho limite ultrapassado. Serão geradas 10 senhas de 128 digitos.')
			lenght, num = 128, 10 
		
		types = {'4️⃣':string.ascii_letters + string.digits + string.punctuation, '3️⃣':string.ascii_letters + string.digits, '2️⃣':string.ascii_letters, '1️⃣':string.digits}
		
		passhelp = await ctx.reply('A senhas serão enviadas para o seu privado. Reaja com um dos emojis: \n1️⃣ Números \n2️⃣ Letras \n3️⃣ Números e letras \n4️⃣ Todos os simbolos')
		for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']:
			await passhelp.add_reaction(emoji)
		
		try:
			def check(reaction: discord.Reaction, user):
				return str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣'] and user == ctx.author
			reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
		except AsyncTimeOutError:
			await passhelp.reply('O tempo de resposta acabou.', delete_after=5)
			return

		generator = types.get(reaction.emoji)
		generated = []

		for x in range(num+1):
			generating = ''
			for n in range(lenght+1):
				
				generating += choice(generator)
			generated.append(generating)

		await passhelp.delete()
		await ctx.reply('Senhas geradas. Cheque seu privado.')

		await ctx.author.send(f'Senhas geradas: \n{nl.join(generated)}')

	@commands.command(aliases=['qr'])
	async def qrcode(self, ctx: commands.Context, link):
		img: PilImage = qrcode.make(link)
		with BytesIO() as image_binary:
			img.save(image_binary, 'PNG')
			image_binary.seek(0)
			await ctx.reply(file=discord.File(fp=image_binary, filename=f'qr/{link[:15]}.png'))

def setup(client):
	client.add_cog(Utilities(client))
