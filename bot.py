import os

from discord import Intents, Client
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
client: Client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord Server')

client.run(TOKEN)