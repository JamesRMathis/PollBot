from discord.utils import get
import discord
from discord.ext import commands
import os
import requests
import randfacts
from pyrandmeme import *
import json
from keep_alive import keep_alive
from replit import db


def get_prefix(client, message):
	prefix = db[str(message.guild.id)]
	return prefix


bot = commands.Bot(command_prefix=get_prefix)

def get_quote():
	response = requests.get('https://zenquotes.io/api/random')
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + ' -' + json_data[0]['a']
	return quote


@bot.event
async def on_ready():
	print('Bot is ready')
	await bot.change_presence(activity=discord.Game(name="use $help"))


@bot.event
async def on_guild_join(guild):
	db[str(guild.id)] = '$'


@bot.event
async def on_message(msg):
  if msg.author.id == '808555253317894163':
    return

  msgContent = msg.content.upper()

  if msgContent.startswith('PREFIX'):
    await msg.channel.send(
		    f'My prefix for this server is: {db[str(msg.guild.id)]}')

  await bot.process_commands(msg)


@bot.command(
    help=
    'Changes the prefix of the bot to a user-specified prefix. This is per server, and can only be run by people with administrator.'
)
@commands.has_permissions(administrator=True)
async def changePrefix(ctx, prefix):
	db[str(ctx.guild.id)] = prefix
	await ctx.send(f'Prefix changed to {prefix}!')


@bot.command(help='Sends the invite to the support server for this bot')
async def support(ctx):
	await ctx.send("Here's the link to the support server")
	await ctx.send('https://discord.gg/WrAkbkm59j')


@bot.command(help='Sends an inspiring quote')
async def inspire(ctx):
	quote = get_quote()
	await ctx.send(quote)


@bot.command(help='Sends a random fun fact')
async def funfact(ctx):
	fact = randfacts.getFact()
	await ctx.send(fact)


@bot.command(help='Sends a random meme')
async def meme(ctx):
	await ctx.send(embed=await pyrandmeme())


@bot.command(help='Shows the latency of the bot for you')
async def ping(ctx):
	await ctx.send(f'Latency: {round(bot.latency * 1000)} ms')


@bot.command(
    help=
    'Creates a poll in the channel the command is called. If the issue is more than one word long, you must put it in quotes "like this." The time limit can be any number with up to 7 decimal places, and the valid time units are seconds, minutes, hours, and days. If you want to specify the emojis used for yay and nay,but not the time, then put 0 for both time limit and time unit.'
)
async def poll(ctx, issue, timeLimit=None, timeUnit=None, customYay='👍', customNay='👎'):
  emojis = [customYay, customNay]

  if timeLimit is not None:
    try:
      timeLimit = float(timeLimit)
    except ValueError:
      await ctx.send('The time limit must be a number!')
      return

  if timeLimit is None and timeUnit is None:
    pass
  elif timeUnit.upper().startswith('SEC'):
    pass
  elif timeUnit.upper().startswith('MIN'):
    timeLimit *= 60
  elif timeUnit.upper().startswith('HOU'):
    timeLimit *= 3600
  elif timeUnit.upper().startswith('DAY'):
    timeLimit *= 86400
  else:
    await ctx.send(
		    "Time unit invalid! Valid time units are minutes, hours, and days! If you don't specify the time limit, then you also can't specify the time unit."
		)
    return

  await ctx.message.delete()

  poll = await ctx.send('@everyone ' + issue)
  pollID = poll.id

  issueChars = list(issue)
  issue = ''
  broke = False

  for count, value in enumerate(issueChars):
    if count > 19:
    	broke = True
    	break

    issue = issue + str(issueChars[count])
  if broke:
  	issue = issue + '...'

  for emoji in emojis:
  	await poll.add_reaction(emoji)

  def check(reaction, user):
  	return user != '808555253317894163' and str(
		    reaction.emoji) in [customYay, customNay]

  if timeLimit is not None:
    yay = 0
    nay = 0
    loop = 0

    while loop == 0:
      try:
        reaction, user = await bot.wait_for('reaction_add', timeout=timeLimit, check=check)

      except:
        msg = await ctx.fetch_message(pollID)

        thumbUps = get(msg.reactions, emoji=customYay)
        yay = thumbUps.count - 1

        thumbDowns = get(msg.reactions, emoji=customNay)
        nay = thumbDowns.count - 1

        await ctx.send(
            f'@everyone Here are the results of poll with the issue "{issue}": \nYay: {yay}\nNay: {nay}'
        )

        if yay > nay:
          await ctx.send('The vote comes out to yay!')
        elif yay < nay:
          await ctx.send('The vote comes out to nay!')
        elif yay == nay:
          await ctx.send('The vote is a tie!')

        loop = 1


keep_alive()
bot.run(os.getenv('TOKEN'))
