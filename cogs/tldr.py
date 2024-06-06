from discord.ext import commands
import PyPDF2
import discord
import requests
import os
import json
from io import BytesIO
from nltk.tokenize import sent_tokenize
import google.generativeai as genai

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
        print(tldr_text)
        with open("Output.txt", "w") as text_file:
            text_file.write(tldr_text)
        await ctx.send("Here is your TLDR:")
        await ctx.send(file=discord.File("Output.txt"))
        os.remove("Output.txt")

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
        # Uses Gemini AI to summarize text
        # TODO: Allow the user to type in the prompt or use the default TLDR prompt
        genai.configure(api_key=(os.getenv('GEMINI_KEY')))
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Here")
        response = model.generate_content("Summarize this text in detail for a college student taking notes: " + text)
        return response.text
    
    def count_sentences(self, text: str):
        sentences = text
        number_of_sentences = sent_tokenize(sentences)
        return len(number_of_sentences)

async def setup(bot):
    await bot.add_cog(TLDR(bot))