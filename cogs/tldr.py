from discord.ext import commands
from discord import app_commands
import PyPDF2
import discord
import os
from io import BytesIO
from nltk.tokenize import sent_tokenize
import google.generativeai as genai

# tldr: A command that takes a pdf file and creates a tldr for it
class TLDR(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="tldr", description="Make your pdf file easier to understand", with_app_command = True, help="Summarizes the content of a PDF file.")
    async def tldr(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("No PDF File Found. Please attach a PDF file.")
            return

        try:
            if not attachment.filename.endswith(".pdf"):
                await ctx.send("The attached file is not a PDF. Please attach a PDF file.")
                return
            
            attachment = ctx.message.attachments[0]
            file_data = await attachment.read()

            await ctx.send("Processing...")

            pdf_stream = BytesIO(file_data)
            file_text = self.convert_text_from_pdf(pdf_stream)
            tldr_text = self.summarize_text(file_text)

            # Write the summary to a text file and send it
            with open("Output.txt", "w") as text_file:
                text_file.write(tldr_text)
            
            await ctx.send("Here is your TLDR:")
            await ctx.send(file=discord.File("Output.txt"))

            # Clean up the output file
            os.remove("Output.txt")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

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
        genai.configure(api_key=(os.getenv('GEMINI_KEY')))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Summarize the following text: \"" + text + "\" for note-taking purposes at a college level. Focus on capturing the key points, main arguments, and any significant details. Ensure the summary is clear, concise, and organized in a way that would be useful for study and review.")
        return response.text

async def setup(bot):
    await bot.add_cog(TLDR(bot))