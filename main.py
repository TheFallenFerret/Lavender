#imports
import os
import random
import discord
import asyncio
from dotenv import load_dotenv
import praw
import inspirobot
import requests
import datetime
import discord_components
from discord_components import *
import time
from google_images_search import GoogleImagesSearch

#defining neccessary stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#reddit definitions
ID = os.getenv('REDDIT_ID')
SECRET = os.getenv('REDDIT_SECRET')
reddit = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent='script:LavenderBot:v1.2A (by u/LavenderTheNom)', check_for_async=False)

#google image definitions
GIS_API = os.getenv('GCS_DEVELOPER_KEY')
GIS_CX = os.getenv('GCS_CX')
gis = GoogleImagesSearch(GIS_API, GIS_CX)

ddb = Button()

#defining on_message
@client.event
async def on_message(message):

#GENERAL COMMANDS
  #suggestions
  if message.content.startswith('!suggest'):
    sug = '['+str(message.author)+'] suggested "'+str(message.content.replace("!suggest ", ""))+'"'
    cmdsug = str(message.author)+' suggested something!'
    print(cmdsug)
    with open('suggestions.txt', 'a') as f:
      print((sug), file=f)
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name= 'your suggestion was added, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
    await(await message.channel.send(embed=embed)).delete(delay=20)
    user = await client.fetch_user('438111061535621130')
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' suggested:',icon_url=str(message.author.avatar_url))
    embed.description = message.content.replace("!suggest ", "")
    await message.delete()
    await user.send(embed=embed)
  #hugs
  if message.content.startswith('!hug'):
    for user in message.mentions:
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_author(name=user.name + ' has been hugged by ' + message.author.name + ' UwU',icon_url=str(user.avatar_url))
      await message.delete()
      await message.channel.send(embed=embed)
  #ping
  if message.content.startswith('!ping'):
    rounded = round(client.latency*1000)
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name='Lavender is online, ' + message.author.name + '! Latency is ' + str(rounded) + 'ms.',icon_url=str(message.author.avatar_url))
    await message.delete()
    await message.channel.send(embed=embed)
  #pfp
  if message.content.startswith('!pfp'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_image(url=message.author.avatar_url)
    embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
    embed.set_author(name='Here\'s your pfp, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
    await message.delete()
    await message.channel.send(embed=embed)
  if message.content.startswith('!ptp'):
    for user in message.mentions:
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=user.avatar_url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here\'s ' + user.name + '\'s pfp, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      await message.delete()
      await message.channel.send(embed=embed)
  #inspirobot
  if message.content.startswith('!quote'):
    quote = inspirobot.generate()
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_image(url=str(quote))
    embed.set_footer(text='Generated from https://inspirobot.me/')
    embed.set_author(name='Here\'s your quote, ' + message.author.name + '!',icon_url='https://inspirobot.me/website/images/inspirobot-dark-green.png')
    await message.delete()
    await message.channel.send(embed=embed)
  #weather
  if message.content.startswith('!weather'):
    owmkey = os.getenv('OWM_KEY')
    city=message.content.replace('!weather ', '')
    georeq=requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + city + '&limit=5&appid=' + owmkey)
    geocache=georeq.json()
    latitude=geocache[0]['lat']
    longitude=geocache[0]['lon']
    onereq=requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(latitude) + '&lon=' + str(longitude) + '&units=imperial&exclude=alerts,hourly,minutely,currently&appid=' + owmkey)
    onecache=onereq.json()
    icon_url = 'http://openweathermap.org/img/wn/' + onecache['daily'][2]['weather'][0]['icon'] + '@2x.png'
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name='Today\'s Weather Forecast for ' + geocache[0]['name'] + ', ' + geocache[0]['state'])
    embed.set_thumbnail(url=icon_url)
    embed.description = '**Weather:** ' + str(onecache['daily'][2]['weather'][0]['description']) + '\n**Temperature:** ' + str(round(onecache['daily'][0]['temp']['day'])*1) + '°F\n**Humidity:** ' + str(onecache['daily'][0]['humidity']) + '%'
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  #server info
  if message.content.startswith('!server'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    datetime = message.guild.created_at
    embed.set_author(name=message.guild.name)
    embed.set_thumbnail(url=message.guild.icon_url)
    embed.add_field(name='Owner:', value=message.guild.owner, inline=False)
    embed.add_field(name='Members:', value=message.guild.member_count, inline=False)
    embed.add_field(name='Region:', value=message.guild.region, inline=False)
    embed.add_field(name='Creation Date:', value=datetime.strftime(r'%b %d, %Y'), inline=False)
    await message.delete()
    await message.channel.send(embed=embed)
  #russian roulette
  if message.content.startswith('!rr'):
    embed1 = discord.Embed()
    embed1.colour = 0xffb3f7
    embed1.set_author(name=message.author.name + ' spins the barrel...', icon_url='https://cdn.stateofthedapps.com/dapps/ruletka/logo_ruletka_6b0b97d3a01d943b29b43c102e0192687008eb7d6d70a5c0606812db9ed24d05_opti.png')
    embed2 = discord.Embed()
    embed2.colour = 0xffb3f7
    bullet = ['Click! ' + message.author.name + ' lives!', 'Click! ' + message.author.name + ' lives!', 'Click! ' + message.author.name + ' lives!', 'Click! ' + message.author.name + ' lives!', 'Click! ' + message.author.name + ' lives!', 'BANG! ' + message.author.name + ' dies!',]
    embed2.set_author(name=random.choice(bullet), icon_url='https://cdn.stateofthedapps.com/dapps/ruletka/logo_ruletka_6b0b97d3a01d943b29b43c102e0192687008eb7d6d70a5c0606812db9ed24d05_opti.png')
    await message.delete()
    sent = await message.channel.send(embed=embed1)
    await asyncio.sleep(4)
    await sent.edit(embed=embed2)
    await asyncio.sleep(7)
    await sent.delete()
  #google images api
  if message.content.startswith('!...'):
    imnm = random.randint(1,100)
    _search_params = {
    'q': 'Ferret Picture',
    'num': 1,
    'safe': 'off',
    'fileType': 'png',
    'imgType': 'photo',
    'imgSize': 'LARGE',}
    gis.search(search_params=_search_params, path_to_dir='fewwets/')
    await message.delete()
  if message.content.startswith('!358184'):
    await message.delete()
    ram = client.process.memory_full_info().rss / 1024**2
    await message.channel.send('Ram Usage: {ramUsage:.2f}')

#IMAGE COMMANDS
  #ferret
  if message.content.startswith('!ferret'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('ferrets').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #fox
  if message.content.startswith('!fox'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('foxes').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #cat
  if message.content.startswith('!cat'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('cats').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #dog
  if message.content.startswith('!dog'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('DogPics').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #border collie
  if message.content.startswith('!collie'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('BorderCollie').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #snow leopard
  if message.content.startswith('!snep'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('snowleopards').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #snek
  if message.content.startswith('!snek'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('Sneks').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break
  #horse
  if message.content.startswith('!horse'):
    while True:
      filetype = ('png', 'jpg', 'jpeg', 'gif')
      post = reddit.subreddit('Horses').random()
      url = str(post.url)
      embed = discord.Embed()
      embed.colour = 0xffb3f7
      embed.set_image(url=post.url)
      embed.set_footer(text='Hosted by 𝓣𝓲𝓶𝓶𝔂')
      embed.set_author(name='Here you go, ' + message.author.name + '!',icon_url=str(message.author.avatar_url))
      if url.endswith(filetype):
        await message.delete()
        await message.channel.send(embed=embed)
        if True:
          break

#DND
  if message.content.startswith('!roll d4'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,4)) + ' on a D4',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  if message.content.startswith('!roll d6'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,6)) + ' on a D6',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  if message.content.startswith('!roll d8'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,8)) + ' on a D8',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  if message.content.startswith('!roll d12'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,12)) + ' on a D12',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  if message.content.startswith('!roll d20'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,20)) + ' on a D20',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)
  if message.content.startswith('!roll d%'):
    embed = discord.Embed()
    embed.colour = 0xffb3f7
    embed.set_author(name=message.author.name + ' rolled ' + str(random.randint(1,100)) + ' on a Percentage Roll',icon_url='https://static.thenounproject.com/png/763027-200.png')
    await message.delete()
    await(await message.channel.send(embed=embed)).delete(delay=20)

#HELP
  if message.content.startswith('!help'):
    await message.delete()
    embed0 = discord.Embed()
    embed0.colour = 0xffc9f7
    embed0.title = '**__About Lavender__**'
    embed0.description = 'Lavender is a discord chatbot I created with the encouragement of some friends. Over time, it evolved into a multi-purpose bot with functions such as using InspiroBot, playing D&D, and using Reddit. Click the numbered buttons below to see some of her commands!'
    smsg = await message.channel.send(embed=embed0, 
    components=[[
      Button(style=ButtonStyle.blue, label='About'),
      Button(style=ButtonStyle.grey, label='1'),
      Button(style=ButtonStyle.grey, label='2'),
      Button(style=ButtonStyle.grey, label='3'),
      Button(style=ButtonStyle.red, label='Close')
    ]])

    t = time.time()
    while time.time() < t + 30:
      rmsg = await client.wait_for("button_click")
      if rmsg.component.label == '1':
        embed1 = discord.Embed()
        embed1.colour = 0xffc9f7
        embed1.title = '**__General Commands__**'
        embed1.description = '`!suggest [suggestion]` *(Puts an idea in a private suggestion box for review)*\n`!hug @[user]` *(hugs mentioned user X3)*\n`!ping` *(Gives Lav\'s ping)*\n`!pfp` *(Grabs your pfp and sends it in chat)*\n`!ptp @[user]` *(Sends the pfp of specified user in chat)*\n`!quote` *(Sends an AI generated quote)*\n`!weather [city name]` *(Sends the weather for selected city)*\n`!server` *(Sends info for current server)*\n`!rr` *(A game of russian roulette)*'
        await rmsg.respond(type=7, embed=embed1, 
        components=[[
          Button(style=ButtonStyle.blue, label='About'),
          Button(style=ButtonStyle.grey, label='1'),
          Button(style=ButtonStyle.grey, label='2'),
          Button(style=ButtonStyle.grey, label='3'),
          Button(style=ButtonStyle.red, label='Close')
        ]])
      if rmsg.component.label == '2':
        embed2 = discord.Embed()
        embed2.colour = 0xffc9f7
        embed2.title = '**__Image Commands__**'
        embed2.description = '`!ferret` *(Sends a random pic of a ferret)*\n`!fox` *(Sends a random pic of a fox)*\n`!cat` *(Sends a random pic of a cat)*\n`!dog` *(Sends a random pic of a dog)*\n`!collie` *(Sends a random pic of a border collie)*\n`!snep` *(Sends a random pic of a snow leopard)*\n`!snek` *(Sends a random pic of a snake)*\n`!horse` *(Sends a random pic of a horse)*'
        await rmsg.respond(type=7, embed=embed2, 
        components=[[
          Button(style=ButtonStyle.blue, label='About'),
          Button(style=ButtonStyle.grey, label='1'),
          Button(style=ButtonStyle.grey, label='2'),
          Button(style=ButtonStyle.grey, label='3'),
          Button(style=ButtonStyle.red, label='Close')
        ]])
      if rmsg.component.label == '3':
        embed3 = discord.Embed()
        embed3.colour = 0xffc9f7
        embed3.title = '**__D&D Commands__**'
        embed3.description = '`!roll d4` *(Rolls 4 sided dice)*\n`!roll d6` *(Rolls 6 sided dice)*\n`!roll d8` *(Rolls 8 sided dice)*\n`!roll d12` *(Rolls 12 sided dice)*\n`!roll d20` *(Rolls 20 sided dice)*\n`!roll d%` *(Rolls percentage dice)*'
        await rmsg.respond(type=7, embed=embed3, 
        components=[[
          Button(style=ButtonStyle.blue, label='About'),
          Button(style=ButtonStyle.grey, label='1'),
          Button(style=ButtonStyle.grey, label='2'),
          Button(style=ButtonStyle.grey, label='3'),
          Button(style=ButtonStyle.red, label='Close')
        ]])
      if rmsg.component.label == 'About':
        await rmsg.respond(type=7, embed=embed0, 
        components=[[
          Button(style=ButtonStyle.blue, label='About'),
          Button(style=ButtonStyle.grey, label='1'),
          Button(style=ButtonStyle.grey, label='2'),
          Button(style=ButtonStyle.grey, label='3'),
          Button(style=ButtonStyle.red, label='Close')
        ]])
      if rmsg.component.label == 'Close':
        await smsg.delete()
    await smsg.delete()

@client.event
async def on_ready():
  discord_components.DiscordComponents(client)

#status
@client.event
async def ch_pr():
  await client.wait_until_ready()
  listboi = 0
  statuses = ['in ' + str(len(client.guilds)) + ' servers | !help', 'with ' + str(sum((guild.member_count) for guild in client.guilds)) + ' users | !help', 'on Linode | !help', 'at ' + str(round(client.latency*1000)) + ' ms | !help', '!ferret | !hug | !pfp', 'on Python 3.8.8 | !help']
  while not client.is_closed():
    status = statuses[listboi]
    await client.change_presence(activity=discord.Game(name=status))
    await asyncio.sleep(10)
    listboi += 1
    if listboi >= 5:
      listboi = 0

#run
client.loop.create_task(ch_pr())
client.run(TOKEN)
