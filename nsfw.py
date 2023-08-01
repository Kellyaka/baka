import discord
from discord.ext import commands
import hmtai
import random
import requests
import json
import pymongo
import random
import aiohttp
import aiosqlite





class danime_api:
	def __init__(self, Bot):
		self.Bot = Bot
		self.bot = self.Bot
		self.mongo_client = self.bot.collection_Client
		self.database = self.mongo_client['AbodeDB']
        ## self.collection = self.database[collection_name]
        ## self.prim_collection = self.database[prim_name]


    

	async def get_img_nsfw(self, ctx, tag):
		col = self.database[str(tag)]
		img = col.aggregate([{'$sample': {'size': 10}}])


		for data in img:
			# print(data)
			return data["_id"]









	async def get_img(self, ctx, tag):
		url = hmtai.get("hmtai", tag)
		return url

	async def get_nekobot_img(self, ctx, tag):
		url = hmtai.get("nekobot", tag)
		return url


	async def get_random_nsfw(self, ctx, tag):
		r = random.choice(['a', 'b'])
		if r == 'a':
			await self.get_img(ctx, tag)

		else:
			await self.get_nekobot_img(ctx, tag)




	async def image_embed(self, ctx, tag, dl=None):

		link = await self.get_img(ctx, tag)

		embed = discord.Embed(color =0x7fcbff)
		embed.description = f"Bad image? [Report it](https://discord.gg/Tvv4UtFcdR)"
		if dl:
			embed.description=f"{dl}"
		embed.set_image(url=f"{link}")
		await ctx.send(embed=embed)


	def get_nutt_harsh_table(self, link):
		"""Gives Nutt amount:str that is saved in Harsh's data returns 0:str if data not exist"""

		a = link
		data =   self.bot.collection_db['nutt'].find_one({"_id": a})

		if not data:
			return str(0)

		else:
			return data['nutt']



	async def image_embed_nsfw(self, ctx, tag, dl=None):
		link = await self.get_img_nsfw(ctx, tag)



		nutts = self.get_nutt_harsh_table(link)


		embed = discord.Embed(color =0x7fcbff)
		embed.description = f"Bad image? [Report it](https://discord.gg/Tvv4UtFcdR)"
		if dl:
			embed.description=f"[Link]({dl})"
		# print(link)
		embed.set_image(url=f"{link}")
		embed.set_footer(text=f"Total Nutts: {nutts}")
		await ctx.send(embed=embed, view=n_Buttons(self.Bot, link=link, ctx=ctx))
		# await ctx.send("test", view=NutButtons())
		# await ctx.send("test", view=Buttons())



















	async def image_embed_nek(self, ctx, tag, dl=None):


		link = await self.get_nekobot_img(ctx, tag)

		embed = discord.Embed(color =0x7fcbff)
		embed.description = f"Bad image? [Report it](https://discord.gg/Tvv4UtFcdR)"
		if dl:
			embed.description=f"[Link]({dl})"
		embed.set_image(url=f"{link}")
		await ctx.send(embed=embed)
