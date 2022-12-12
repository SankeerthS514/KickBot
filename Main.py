import os
import discord
import requests
import asyncio
from replit import db
from bs4 import BeautifulSoup

from asyncio import sleep as s 
from discord.ext import commands
from keep_alive import keep_alive

mlist=[]

client = commands.Bot(command_prefix = '!')

commands={}


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

  #Numbers = [1,2,3,4,5]

  if message.author == client.user:
    return

  if any(word in message.content.lower() for word in db.keys()):
    for i in message.content.lower().split():
      if i in db.keys():
        await message.channel.send(db[i])

  if message.content.startswith('-'):
    customs = open("Customs.txt","r")
    check = message.content[1:].strip(" ")
    for i in customs.readlines():
      if check in i:
        invites = open(check+".txt","r")
        await message.channel.send(invites.readline())
        break

  
        
  await client.process_commands(message)




@client.command()
async def bye(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send('You were removed from the voice channel')
    await member.edit(voice_channel=None)

@client.command()
async def wordle(ctx,*,reason=None):
  for i in range(6):
    try:
      guess = await ctx.bot.wait_for("message",timeout=10,check=lambda message: message.author==ctx.author and message.channel==ctx.channel)
      m = await ctx.send(guess.content)
      

    except asyncio.TimeoutError:
      await m.delete()


@client.command()
async def shh(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send("You have the right to remain silent") 
    await member.edit(mute = True)

@client.command()
async def unshh(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send("Your speaking priveleges are restored, Filthy Wench") 
    await member.edit(mute = False)

@client.command()
async def move(ctx,member : discord.Member,*,reason=None):
  if str(ctx.message.author) == 'Sank514#6682' or str(ctx.message.author) == 'MaleuS#3296':
    await ctx.send('You have been summoned')
    await member.edit(voice_channel=ctx.author.voice.channel)

@client.command()
async def sus(ctx,member : discord.Member,*,reason=None):
  if member.id!=617732810115121163:
    await ctx.send('Please leave')
    for i in ctx.message.guild.channels:
      if i.id==859454337130168362:
        channel=i

    await member.edit(voice_channel=channel)





@client.command(pass_context=True)
async def Ccommand(ctx,*,message):
  parts=message.split(",")
  db[parts[0].lower()]=parts[1]

@client.command(pass_context=True)
async def Rcommand(ctx,*,message):
  if str(ctx.message.author) == 'Sank514#6682':
    del db[message.lower()]

@client.command(pass_context=True)
async def Lcommand(ctx):
  if str(ctx.message.author) == 'Sank514#6682':
    for i in db.keys():
      await ctx.send(i+" : "+db[i])


@client.command()
async def newGroup(ctx,*,content:str):
  p = content.split(",")
  await ctx.send("Names : "+p[0]+" Group Name : "+p[1])
  customs = open("Customs.txt","a")
  customs.write("\n")
  customs.write(p[1])
  customs.close()
  mentions = open(p[1]+".txt","w")
  mentions.write(p[0])
  mentions.close()

  




@client.command(pass_context = True)
async def spam(ctx, member : discord.Member, *, content: str):
  for i in range(1,10):
    channel = await member.create_dm()
    await channel.send('<@!'+str(member.id)+'>'+content)








@client.command(pass_context = True)
async def imdb(ctx,*,content: str):
  movie = content.strip().split(' ')
  mov = "+".join(movie)
  
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
  sent=await ctx.send(embed=embedIt(movies,ratings,"Your Search Results"))
  sent2=await ctx.send("Which movie would you like to check out, You have 10 seconds to respond")
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
      A=soup.find('li',{"data-testid":"storyline-genres"})

      B=A.find_all('li',class_="ipc-inline-list__item")     
      sent=await ctx.send("Want the details? You have 15 seconds to reply type 'Y/y' or 'N/n'")
      try:
        choice = await ctx.bot.wait_for("message",timeout=15,check=lambda message: message.author==ctx.author and message.channel==ctx.channel)
        if 'y' in choice.content or 'Y' in choice.content:
          await ctx.send("Here are the Details: ")
          await ctx.send(f'The IMDb Rating is: {r}')
          await ctx.send(embed=embedIt2(B,"The Genres of this movie:"))
        else:
          await ctx.send("Bro what was the point then")

      except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("You took too long!",delete_after=10)

  except asyncio.TimeoutError:
    await sent.delete()
    await sent2.delete()
    await ctx.send("You took too long!",delete_after=10)
  


@client.command(pass_context = True)
async def addmovie(ctx,*,content: str):
  file = open('Votes.txt','a')
  file.write(content.strip()+'\n')
  file.close()
  m=await ctx.send("Alright, Added")
  await s(5)
  await m.delete()



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
  m=await ctx.send("Deleted")
  await s(5)
  await m.delete()

@client.command(pass_context = True)
async def movielist(ctx):
  file = open('Votes.txt','r')
  embed = discord.Embed(
    colour=discord.Colour.teal()
  )
  count=1
  embed.set_author(name="The Movie List: ")
  embed.set_thumbnail(url=ctx.message.author.avatar_url)
  movies=[]
  for each in file:
    embed.add_field(name=str(count).strip()+')',value=each,inline=False)
    movies.append(each)
    count=count+1
  message=await ctx.send(embed=embed)
  await s(5*60)
  await message.delete()



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
