import discord
from discord.ext import commands, tasks
from baka import Baka

import random

import pymongo






mongodb_url = Baka.mongodb()[0]
sauce_api = Baka.sauce()
database_name = 'Harsh2'
collection_name = 'economy'
prim_name = "prime"

list_check_id = ['2']




a = Baka.guild()


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('`'), intents=intents)
guild = bot.get_guild(a[0])
token = Baka.token()



@tasks.loop(seconds=10000)
async def statusloop():
	await bot.wait_until_ready()
	a = ['`help', 'Auto Images', "Refreshments", 'Kelly!', "Your Heart!!"]
	name = random.choice(a)
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=name))
   




owners = [947838163974504489, 850235530695540736]






bot.owners = owners
bot.afk_users = {}

bot.sauce_api = sauce_api
bot.mongodb_url = mongodb_url
bot.list_check_id = list_check_id
bot.database_name = database_name
bot.collection_name = "main"
bot.disabled_owner = []

bot.collection_Client = pymongo.MongoClient(bot.mongodb_url)
bot.collection_db = bot.collection_Client['Harsh2']



bot.collection_main = bot.collection_db['main']
bot.collection_level = bot.collection_db['level']
bot.collection_prim = bot.collection_db['prime']


bot.collection_command = bot.collection_db['config']
bot.version = "2.3.7"


# data = {
#        'guild_id': 0,
#        'starboard': 0,
#        'news-channel': 0,
#        "commands": {'afk': 'channel.id'}
#
#   
#    }













# Bot-wide cooldown duration in seconds
bot_cooldown_duration = 10

# Dictionary to store user cooldown timestamps
user_cooldowns = {}





@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore errors when the command is not found.
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide all the required arguments for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please provide valid arguments for this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

    




@bot.command()
async def foo(ctx):
	await ctx.send(f"{ctx.author.name} just farted!")


@bot.event
async def on_ready():
	statusloop.start()

	print('-------------------------')
	await bot.load_extension('auto')
	print('Loaded Cog: Auto')
	print('-------------------------')


	print(f"Logged in as: {bot.user}")


bot.run(token)