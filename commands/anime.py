import discord
import mal
from discord.ext import commands

# TODO Asynchronous MAL functions

class Anime(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.group()
	async def mal(self, ctx):
		pass

	@mal.command()
	async def anime(self, ctx, * , anime):
		anime: mal.Anime = mal.Anime(mal.AnimeSearch(anime).results[0].mal_id)

		for original, trans in {'Currently Airing':'⬆️Estreando', 'Not yet aired':'📆Ainda Não Estrou', 'Finished Airing':'✅Finalizado'}.items():
			if anime.status.replace(original, trans) in ['⬆️Estreando', '📆Ainda Não Estrou', '✅Finalizado'] :
				new_anime_status = anime.status.replace(original, trans)

		msg = discord.Embed(title=anime.title, description=anime.synopsis, url=anime.url)
		msg.add_field(name='Tipo', value=anime.type)
		msg.add_field(name=f'{new_anime_status[0]} Status', value=new_anime_status[1:])
		msg.add_field(name='📆 Estreia', value=anime.premiered)
		msg.add_field(name='🌟 Score', value=anime.score)
		msg.add_field(name='🤩 Popularidade', value=f'#{anime.popularity}')
		msg.add_field(name='📼 Episódios', value=anime.episodes)
		msg.add_field(name='Origem', value=anime.source)
		msg.add_field(name='Gêneros', value=', '.join(anime.genres))
		msg.set_thumbnail(url=anime.image_url)
		msg.set_footer(text=f'🏅 Rank #{anime.rank}')

		await ctx.send(embed=msg)

	@mal.command()
	async def manga(self, ctx, * , manga):
		manga: mal.Manga = mal.Manga(mal.MangaSearch(manga).results[0].mal_id)

		for original, trans in {'Publishing':'⬆️Publicando', 'Not yet published':'📆Ainda Não Publicado', 'Finished':'✅Finalizado', 'Discontinued':'😭Abandonado', 'On Hiatus':'😴Em Hiato'}.items():
			if manga.status.replace(original, trans) in ['⬆️Publicando', '📆Ainda Não Publicado', '✅Finalizado', '😭Abandonado', '😴Em Hiato'] :
				new_manga_status = manga.status.replace(original, trans)

		msg = discord.Embed(title=manga.title, description=manga.synopsis, url=manga.url)
		msg.add_field(name='📄 Capitulos', value=manga.chapters)
		msg.add_field(name='📓 Volumes', value=manga.volumes)
		msg.add_field(name='🤩 Popularidade', value=manga.popularity)
		msg.add_field(name='🌟 Score', value=manga.score)
		msg.add_field(name=f'{new_manga_status[0]} Status', value=new_manga_status[1:])
		msg.add_field(name='📆Publicado', value=manga.published)
		msg.add_field(name='Tipo', value=manga.type)
		msg.add_field(name='Gêneros', value=', '.join(manga.genres))
		msg.set_thumbnail(url=manga.image_url)
		msg.set_footer(text=f'🏅 Rank #{manga.rank}')

		await ctx.send(embed=msg)

def setup(client):
	client.add_cog(Anime(client))