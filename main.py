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

@bot.event
async def on_message(message):
  ctx = await bot.get_context(message)
  if message.author.id == '808555253317894163':
    return

  msg = message.content
  # del db['{} money'.format(message.author.id)]

  vote_channel = discord.utils.get(ctx.guild.channels, name='voting')

  if msg.startswith('$inspire') or msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if msg.startswith('$funfact'):
    fact = randfacts.getFact()
    await message.channel.send(fact)
  
  if msg.startswith('$money'):
    if '-account' in msg:
      money = db['{} money'.format(message.author.id)]
      await message.channel.send('$' + str(money))

    if '-a ' in msg:
      money_to_add = msg.split('-a ', 1)[1]

      try:
        money_to_add = int(money_to_add)
      except:
        await message.channel.send('The amount to add must be an integer!')

      money_in_acnt = db['{} money'.format(message.author.id)]
      money_in_acnt += money_to_add

      db['{} money'.format(message.author.id)] = money_in_acnt

      await message.channel.send('{} has gained ${}'.format(message.author, money_to_add))

    elif '-r ' in msg:
      money_to_take = msg.split('-r ', 1)[1]

      try:
        money_to_take = int(money_to_take)
      except:
        await message.channel.send('The amount to take must be a number!')

      money_in_acnt = db['{} money'.format(message.author.id)]
      money_in_acnt -= money_to_take

      db['{} money'.format(message.author.id)] = money_in_acnt

      await message.channel.send('{} has removed ${}'.format(message.author, money_to_take))

    elif '-u ' in msg:
      command = msg.split('-u', 1)[1]

      if 'add' in command:
        db['{} money'.format(message.author.id)] = 0
        await message.channel.send('Account created and bound to you!')
      
      elif 'del' in command:
        del db['{} money'.format(message.author.id)]
        await message.channel.send('Your account was deleted!')

  if msg.startswith('$meme'):
    await message.channel.send(embed=await pyrandmeme())

  if msg.startswith('$poll'):
    issue = msg.split('$poll ', 1)[1]
    # chars_list = [char for char in issue]

    # try:
    #   minutes = int(chars_list[-3] + chars_list[-2] + chars_list[-1])
    #   chars_list.pop(-1)
    #   chars_list.pop(-1)
    #   chars_list.pop(-1)
    #   chars_list.pop(-1)

    #   issue = ''

    #   for element in chars_list:
    #     issue += str(element)
    # except ValueError:
    #   await message.channel.send('Last 3 characters must be integers!')

    # db['minutes'] = minutes

    await message.delete()

    poll = await vote_channel.send('@everyone ' + issue)

    for emoji in emojis:
      await poll.add_reaction(emoji)
    
  if msg.startswith('$help'):
    embedVar = discord.Embed(title='Help', description='List of PollBot commands', color=0x00ff00)
    embedVar.add_field(name='$inspire', value='Sends a random inspirational quote', inline=False)
    embedVar.add_field(name='$quote', value='Sends a random inspirational quote', inline=False)
    embedVar.add_field(name='$funfact', value='Sends a random fun fact', inline=False)
    embedVar.add_field(name='$meme', value='Sends a random meme', inline=False)
    embedVar.add_field(name='$poll <issue>', value='Posts a poll with the issue in the channel called "voting" that will ping everyone and add the thumbs up and down reactions for voting', inline=False)
    await message.channel.send(embed=embedVar)

# @bot.event
# async def on_reaction_add(reaction, user):
#   emoji = reaction.emoji
#   yay = 0
#   nay = 0
#   time_limit = db['minutes']
#   del db['minutes']
#   # minutes *= 60

#   if user.bot:
#     return

#   main_channel = discord.utils.get(ctx.guild.channels, name='general')
  
#   if emoji == '👍':
#     yay += 1
#   elif emoji == '👎':
#     nay += 1
#   else:
#     return
  
#   start_time = time.time()
#   while (time.time() - start_time) < time_limit:
#     pass
#   else:
#     await main_channel.send('Yay: ' + str(yay) + '\nNay: ' + str(nay))
#     if yay > nay:
#       await main_channel.send('@everyone Result: Yay')
#     else:
#       await main_channel.send('@everyone Result: Nay')

keep_alive()
bot.run(os.getenv('TOKEN'))