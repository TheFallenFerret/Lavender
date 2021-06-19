#imports
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

#definitions
bot = commands.Bot(command_prefix='!')
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#general commands
@bot.command()
async def suggest(ctx):
  await ctx.message.delete()
  embed = discord.Embed()
  embed.colour = 0xffb3f7
  embed.set_author(name= 'Your suggestion was added, ' + ctx.author.name + '!',icon_url=str(ctx.author.avatar_url))
  await(await ctx.send(embed=embed)).delete(delay=20)
  user = await bot.fetch_user('438111061535621130')
  embed = discord.Embed()
  embed.colour = 0xffb3f7
  embed.set_author(name=ctx.author.name + ' suggested:',icon_url=str(ctx.author.avatar_url))
  embed.description = ctx.message.content.replace("!suggest ", "")
  await user.send(embed=embed)
@bot.command()
async def hug(ctx):
  await ctx.message.delete()
  for user in message.mentions:
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=user.name + ' has been hugged by ' + ctx.author.name + ' UwU',icon_url=str(user.avatar_url))
    await message.delete()
    await message.channel.send(embed=embed)
@bot.command()
async def join(ctx):
  channel = ctx.author.voice.channel
  source = discord.FFmpegPCMAudio('voice/FirstLine.mp3')
  await channel.connect()
  await ctx.voice_client.play(source)
@bot.command()
asv  ync def play(ctx):
  
@bot.command()
async def leave(ctx):
  await ctx.voice_client.disconnect()

bot.run(TOKEN)