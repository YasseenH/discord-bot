# Import required dependicies
import asyncio
import os
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

# Loads the keys from my .env file
load_dotenv()

# Updates the intents for the bot and sets '!' as the command prefix
intents: Intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# The on-message when the bot enters the server
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord Server')

# Hello Command: Prints a simple message
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive and Nothing!")

# Loads all of the Cogs from other files
async def load_extensions():
    initial_extensions = []
    # Gets all the Cog files in "cogs.<FileName>" format
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            initial_extensions.append("cogs." + file[:-3])
    for extension in initial_extensions:
            await bot.load_extension(extension)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))

asyncio.run(main())