import discord
from discord.ext import commands
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

# Text to Image Command
class TextToImage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(pass_context=True,name = "toimage", with_app_command = True, description ="I am an artist at heart", help = "Generates an image from the given text prompt.")
    async def textToImage(self, ctx, *, prompt: str):
        await ctx.send(f"Processing your prompt: {prompt}")
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
        headers = {"Authorization": "Bearer " + os.getenv("HUGGING_FACE_API_KEY")}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.content
        
        image_bytes = query({"inputs": prompt})

        # Ensure that the image is correctly generated
        if not is_valid_image(image_bytes):
            await ctx.send("Failed to generate a valid image. Please try again later.")
            return
        
        image = io.BytesIO(image_bytes)
        image_url = "attachment://image.png"

        # Send the file first
        file = discord.File(image, "image.png")
        message = await ctx.send(file=file)
        
        # Create and send the embed with the image
        embed = discord.Embed(title="Here is your generated image!")
        embed.set_image(url=image_url)
        
        await message.edit(embed=embed)

def is_valid_image(image_bytes):
    try:
        # Try to open the image bytes with PIL
        image = Image.open(io.BytesIO(image_bytes))
        image.verify() 
        return True
    except (IOError, SyntaxError) as e:
        print(e)
        return False

async def setup(bot):
    await bot.add_cog(TextToImage(bot))
