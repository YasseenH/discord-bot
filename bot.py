#Import required dependicies
import os, aiohttp
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json

load_dotenv()

intents: Intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord Server')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive!")

@bot.command()
async def joke(ctx):
    url = "https://official-joke-api.appspot.com/random_joke"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    await ctx.send(json.loads(response.text)['setup'])
    await ctx.send(json.loads(response.text)['punchline'])


bot.run(os.getenv('DISCORD_TOKEN'))