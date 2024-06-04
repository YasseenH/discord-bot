from discord.ext import commands
import PyPDF2
import discord
import requests
import os
import json
from io import BytesIO
from nltk.tokenize import sent_tokenize

# tldr: A command that takes a pdf file and creates a tldr for it
class TLDR(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def tldr(self, ctx, attachment : discord.Attachment):
        file_data = await attachment.read()
        await ctx.send("Processing...")
        pdf_stream = BytesIO(file_data)
        file_text = self.convert_text_from_pdf(pdf_stream)
        tldr_text = self.summarize_text(file_text)
        await ctx.send(tldr_text)

    def convert_text_from_pdf(self, pdf_stream: BytesIO):
        # Create a PdfReader object
        reader = PyPDF2.PdfReader(pdf_stream)
        pdf_text = [""]

        # Extract text from each page
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
        return ("".join(pdf_text[:]))

    def summarize_text(self, text: str):
        url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"
        payload = {
            "text": text,
            "num_sentences": self.count_sentences(text)
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": os.getenv('API_KEY'),
            "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(json.loads(response.text)['summary'])
        return (json.loads(response.text)['summary'])
    
    def count_sentences(self, text: str):
        sentences = text
        number_of_sentences = sent_tokenize(sentences)
        return len(number_of_sentences)


async def setup(bot):
    await bot.add_cog(TLDR(bot))