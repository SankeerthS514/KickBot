import os
import discord
import requests
import json
import random
import urlopen
import threading
import asyncio
from bs4 import BeautifulSoup

from asyncio import sleep as s 
from discord.ext import commands
from keep_alive import keep_alive

mlist=[]

client = commands.Bot(command_prefix = '!')

def get_time():
  response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Kolkata")
  time = (response.json()["datetime"])[11:16]
  return(time)

def embedIt(toEmbed,ratings,title):
  embed = discord.Embed(
    colour=discord.Colour.random()
  )
  count=1
  embed.title=(title)
  for each in toEmbed:

    embed.add_field(name=str(count).strip()+')',value=each.text+' : '+ratings[toEmbed.index(each)],inline=False)
    count=count+1
  return(embed)

def embedIt2(toEmbed,title):
  embed = discord.Embed(
    colour=discord.Colour.random()
  )
  count=1
  embed.title=(title)
  for each in toEmbed:
    embed.add_field(name=str(count).strip()+')',value=each.text,inline=False)
    count=count+1
  return(embed)

@client.event
async def on_ready():
  
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return


  if 'Hello' in message.content.lower():
    await message.channel.send("Hi")

  await client.process_commands(message)

@client.command()
async def getout(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send('Goodbye',tts=True)
    await member.edit(voice_channel=None)

@client.command()
async def move(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send('Join Here',tts=True)
    await member.edit(voice_channel=ctx.author.voice.channel)

@client.command()
async def sus(ctx,member : discord.Member,*,reason=None):
  if member.id!=617732810115121163:
    await ctx.send('Move to the other VC')
    for i in ctx.message.guild.channels:
      if i.id==859454337130168362:
        channel=i

    await member.edit(voice_channel=channel)


@client.command()
async def Mute(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send("Please Be Silent",tts=True) 
    await member.edit(mute = True)


@client.command()
async def unMute(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send("You may now Speak",tts=True) 
    await member.edit(mute = False)

@client.command(pass_context=True)
async def movierem(ctx,time: int,*,message):
  await ctx.send("Ok i will remind you in "+str(time)+" minutes, Goodbye")
  await s(60*time)
  await ctx.send("@everyone let's watch "+f'{message}'+" tonight",tts=True)

@client.command()
async def remind(ctx,*,message):
  
  t2=message.split(' ')[0].split(':')
  while True:
    await s(5)
    t=str(get_time()).split(':')
    if(int(t[0])>12):
      t[0]=str(int(t[0])-12)
    if t[0]==t2[0] and t[1]==t2[1]:
      await ctx.send("Hello there, here's the reminder you asked for: "+message,tts=True)
      break

@client.command(pass_context = True)
async def spam(ctx, member : discord.Member, *, content: str):
  for i in range(1,10):
    channel = await member.create_dm()
    await channel.send('<@!'+str(member.id)+'>'+content)

@client.command(pass_context = True)
async def valorant(ctx):
  channel=ctx.message.guild.id
  if(channel==678223464699789312):
    await ctx.send('<@!455705329443930113><@!456649200155754506><@!690148550558220294><@!442598851656941592><@!617732810115121163><@!442639977764093954><@!792641729320714251><@!518047377064591399><@!605423783590887427><@!715544344819662901><@!582964437284290580>'+"We playin valorant?")


@client.command(pass_context = True)
async def imdb(ctx,*,content: str):
  movie = content.strip().split(' ')
  mov = ""
  for word in movie:
    if(mov==""):
      mov=word
    else:
      mov = mov + "+" + word
  website=requests.get('https://www.imdb.com/find?q='+mov+'&ref_=nv_sr_sm').text
  soup = BeautifulSoup(website,'lxml')
  options = soup.find('table',class_="findList")
  movies = options.find_all('tr')
  ratings=[]
  for i in movies:
    link2='https://www.imdb.com/'+str(i.td.a['href'])
    website2=requests.get(link2).text
    soup2 = BeautifulSoup(website2,'lxml')
    rating = soup2.find('span',class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV")
    if(rating):
      ratings.append(rating.text)
    else:
      ratings.append('None')
  sent=await ctx.send(embed=embedIt(movies,ratings,"Your Search Results uWu"))
  sent2=await ctx.send("Which movie would you like to check out, You have 10 seconds to respond!")
  try:
    choice = await ctx.bot.wait_for("message",timeout=10,check=lambda message: message.author==ctx.author and message.channel==ctx.channel)
    if choice:
      await ctx.send("Here's the link:")
      link='https://www.imdb.com/'+str(movies[int(choice.content)-1].td.a['href'])
      await ctx.send(link)
      website2=requests.get(link).text
      soup = BeautifulSoup(website2,'lxml')
      rating = soup.find('span',class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV")
      if(rating):
        r=rating.text
      else:
        r='None'
      A=soup.find('div',class_="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty")
      B=A.find_all('ul')
      C=B[1].find_all('li')
      D=C[2].find('div',class_="ipc-metadata-list-item__content-container")
      E=D.find_all('a')     
      sent=await ctx.send("Would you like the details for this movie? You have 5 seconds to reply")
      try:
        choice = await ctx.bot.wait_for("message",timeout=5,check=lambda message: message.author==ctx.author and message.channel==ctx.channel)
        if 'y' in choice.content or 'Y' in choice.content:
          await ctx.send("Here are the details you asked for:")
          await ctx.send(f'The IMDb Rating is: {r}')
          await ctx.send(embed=embedIt2(E,"The Genres of this movie:"))
        else:
          await ctx.send("Sorry you took too long")

      except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Sorry you took too long>.<",delete_after=10)

  except asyncio.TimeoutError:
    await sent.delete()
    await sent2.delete()
    await ctx.send("Sorry you took too long>.<",delete_after=10)
  


@client.command(pass_context = True)
async def addmovie(ctx,*,content: str):
  file = open('Votes.txt','a')
  file.write(content.strip()+'\n')
  file.close()

@client.command(pass_context = True)
async def Laugh(ctx):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    channel = ctx.author.voice.channel #gets channel
    await channel.connect() #connects to channel
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('Laugh.mp3')
    voice_client.play(audio_source, after=None)
    await asyncio.sleep(4)
    await ctx.voice_client.disconnect()

@client.command(pass_context = True)
async def delmovie(ctx,*,content: str):
  f1 = open('Votes.txt', "r")
  lines = f1.readlines()
  f1.close()
  f2 = open('Votes.txt', "w")
  for line in lines:
      if content.lower() not in line.strip("\n").lower():
          f2.write(line)
  f2.close()
  await ctx.send("Deleted")


@client.command(pass_context = True)
async def votelist(ctx):
  file = open('Votes.txt','r')
  embed = discord.Embed(
    colour=discord.Colour.teal()
  )
  count=1
  embed.set_author(name="The Voting List: ")
  embed.set_thumbnail(url=ctx.message.author.avatar_url)
  movies=[]
  for each in file:
    embed.add_field(name=str(count).strip()+')',value=each,inline=False)
    movies.append(each)
    count=count+1
  message=await ctx.send(embed=embed)
  res = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
  for i in range(count-1):
    await message.add_reaction(res[i])
  mes2=await ctx.send("You have 10 minutes to vote")
  await s(20)
  await mes2.delete()
  await ctx.send("The winner is...",delete_after=5)
  await s(5)
  maxcount=0
  winner=0
  message = await ctx.channel.fetch_message(message.id)
  for i in message.reactions:
    if i.count>maxcount:
      maxcount=i.count
      winner=i.emoji
  await message.delete()  
  await ctx.send(f'{movies[res.index(winner)].strip()} !!!')

keep_alive()
client.run(os.getenv('TOKEN'))


