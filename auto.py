import discord
from discord.ext import commands, tasks
from discord.ui import Select
import asyncio
import random
import aiohttp
import asyncpraw as praw
import pymongo
import pybooru
import datetime as dt
from dateutil import parser 
import regex as re
from DisWebhook import DisWebhook as webhok 
from DisWebhook import Embed 

from nsfw import danime_api
from baka import Baka









tags = Baka.tag()

mongodb_url = Baka.mongodb()
mongodb_url = mongodb_url[0]

db = "AbodeDB"

da = pymongo.MongoClient(mongodb_url)
db = da[db]

eco = da['Harsh2']
color = 0x8F00FF
select_option = ["sup", "hi"]

re = Baka.reddit()

r_client_secret = re[0]
r_client_id = re[1]
r_client_username = re[2]
r_client_pass = re[3]
r_client_agent = "Jr. Kelly"


guild_report = 1124978993905553518
img_report = 1126546382501711912
r_list = ["Artistic_Hentai", "HentaiAI", "AnimeNude"]

class Button(discord.ui.View):
    def __init__(self, bot, link):
        super().__init__()
        self.bot = bot
        self.link = link

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def Decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        img_admin_role = discord.utils.get(member.roles, name="img_admin")
        if img_admin_role:
            button.disabled = True
            await interaction.response.edit_message(content="Decline!", view=self)
            await interaction.message.delete()



    @discord.ui.button(label="Approve!", style=discord.ButtonStyle.green)
    async def Approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        img_admin_role = discord.utils.get(member.roles, name="img_admin")
        if img_admin_role:
            button.disabled = True
            await interaction.response.edit_message(content="Type tags separated by comma `,` or period `.`!", view=self)

            def check_author_and_role(m):
                return m.author == interaction.user and img_admin_role in m.author.roles

            try:
                user_input = await self.bot.wait_for('message', check=check_author_and_role, timeout=180)
            except asyncio.TimeoutError:
                await interaction.followup.send("Timeout: No valid input received.")
                return
            input_content = user_input.content

            # Split input based on commas or periods
            tables = re.split(r'[,\.]', input_content)

            # Insert data into each table
            for table_name in tables:
                collection = db[table_name]
                data = collection.find_one({"_id": self.link})

                if not data:
                    data = {
                        '_id': self.link
                    }
                    collection.insert_one(data)

            await interaction.followup.send(f"Received input: {input_content}")



class img_button(discord.ui.View):
    def __init__(self, bot, link, tag):
        super().__init__()
        self.bot = bot
        self.link = link
        self.tag = tag



    @discord.ui.button(label="Delete!", style=discord.ButtonStyle.danger)
    async def delete__(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        img_admin_role = discord.utils.get(member.roles, name="img_admin")
        global db
        
        db = db[str(self.tag)]
        data = db.find_one({"_id": str(self.link)})

        if img_admin_role:
            button.disabled = True
            if data:
                db.delete_one(data)
            await interaction.message.delete()


class r_Button(discord.ui.View):
    def __init__(self, bot, link, tag):
        super().__init__()
        self.bot = bot
        self.link = link
        self.tag = tag


    @discord.ui.button(label="Report!", style=discord.ButtonStyle.danger)
    async def report_(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        img_admin_role = discord.utils.get(member.roles, name="img_admin")
        if img_admin_role:
            button.disabled = True
            await interaction.response.edit_message(content="Reported!", view=self)
            # await interaction.response.defer()
            await interaction.message.delete()

            guild = self.bot.get_guild(guild_report)
            channel = guild.get_channel(img_report)
            try:
                em = discord.Embed()
                em.color = color
                em.description  = "A reported image!"
                em.set_image(url=self.link)
                await channel.send(embed=em, view=img_button(self.bot, self.link, self.tag))
            except Exception as r:
                print(r)




class Auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.danime_api = danime_api(self.bot)
        self.db_img.start()
        self.top_img.start()
        
    def unload_cog(self):
        self.send_img.cancel()
        self.top_img.cancel()
        print('Tasks has been cancaled')
        




    def get_top_img(self):
        results = self.bot.collection_db['nutt']
        results = list(results.find().sort('nutt', pymongo.DESCENDING))
        return results


    @tasks.loop(minutes=120)
    async def top_img(self):
        try:
            
            g = self.bot.get_guild(1124978993905553518)
            chan = g.get_channel(1130512868660478034)
            await chan.purge(limit=100)
            embed = discord.Embed()
            img = self.get_top_img()
            num = 0
            for _ in range(5):
                my_msg = webhok(username="Jr Kelly.", avatar_url=g.icon.url, url="https://discord.com/api/webhooks/1134957150440017970/fI4QFfl-ePMXE5YT-PJt9p80nEuKD71KtmkHUdRLOxs61kILbyb7Na9e13R4MGCt5bNr")
                d_emb = Embed(title = f"Position: {num+1}", description = f"Total Nutts: {img[num]['nutt']}")
                d_emb.set_image(url=img[num]['_id'])
                num += 1 
                my_msg.send(embed=d_emb)

        except Exception as r:
            print(r)
















































    @tasks.loop(seconds=10000)
    async def db_img(self):
        try:
        
            chan = 1126911855256936460
            guild_id = 1124978993905553518
            guild = self.bot.get_guild(guild_id)
            channel = guild.get_channel(chan)

            tag = random.choice(tags)
            data = await self.danime_api.get_img_nsfw(ctx=None, tag = tag)
            
            link = data
            tag = tag

                
            em = discord.Embed()
            em.color  = color
            em.title = tag
            em.set_image(url=link)
            await channel.send(embed=em, view=r_Button(self.bot, link, tag))
         
        except Exception as r:
            print(r)
           
        











        
    @tasks.loop(minutes=5)
    async def booru_img(self):
        chan = 1126911530814951447
        guild_id = 1124978993905553518
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(chan)
        v = discord.ui.View()
        # print(Danbooru)
        booru = pybooru.Danbooru("danbooru", username= "Jr-Kelly" ,api_key="CNerw4STWe1N2Yg51E4T3tLa")

        b_tags_search = tags
        b_tags_search = random.choice(b_tags_search)
        # print("JH")
        al = []
        a = booru.post_list(tags=b_tags_search, limit=200)
        s = None
        for a in a:
            # print(a['media_asset']['variants'][4]['url'])
            try:
                al.append(a['media_asset']['variants'][3]['url'])
            except Exception:
                continue
        
        try:
            s = random.choice(al)
        except Exception:
            return

        
            
        e=discord.Embed()
        e.color =color
        e.set_image(url=s)
        await channel.send(embed=e, view=Button(bot=self.bot, link=s))




        

async def setup(bot):
    await bot.add_cog(Auto(bot))
