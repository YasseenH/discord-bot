##
##
# This file holds old commands and functions for testing purposes
##
##

# #Join_Voice: Simple Command that allows the Bot to join the voice channel
# @bot.command(pass_context = True)
# async def join_voice(ctx):
#     if (ctx.author.voice):
#         channel = ctx.message.author.voice.channel
#         await channel.connect()
#     else:
#         await ctx.send("There's no one in the voice channel")

# #Leave_Voice: Simple Command that allows the Bot to leave the voice channel
# @bot.command(pass_context = True)
# async def leave_voice(ctx):
#     if (ctx.voice_client):
#         await ctx.guild.voice_client.disconnect()
#         await ctx.send("I left")
#     else:
#         await ctx.send("I am not in the voice channel")