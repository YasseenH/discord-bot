#Import required dependicies
import asyncio
import os
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

#Loads the keys from my .env file
load_dotenv()

intents: Intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#The on-message when the bot enters the server
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord Server')

async def load_extensions():
    initial_extensions = []
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