import os

from discord import Client, Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord Server')

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive!")

client.run(TOKEN)