from discord.ext import commands
import requests
import json
import time

# Joke Command: Uses a joke API to print a simple joke
class Joke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="joke", description="I'm a funny guy look at me", with_app_command = True, help="Sends a random joke.")
    async def joke(self, ctx):
        url = "https://official-joke-api.appspot.com/random_joke"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        
        if response.status_code == 200:
            # Sends the Joke from the url
            await ctx.send(json.loads(response.text)['setup'])
            time.sleep(3)
            await ctx.send(json.loads(response.text)['punchline'])
        else:
            await ctx.send("Failed to retrieve a joke. Please try again later.")

async def setup(bot):
    await bot.add_cog(Joke(bot))