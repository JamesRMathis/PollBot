from discord.utils import get
import discord
from discord.ext import commands
import os
import requests
import randfacts
from pyrandmeme import *
import json
from keep_alive import keep_alive


bot = commands.Bot(command_prefix= '$')

emojis = ['👍', '👎']

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return quote

@bot.event
async def on_ready():
  print('Bot is ready')
  await bot.change_presence(activity=discord.Game(name="use $help"))

@bot.command(
  help='Sends an inspiring quote'
)
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)

@bot.command(
  help='Sends a random fun fact'
)
async def funfact(ctx):
  fact = randfacts.getFact()
  await ctx.send(fact)

@bot.command(
  help='Sends a random meme'
)
async def meme(ctx):
  await ctx.send(embed=await pyrandmeme())

@bot.command(
  help='Shows the latency of the bot for you'
)
async def ping(ctx):
  await ctx.send(f'Latency: {round(bot.latency * 1000)} ms')

@bot.command(
  help='Creates a poll in the channel called "voting". There must be a voting channel for this to work. If the issue is more than one word long, you must put it in quotes "like this." The time unit defaults to being seconds, but you can specify it to be minutes, hours, or days. They must be spelled out completely and correctly, but capitalization does not matter'
)
async def poll(ctx, issue, timeLimit, timeUnit='seconds'):
  try:
    timeLimit = float(timeLimit)
  except ValueError:
    await ctx.send('The time limit must be a number!')
    return

  if timeUnit.upper() == 'SECONDS':
    pass
  elif timeUnit.upper() == 'MINUTES':
    timeLimit *= 60
  elif timeUnit.upper() == 'HOURS':
    timeLimit *= 3600
  elif timeUnit.upper() == 'DAYS':
    timeLimit *= 86400
  else:
    await ctx.send('Time unit invalid! Valid time units are minutes, hours, and days!')
    return

  vote_channel = get(ctx.guild.channels, name='voting')

  await ctx.message.delete()

  poll = await vote_channel.send('@everyone ' + issue)
  pollID = poll.id

  issueChars = list(issue)
  issue = ''
  broke = False

  for count, value in enumerate(issueChars):
    if count > 9:
      broke = True
      break

    issue = issue + str(issueChars[count])
  if broke:
    issue = issue + '...'

  await ctx.send('Poll sent!')

  for emoji in emojis:
    await poll.add_reaction(emoji)

  def check(reaction, user):
    return user != '808555253317894163' and str(reaction.emoji) in ['👍', '👎']

  yay = 0
  nay = 0
  loop = 0

  while loop == 0:
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=timeLimit, check=check)
      
    except:
      msg = await vote_channel.fetch_message(pollID)
      
      thumbUps = get(msg.reactions, emoji='👍')
      yay = thumbUps.count - 1

      thumbDowns = get(msg.reactions, emoji='👎')
      nay = thumbDowns.count - 1


      await ctx.send(f'@everyone Here are the results of poll with the issue "{issue}": \nYay: {yay}\nNay: {nay}')

      if yay > nay:
        await ctx.send('The vote comes out to yay!')
      elif yay < nay:
        await ctx.send('The vote comes out to nay!')
      elif yay == nay:
        await ctx.send('The vote is a tie!')
      
      loop = 1

keep_alive()
bot.run(os.getenv('TOKEN'))