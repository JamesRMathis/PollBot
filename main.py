import discord
from discord.ext import commands
from replit import db
import os
import time
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
  help='Creates a poll in the channel called "voting". There must be a voting channel for this to work'
)
async def poll(ctx, *, issue):
  vote_channel = discord.utils.get(ctx.guild.channels, name='voting')

  await ctx.message.delete()

  poll = await vote_channel.send('@everyone ' + issue)

  for emoji in emojis:
    await poll.add_reaction(emoji)

  def check(reaction, user):
    return user != '808555253317894163' and str(reaction.emoji) in ['👍', '👎']

  yay = 0
  nay = -1
  loop = 0

  while loop == 0:
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
      if reaction.emoji == '👍' and user != '808555253317894163':
        yay += 1
      elif reaction.emoji == '👎' and user != '808555253317894163':
        nay += 1
      
    except:
      await ctx.send('Yay: {}\nNay: {}'.format(yay, nay))

      if yay > nay:
        await ctx.send('The vote comes out to yay!')
      elif yay < nay:
        await ctx.send('The vote comes out to nay!')
      elif yay == nay:
        await ctx.send('The vote is a tie!')
      
      loop = 1

keep_alive()
bot.run(os.getenv('TOKEN'))