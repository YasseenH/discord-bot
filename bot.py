#Import required dependicies
import os
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord Server')

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive!")

@client.command()
async def joke(ctx):
    joke_url = "https://joke3.p.rapidapi.com/v1/joke"
    JOKE_KEY = os.getenv('JOKE_API_KEY')

    headers = {
	"X-RapidAPI-Key": JOKE_KEY,
	"X-RapidAPI-Host": "joke3.p.rapidapi.com"
}

    response = requests.get(joke_url, headers=headers)
    await ctx.send(response.text)

client.run(TOKEN)