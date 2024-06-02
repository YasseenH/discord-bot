#Import required dependicies
import os
from discord import Intents
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json

#Loads the keys from my .env file
load_dotenv()

intents: Intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#The on-message when the bot enters the server
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord Server')

#Hello Command: Prints a simple message
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am alive!")

#Joke Command: Uses a joke API to print a simple joke
@bot.command()
async def joke(ctx):
    url = "https://official-joke-api.appspot.com/random_joke"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    await ctx.send(json.loads(response.text)['setup'])
    await ctx.send(json.loads(response.text)['punchline'])

#Join_Voice: Simple Command that allows the Bot to join the voice channel
@bot.command(pass_context = True)
async def join_voice(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("There's no one in the voice channel")

#Leave_Voice: Simple Command that allows the Bot to leave the voice channel
@bot.command(pass_context = True)
async def leave_voice(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left")
    else:
        await ctx.send("I am not in the voice channel")

import PyPDF2
from io import BytesIO
from nltk.tokenize import sent_tokenize

#tldr: A command that takes a pdf file and creates a tldr for it
@bot.command(pass_context = True)
async def tldr(ctx, attachment : discord.Attachment):
    await ctx.defer()
    file_data = await attachment.read()
    await ctx.send("Processing...")
    pdf_stream = BytesIO(file_data)
    file_text = convert_text_from_pdf(pdf_stream)
    print(file_text)
    tldr_text = summarize_text(file_text)
    await ctx.send(tldr_text)


def convert_text_from_pdf(pdf_stream: BytesIO):
    # Create a PdfReader object
    reader = PyPDF2.PdfReader(pdf_stream)
    pdf_text = [""]

    # Extract text from each page
    for page in reader.pages:
        content = page.extract_text()
        pdf_text.append(content)
    
    return ("".join(pdf_text[:]))

def count_sentences(text: str):
    sentences = text
    number_of_sentences = sent_tokenize(sentences)
    return len(number_of_sentences)

def summarize_text(text: str):
    url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"
    payload = {
        "text": text,
        "num_sentences": count_sentences(text)
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('API_KEY'),
        "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(json.loads(response.text)['summary'])
    return (json.loads(response.text)['summary'])

bot.run(os.getenv('DISCORD_TOKEN'))