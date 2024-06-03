from discord.ext import commands
import requests
import json

#Joke Command: Uses a joke API to print a simple joke
class Joke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def joke(self, ctx):
        url = "https://official-joke-api.appspot.com/random_joke"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        await ctx.send(json.loads(response.text)['setup'])
        await ctx.send(json.loads(response.text)['punchline'])

async def setup(bot):
    await bot.add_cog(Joke(bot))