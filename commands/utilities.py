import random
import sqlite3

import discord
import asyncpraw
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
		db.commit()
		db.close()

	@commands.command(
		help='Mostra um artigo sobre o assunto escolhido.'
	)
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

	@commands.command(
		help='Mostra uma postagem aleatória do subreddit escolhido entre os 50 melhores.'
	)
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
				await ctx.send("Calma lá amigão, esse subreddit não é FamIlY FrIenDlY")
				return

			async for submission in subreddit.hot(limit=50):
				if submission.url[-3:] in ["jpg", "png", "gif"]:
					sub_list.append(submission)

			submission = random.choice(sub_list)

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


def setup(client):
	client.add_cog(Utilities(client))
