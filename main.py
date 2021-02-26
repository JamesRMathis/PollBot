import discord
from discord.ext import commands
from replit import db
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
async def poll(ctx, issue):
  vote_channel = discord.utils.get(ctx.guild.channels, name='voting')
  general = discord.utils.get(ctx.guild.channels, name='general')

  await ctx.message.delete()

  poll = await vote_channel.send('@everyone ' + issue)

  for emoji in emojis:
    await poll.add_reaction(emoji)

@bot.event
async def on_reaction_add(reaction, user):
  if reaction.emoji == '👍'

keep_alive()
bot.run(os.getenv('TOKEN'))